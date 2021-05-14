import json
import sys

from app.connector import redshift_connection
from .query import dml_creator,ddl_creator
import re


def process_message(msg_val, is_ddl):
    sys.stderr.write('%% %s [%d] at offset %d with key %s:\n' %
                     (msg_val.topic(), msg_val.partition(), msg_val.offset(),
                      str(msg_val.key())))
    print(f"msg.value() is: {msg_val.value()}")

    if msg_val.value() is not None:
        msg_value_dict = json.loads(msg_val.value().decode('utf-8'))
        print(f"msg_value_str is: {msg_value_dict}")
        if is_ddl is not None:

            # msg format is
            # {
            #   "source" : {
            #     "server" : "mysql"
            #   },
            #   "position" : {
            #     "ts_sec" : 1620903794,
            #     "file" : "mysql-bin.000072",
            #     "pos" : 360,
            #     "server_id" : 223344
            #   },
            #   "databaseName" : "inventory",
            #   "ddl" : "ALTER TABLE orders ADD COLUMN first_referrer varchar(100)"
            # }
            ddl_query_applied = msg_value_dict["ddl"]
            database = msg_val["database"]
            if re.search('CREATE TABLE', ddl_query_applied, re.IGNORECASE):
                print(f"expected create table scenario : ", {ddl_query_applied})
                # Ignoring these use cases currently as create runs on its own
                # ddl_query = ddl_creator.create_table_query(database, ddl_query_applied)
                # result = redshift_connection.push_to_redshift(database, ddl_query)
            elif re.search("ALTER TABLE ", ddl_query_applied, re.IGNORECASE):
                print(f"expected alter table scenario : ", {ddl_query_applied})

                if re.search("REFERENCES", ddl_query_applied, re.IGNORECASE):
                    print(f"expected alter table scenario other than column ones : ", {ddl_query_applied})
                ## Leaving this comment here. Make changes here for handling alter table commands other than drop or create columns

                else :
                    print(f"Expected scenario with alter table drop or add columns : ", {ddl_query_applied})
                    ddl_query = ddl_creator.alter_table_query(database, ddl_query_applied)
                    result = redshift_connection.push_to_redshift(database, ddl_query)

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
                else :
                    sql_query = dml_creator.update_record_query(after, db, table)
                    result = redshift_connection.push_to_redshift(db, sql_query)