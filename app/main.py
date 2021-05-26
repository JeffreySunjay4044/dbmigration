from connector import stream_connection
from query_process.metadata import type_metadata

if __name__ == '__main__':
    ## Starting the kafka consumer to pull ddl records
    stream_connection.start_consumer()
    # print(type_metadata.convert_query('ALTER TABLE products MODIFY COLUMN rating DOUBLE'))

    ####
