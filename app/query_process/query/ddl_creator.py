import re

from simple_ddl_parser import DDLParser

def get_metadata(db, ddl_query):
    # clean ddl query by deleting auto increment
    parse_results = DDLParser(ddl_query).run()
    case_insensitive = re.compile(re.escape('CREATE TABLE'), re.IGNORECASE)
    ddl_query = case_insensitive.sub('', ddl_query)
    word_started=False
    start_pos=0
    end_pos=0
    increment=0
    for x in ddl_query:
        if x == ' ':
            if word_started:
                end_pos = increment
                end_pos += 1
                break
        else:
            if not word_started:
                start_pos = increment
                word_started=True
        increment += 1
    print(f"Expected string and start-pos and end-pos {ddl_query},  {start_pos},  {end_pos}")

    ddl_query = ddl_query.replace('`', '"')
    ddl_query = ddl_query.replace('\n', '')
    ddl_query = ddl_query.replace('AUTO INCREMENT', '')
    ddl_query = ddl_query.replace('AUTO_INCREMENT', '')
    ddl_query = ddl_query.replace('DEFAULT NULL', '')
    start_pos = ddl_query.find("ENGINE=InnoDB")
    statement = ddl_query[0:start_pos]
    # statement = 'CREATE TABLE "customers" (  "id" int(11) NOT NULL AUTO_INCREMENT,  "first_name" varchar(255) NOT NULL,  "last_name" varchar(255) NOT NULL,  "email" varchar(255) NOT NULL,  PRIMARY KEY ("id"), "email" varchar(255)) '
    result = DDLParser(statement).run(output_mode="mysql")
    primary_key = ','.join(result[0]["primary_key"])
    print(f"Result from ddl parsing : {primary_key}")
    return ddl_query[start_pos: end_pos], primary_key




    # case_insensitive_auto_increment = re.compile(re.escape('AUTO_INCREMENT'), re.IGNORECASE)
    # ddl_query = case_insensitive_auto_increment.sub('', ddl_query)
    # rm_unnecessary = re.compile(re.escape('=110 DEFAULT CHARSET=latin1'), re.IGNORECASE)
    # ddl_query = rm_unnecessary.sub('', ddl_query)
    # rm_engine = re.compile(re.escape('ENGINE=InnoDB'), re.IGNORECASE)
    # ddl_query = rm_engine.sub('', ddl_query)
    # table_separation = ddl_query.split('(')
    # table_name = table_separation[0]
    # ddl_query = ddl_query.strip('\n')
    # column_separator = ddl_query.split(',')
    # # for column in column_separator:
    # #     for char in column:
    # #         if char == "'"

def alter_table_query(db, ddl_query):
    return ddl_query

def delete_table_query(db, ddl_query):
    return ddl_query





