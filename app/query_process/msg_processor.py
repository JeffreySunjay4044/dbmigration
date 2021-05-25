import json

from connector import redshift_connection
from query_process.query import ddl_creator
import re


def process_message(msg_val, is_ddl):
    result = {}
    if msg_val.value() is not None:
        msg_value_dict = json.loads(msg_val.value().decode('utf-8'))
        print(f"msg_value_str is: {msg_value_dict}")
        if is_ddl is not None:
            ddl_query_applied = msg_value_dict["ddl"]
            db = "inventory"
            if re.search('CREATE TABLE', ddl_query_applied, re.IGNORECASE):
                print(f"Not handling this feature here . Handled in dml")
            elif re.search("ALTER TABLE ", ddl_query_applied, re.IGNORECASE):
                if re.search("REFERENCES", ddl_query_applied, re.IGNORECASE):
                    print(f"expected alter table scenario other than column ones :  {ddl_query_applied}")
                else:
                    ddl_query = ddl_creator.alter_table_query(db, ddl_query_applied)
                    if ddl_query is not None:
                        result = redshift_connection.push_to_redshift(db, ddl_query, False)
            elif re.search("DROP TABLE", ddl_query_applied, re.IGNORECASE):
                ddl_query = ddl_creator.delete_table_query(db, ddl_query_applied)
                result = redshift_connection.push_to_redshift(db, ddl_query, False)
            else:
                print(f"Encountered unexpected scenario : {ddl_query_applied}")
    return result
