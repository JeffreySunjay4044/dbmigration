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
            print(f"before_value is {before} and after_value is {after}")
            if before is None:
                if after is not None:
                    sql_query = ddl_creator.insert_record_query(after, db, table)
                    result = redshift_connection.push_to_redshift(db, sql_query)
            elif after is None:
                if before is not None:
                    sql_query = ddl_creator.delete_record_query(after, db, table)
                    result = redshift_connection.push_to_redshift(db, sql_query)
            else :
                sql_query = ddl_creator.update_record_query(after, db, table)
                result = redshift_connection.push_to_redshift(db, sql_query)
