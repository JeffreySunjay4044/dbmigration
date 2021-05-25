import re

from simple_ddl_parser import DDLParser
from query_process.metadata import type_metadata


def get_metadata(db, ddl_query):
    # clean ddl query by deleting auto increment
    ddl_query = ddl_query.replace('`', '"')
    ddl_query = ddl_query.replace('\n', '')
    ddl_query = ddl_query.replace('AUTO INCREMENT', '')
    ddl_query = ddl_query.replace('AUTO_INCREMENT', '')
    ddl_query = ddl_query.replace('DEFAULT NULL', '')
    start_pos = ddl_query.find("ENGINE=InnoDB")
    statement = ddl_query[0:start_pos]
    result = DDLParser(statement).run(output_mode="mysql")

    case_insensitive = re.compile(re.escape('CREATE TABLE'), re.IGNORECASE)
    ddl_query = case_insensitive.sub('', ddl_query)
    word_started = False
    start_pos = 0
    end_pos = 0
    increment = 0
    for x in ddl_query:
        if x == ' ':
            if word_started:
                end_pos = increment
                end_pos += 1
                break
        else:
            if not word_started:
                start_pos = increment
                word_started = True
        increment += 1
    print(f"Expected string and start-pos and end-pos {ddl_query},  {start_pos},  {end_pos}")
    table_name = ddl_query[start_pos:end_pos]
    return table_name, "id"


def alter_table_query(db, ddl_query):
    return type_metadata.convert_query(ddl_query)


def delete_table_query(db, ddl_query):
    db_with_dot = f"{db}."
    ddl_query = ddl_query.replace("`", "")
    ddl_query = ddl_query.replace(db_with_dot, '')
    print(f"ddl_query is : {ddl_query}")
    return ddl_query
