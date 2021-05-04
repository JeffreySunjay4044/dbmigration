# dbmigration

Using debezium and an intelligent python redshift sink consumer .


Important docker commands to execute:
docker-compose up --detach dbmigration : to compose up a single container


INSERT INTO products ( dict_keys(['id', 'name', 'description', 'weight']) ) values (dict_values([101, 'scooter', 'Small 2-wheel scooter', 3.140000104904175]))