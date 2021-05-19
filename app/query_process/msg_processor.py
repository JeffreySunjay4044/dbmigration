import json

from connector import redshift_connection
from api_client.dto import api_payload
from api_client import sink_connector
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
                print(f"msg_value_dict {msg_value_dict}")
                ddl_db = msg_value_dict["databaseName"]
                if ddl_db == db:
                    print(f"Expected create table scenario for db: {db}")
                    print(f"expected create table scenario : {ddl_query_applied}")
                    ## Commenting these lines for local testing.
                    # table_name, primary_key=ddl_creator.get_metadata(db, ddl_query_applied)
                    # json_payload = api_payload.sink_connector_payload(table_name,primary_key)
                    # connector_name = json_payload["name"]
                    # context_path = f"connectors/{connector_name}/config"
                    # sink_connector.api_call(context_path, json)
                else:
                    print(f"Not proceeding further as db is {ddl_db}")

            elif re.search("ALTER TABLE ", ddl_query_applied, re.IGNORECASE):
                print(f"expected alter table scenario : {ddl_query_applied}")

                if re.search("REFERENCES", ddl_query_applied, re.IGNORECASE):
                    print(f"expected alter table scenario other than column ones :  {ddl_query_applied}")
                else:
                    print(f"Expected scenario with alter table drop or add columns : {ddl_query_applied}")
                    ddl_query = ddl_creator.alter_table_query(db, ddl_query_applied)
                    result = redshift_connection.push_to_redshift(db, ddl_query, False)
            elif re.search("DROP TABLE", ddl_query_applied, re.IGNORECASE):
                print(f"Exepected scenario : {ddl_query_applied}")
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
