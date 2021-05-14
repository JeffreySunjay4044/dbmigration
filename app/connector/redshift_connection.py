import os
from typing import NamedTuple, Optional
import redshift_connector
import psycopg2
from singleton_decorator import singleton


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
        database: Optional[str] = None
) -> ConnInfo:
    """
    Parse arguments and return connection info for Redshift
    """
    return ConnInfo(
        user=user or os.environ["ANALYTICS_DB_USER"],
        password=password or os.environ["ANALYTICS_DB_PASSWORD"],
        host=host or os.environ["ANALYTICS_DB_HOST"],
        database=database or os.environ["ANALYTICS_DB_NAME"]
    )


@singleton
class RedshiftConnection:
    def __init__(self, conn_info):
        self.conn_info = conn_info

    def get_client(self):
        conn = psycopg2.connect(
            host=self.conn_info.host,
            port=5432,
            database=self.conn_info.database,
            user=self.conn_info.user,
            password=self.conn_info.password
        )
        return conn


def push_to_redshift(db, sql_query, is_result_needed):
    conn_info = build_conn_info(
        host='redshift',
        database=db,
        user='postgres',
        password='debezium'
    )
    print(f"conn info is {conn_info}")
    connection = RedshiftConnection(conn_info).get_client()
    cursor: redshift_connector.Cursor = connection.cursor()
    cursor.execute(sql_query)
    if is_result_needed is not None:
        if is_result_needed is True:
            result: tuple = cursor.fetchall()
            print(f"Result after insert {result}")
            return result
        else:
            connection.commit()

