# ---------------------------------------------------------------------------------------------------------------------
# CREATE application TO DATA LAKE STATE MACHINE
# ---------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------------
# CONFIGURE OUR AWS CONNECTION
# ---------------------------------------------------------------------------------------------------------------------

provider "aws" {
  # The AWS region in which all resources will be created
  region = var.aws_region
}

locals {
  default_tags = {
    "application" = var.application,
    "env"         = var.aws_environment_name,
    "provider"    = "aws"
  }

  process_glue_job_file = "default_glue_json_to_parquet_processing_job.py"
  s3_scripts_path         = "glue-scripts"
  name                    = "${lower(replace(var.application, " ", "-"))}-process-parquet"
  # Merge the default tags with any extra passed in by the user into a single map
  tags = merge(local.default_tags, var.tags)

}

# ---------------------------------------------------------------------------------------------------------------------
# CREATE IAM RESOURCES FOR STATE MACHINE
# ---------------------------------------------------------------------------------------------------------------------

data "aws_iam_policy_document" "phoenix_raw_data_to_parquet_state_machine_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      identifiers = ["states.${var.aws_region}.amazonaws.com"]
      type        = "Service"
    }
  }
}

resource "aws_iam_role" "phoenix_raw_data_to_parquet_state_machine_role" {
  assume_role_policy = data.aws_iam_policy_document.phoenix_raw_data_to_parquet_state_machine_policy_document.json
  name               = "${var.application}-raw-data-to-parquet-state-machine-role"
}

data "aws_iam_policy_document" "phoenix_raw_data_to_parquet_state_machine_policy_document" {
  statement {
    actions = ["logs:CreateLogDelivery",
      "logs:GetLogDelivery",
      "logs:UpdateLogDelivery",
      "logs:DeleteLogDelivery",
      "logs:ListLogDeliveries",
      "logs:PutResourcePolicy",
      "logs:DescribeResourcePolicies",
    "logs:DescribeLogGroups"]
    effect    = "Allow"
    resources = ["*"]
  }

  statement {
    actions = ["glue:StartJobRun",
      "glue:GetJobRun",
      "glue:GetJobRuns",
      "glue:BatchStopJobRun"
    ]
    effect    = "Allow"
    resources = ["*"]
  }
}

resource "aws_iam_policy" "phoenix_raw_data_to_parquet_state_machine_policy" {
  name   = "${var.application}-raw-data-to-parquet-state-machine-policy"
  policy = data.aws_iam_policy_document.phoenix_raw_data_to_parquet_state_machine_policy_document.json
}

resource "aws_iam_role_policy_attachment" "phoenix_raw_data_to_parquet_state_machine_role_policy_attachment" {
  policy_arn = aws_iam_policy.phoenix_raw_data_to_parquet_state_machine_policy.arn
  role       = aws_iam_role.phoenix_raw_data_to_parquet_state_machine_role.name
}

# ---------------------------------------------------------------------------------------------------------------------
# CREATE APPLICATION TO PROCESS PARQUET STATE MACHINE
# ---------------------------------------------------------------------------------------------------------------------
data "template_file" "state_machine_definition" {
  template = file("${path.module}/definition/raw-data-process-parquet-sfn.yaml")
  vars = {
    job_names       = jsonencode(module.glue_jobs.*.glue_job_name)
    max_concurrency = var.max_concurrency
  }
}

resource "aws_sfn_state_machine" "data_lake_process_parquet_state_machines" {
  definition = jsonencode(yamldecode(data.template_file.state_machine_definition.rendered))

  logging_configuration {
    include_execution_data = true
    level                  = "ALL"
    log_destination        = "${aws_cloudwatch_log_group.data_lake_processing_log_group.arn}:*"
  }

  name     = local.name
  role_arn = aws_iam_role.phoenix_raw_data_to_parquet_state_machine_role.arn
  tags     = local.tags
}

# ---------------------------------------------------------------------------------------------------------------------
# Glue Connection
# ---------------------------------------------------------------------------------------------------------------------

module "source_glue_connection" {

  source                 = "/Users/sachinsharma/PycharmProjects/infrastructure_modules/data-lake/glue-connection"
  application            = var.application
  availability_zone      = data.terraform_remote_state.vpc.outputs.availability_zones[0][0]
  aws_environment_name   = var.aws_environment_name
  aws_region             = var.aws_region
  catalog_id             = var.aws_account_id
  jdbc_connection_url    = var.glue_connection_jdbc_connection_url
  password               = var.glue_connection_password
  security_group_id_list = distinct(concat(var.glue_connection_security_groups, [aws_security_group.glue_security_group.id]))
  subnet_id              = data.terraform_remote_state.vpc.outputs.private_persistence_subnet_ids[0]
  username               = var.glue_connection_username
}

# ---------------------------------------------------------------------------------------------------------------------
# Glue Jobs
# ---------------------------------------------------------------------------------------------------------------------

module "glue_jobs" {
  source                 = "/Users/sachinsharma/PycharmProjects/infrastructure_modules/data-lake/glue-job"

  count = length(var.glue_params)

  application          = var.application
  aws_environment_name = var.aws_environment_name
  aws_region           = var.aws_region

  default_arguments = {
    "--destination_path"  = "s3://${aws_s3_bucket.datalake_s3_bucket.bucket}/processed/${var.glue_params[count.index]["source_table"]}/"
    "--output_format"     = "parquet"
    "--source_database"   = var.source_glue_database
    "--source_table"      = "${var.source_database}_${var.source_schema}_${var.glue_params[count.index]["source_table"]}"
    "--run_date_iso_8601" = "none"
  }

  connections       = [module.source_glue_connection.name]
  glue_version      = var.glue_version
  name              = var.glue_params[count.index]["source_table"]
  number_of_workers = var.glue_job_number_of_workers
  role_arn          = aws_iam_role.glue_role.arn
  tags              = local.tags
  timeout           = var.glue_job_timeout
  script_location   = "s3://${aws_s3_bucket_object.basic_glue_job.bucket}/${aws_s3_bucket_object.basic_glue_job.key}"
  worker_type       = var.glue_job_worker_type
}

# ---------------------------------------------------------------------------------------------------------------------
# Security Group
# ---------------------------------------------------------------------------------------------------------------------

resource "aws_security_group" "glue_security_group" {
  name   = "${var.application}-phoenix-raw-data-to-parquet-security-group"
  tags   = local.tags
  vpc_id = data.terraform_remote_state.vpc.outputs.vpc_id

  egress {
    description = "Self-referencing egress for Glue Jobs"
    from_port   = 0
    protocol    = "tcp"
    self        = true
    to_port     = 65535
  }

  egress {
    description = "Egress to data source subnets"
    cidr_blocks = var.source_cidr_blocks
    from_port   = var.source_from_port
    protocol    = "tcp"
    to_port     = var.source_to_port
  }

  egress {
    description     = "Egress to S3 VPC endpoint"
    from_port       = 443
    prefix_list_ids = ["pl-63a5400a"]
    protocol        = "tcp"
    to_port         = 443
  }

  ingress {
    description = "Self-referencing ingress for Glue Jobs"
    from_port   = 0
    protocol    = "tcp"
    self        = true
    to_port     = 65535
  }
}

# ---------------------------------------------------------------------------------------------------------------------
# PULL DATA FROM OTHER TERRAFORM TEMPLATES USING TERRAFORM REMOTE STATE
# These templates use Terraform remote state to access data from a number of other Terraform templates, all of which
# store their state in S3 buckets.
# ---------------------------------------------------------------------------------------------------------------------

data "terraform_remote_state" "vpc" {
  backend = "s3"
  config = {
    region = var.terraform_state_aws_region
    bucket = var.terraform_state_s3_bucket
    key    = "${var.aws_region}/${var.vpc_name}/vpc/terraform.tfstate"
  }
}

# ---------------------------------------------------------------------------------------------------------------------
# S3 buckets
# ---------------------------------------------------------------------------------------------------------------------
resource "aws_s3_bucket" "datalake_s3_bucket" {
  acl    = "private"
  bucket = "${var.application}-datalake-${var.aws_environment_name}"
  tags   = local.tags

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}

resource "aws_s3_bucket" "scripts_s3_bucket" {
  acl    = "private"
  bucket = "${var.application}-scripts-${var.aws_environment_name}"
  tags   = local.tags

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  versioning {
    enabled = true
  }
}

resource "aws_s3_bucket_object" "basic_glue_job" {
  bucket = aws_s3_bucket.scripts_s3_bucket.bucket
  key    = "${local.s3_scripts_path}/${local.process_glue_job_file}"
  source = local.process_glue_job_file
  etag   = filemd5(local.process_glue_job_file)
}
# ---------------------------------------------------------------------------------------------------------------------
# IAM Roles and Policies for the glue resources
# ---------------------------------------------------------------------------------------------------------------------

data "aws_iam_policy_document" "datalake_s3_access_data" {
  statement {
    effect = "Allow"
    actions = [
      "s3:ListBucket"
    ]
    resources = [
      "arn:aws:s3:::${aws_s3_bucket.datalake_s3_bucket.bucket}"
    ]
  }

  statement {
    effect = "Allow"
    actions = [
      "s3:PutObject"
      , "s3:GetObject"
      , "s3:DeleteObject"
    ]
    resources = [
      "arn:aws:s3:::${aws_s3_bucket.datalake_s3_bucket.bucket}/*"
    ]
  }

  statement {
    effect = "Allow"
    actions = [
      "s3:GetObject"
    ]
    resources = [
      "arn:aws:s3:::${aws_s3_bucket.scripts_s3_bucket.bucket}/${local.s3_scripts_path}/*"
    ]
  }
}

resource "aws_iam_policy" "datalake_s3_access_policy" {
  description = "Data lake S3 access policy"
  name        = "${var.application}-datalake-s3-access"
  path        = "/"
  policy      = data.aws_iam_policy_document.datalake_s3_access_data.json
}

resource "aws_iam_role_policy_attachment" "glue_service_role_attachment" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
  role       = aws_iam_role.glue_role.name
}

resource "aws_iam_role_policy_attachment" "glue_datalake_s3_attachment" {
  policy_arn = aws_iam_policy.datalake_s3_access_policy.arn
  role       = aws_iam_role.glue_role.name
}

resource "aws_iam_role" "glue_role" {
  assume_role_policy = file("${path.module}/policies/glue_role_policy.json")
  name               = "${var.application}-glue-role"
}

# ---------------------------------------------------------------------------------------------------------------------
# CREATE APPLICATION TO PROCESS PARQUET STATE MACHINE LOG GROUP
# ---------------------------------------------------------------------------------------------------------------------

resource "aws_cloudwatch_log_group" "data_lake_processing_log_group" {
  name              = "/aws/vendedlogs/states/${local.name}"
  retention_in_days = var.retention_in_days
  tags              = local.tags
}
