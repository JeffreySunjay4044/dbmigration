import json
import sys

from app.connector import redshift_connection
from .query import ddl_creator




def process_message(msg_val):
    sys.stderr.write('%% %s [%d] at offset %d with key %s:\n' %
                     (msg_val.topic(), msg_val.partition(), msg_val.offset(),
                      str(msg_val.key())))
    print(f"msg.value() is: {msg_val.value()}")


    if msg_val.value() is not None:
        msg_value_dict = json.loads(msg_val.value().decode('utf-8'))
        print(f"msg_value_str is: {msg_value_dict}")

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
            sql_query = f"INSERT INTO {table}"
            values = payload["after"].keys()
            print(f"before_value is {before} and after_value is {after}")
            if before is None:
                if after is not None:
                    sql_query = ddl_creator.create_record_query(after, table)
                    result = redshift_connection.push_to_redshift(db, sql_query)
            elif after is None:
                if before is not None:
                    before_keys = before.keys()
                    before_keys = ",".join(before_keys)
                    print(f"Checking format for keys {before_keys}")
                    # if type(after.keys()) is not str:
                    #     after_keys = json.dumps(after.keys())
                    val_list = before.values()
                    count = 0
                    converted_values = ""
                    for val in val_list:
                        if count > 0:
                            converted_values += ','
                        elif count == 0:
                            count = 1
                        if type(val) is not str:
                            val = str(val)
                        elif type(val) is str:
                            val = "'" + val + "'"
                        converted_values += val

                    print(f"Checking format for values {converted_values}")
                    # if type(after.values()) is not str:
                    sql_query = f"INSERT INTO {table} VALUES ({converted_values})"
                    print(f"sql query is {sql_query}")
                    result = redshift_connection.push_to_redshift(db, sql_query)