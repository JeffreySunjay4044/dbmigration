import json
import sys
import os
from typing import NamedTuple, Optional
import redshift_connector
from singleton_decorator import singleton
from confluent_kafka import Consumer, KafkaException, KafkaError

class ConnInfo(NamedTuple):
    """ Represents Redshift Connection Information """
    user: str
    password: str
    host: str
    database: str

def build_conn_info(
    user: Optional[str] = None,
    password: Optional[str] = None,
    host: Optional[str] = None,
    database: Optional[str] = None,
) -> ConnInfo:
    """
    Parse arguments and return connection info for Redshift
    """
    return ConnInfo(
        user=user or os.environ["ANALYTICS_DB_USER"],
        password=password or os.environ["ANALYTICS_DB_PASSWORD"],
        host=host or os.environ["ANALYTICS_DB_HOST"],
        database=database or os.environ["ANALYTICS_DB_NAME"],
    )



@singleton
class RedshiftConnection:
    def __init__(self, conn_info):
        self.conn_info = conn_info
    def getClient(self):
        conn = redshift_connector.connect(
            host=self.conn_info.host,
            database=self.conn_info.database,
            user=self.conn_info.user,
            password=self.conn_info.password
        )
        return conn
def push_to_redshift(db, sql_query):
    conn_info = build_conn_info(
        host='redshift',
        database=db,
        user='postgres',
        password='debezium'
    )
    print(f"conn info is {conn_info}")
    connection = RedshiftConnection(conn_info).getClient()
    cursor: redshift_connector.Cursor = connection.cursor()
    cursor.execute(sql_query)
    result: tuple = cursor.fetchall()
    print(result)
    return result

if __name__ == '__main__':
    topics = ["mysql.inventory.products"]
    # Consumer configuration
    # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    conf = {
        'bootstrap.servers': 'kafka:9092',
        'group.id': "Mercato_test",
        'session.timeout.ms': 6000,
        'default.topic.config': {'auto.offset.reset': 'smallest'},
        # 'security.protocol': 'SSL',
        # 'sasl.mechanisms': 'SCRAM-SHA-256',
        # 'sasl.username': os.environ['CLOUDKARAFKA_USERNAME'],
        # 'sasl.password': os.environ['CLOUDKARAFKA_PASSWORD']
    }
    # conn_info = build_conn_info(
    #     user='postgres',
    #     password='debezium',
    #     host='redshift',
    #     database='inventory'
    # )
    c = Consumer(**conf)
    c.subscribe(topics)
    try:
        while True:
            msg = c.poll(timeout=1.0)
            if msg is None:
                continue
            print(f"message is {msg}")
            if msg.error():
                # Error or event
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                     (msg.topic(), msg.partition(), msg.offset()))
                elif msg.error():
                    # Error
                    raise KafkaException(msg.error())
            else:
                # Proper message
                sys.stderr.write('%% %s [%d] at offset %d with key %s:\n' %
                                 (msg.topic(), msg.partition(), msg.offset(),
                                  str(msg.key())))
                print(f"msg.value() is: {msg.value()}")

                topic = msg.topic()

                if msg.value() is not None:
                    msg_value_dict = json.loads(msg.value().decode('utf-8'))
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
                                after_keys = after.keys()
                                # if type(after.keys()) is not str:
                                #     after_keys = json.dumps(after.keys())
                                val_list = after.values()
                                # if type(after.values()) is not str:
                                #     val_list = json.dumps(after.values())
                                sql_query = f"INSERT INTO {table} ( {after_keys} ) values ({val_list})"
                                print(f"sql query is {sql_query}")
                                result = push_to_redshift(db, sql_query)
                        elif after is None:
                            if before is not None:
                                before_keys = ""
                                if type(before.keys()) is not str:
                                    before_keys = json.dumps(before.keys())
                                val_list = ""
                                if type(before.values()) is not str:
                                    val_list = json.dumps(before.values())
                                sql_query = f"UPDATE {table} ( {before_keys} ) values ({val_list})"
                                result = push_to_redshift(db, sql_query)
    except KeyboardInterrupt:
        sys.stderr.write('%% Aborted by user\n')
    # Close down consumer to commit final offsets.
    c.close()
    # Connects to Redshift cluster using AWS credentials