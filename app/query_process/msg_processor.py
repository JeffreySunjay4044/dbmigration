import json

from connector import redshift_connection
from query_process.query import dml_creator, ddl_creator
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

        elif is_ddl is None:
            payload = msg_value_dict["payload"]
            if type(payload) is not dict:
                payload = json.loads(payload)

            if payload and payload["source"] is not None:

                source = payload["source"]
                if type(source) is not dict:
                    source = json.loads(source)
                db = source["db"]
                table = source["table"]
                before = payload["before"]
                if before is not None:
                    if type(before) is not dict:
                        before = json.loads(before)
                after = payload["after"]
                if after is not None:
                    if type(after) is not dict:
                        after = json.loads(after)
                print(f"before_value is {before} and after_value is {after}")
                if before is None:
                    if after is not None:
                        sql_query = dml_creator.insert_record_query(after, db, table)
                        result = redshift_connection.push_to_redshift(db, sql_query)
                elif after is None:
                    if before is not None:
                        sql_query = dml_creator.delete_record_query(after, db, table)
                        result = redshift_connection.push_to_redshift(db, sql_query)
                else:
                    sql_query = dml_creator.update_record_query(after, db, table)
                    result = redshift_connection.push_to_redshift(db, sql_query)
    return result
