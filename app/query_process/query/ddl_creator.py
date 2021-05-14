import re

def create_table_query(db, ddl_query):
    # clean ddl query by deleting auto increment
    case_insensitive = re.compile(re.escape('CREATE TABLE'), re.IGNORECASE)
    ddl_query = case_insensitive.sub('', ddl_query)
    case_insensitive_auto_increment = re.compile(re.escape('AUTO_INCREMENT'), re.IGNORECASE)
    ddl_query = case_insensitive_auto_increment.sub('', ddl_query)
    rm_unnecessary = re.compile(re.escape('=110 DEFAULT CHARSET=latin1'), re.IGNORECASE)
    ddl_query = rm_unnecessary.sub('', ddl_query)
    rm_engine = re.compile(re.escape('ENGINE=InnoDB'), re.IGNORECASE)
    ddl_query = rm_engine.sub('', ddl_query)
    table_separation = ddl_query.split('(')
    table_name = table_separation[0]
    ddl_query = ddl_query.strip('\n')
    column_separator = ddl_query.split(',')
    # for column in column_separator:
    #     for char in column:
    #         if char == "'"

def alter_table_query(db, ddl_query):
    return ddl_query





