from connector import stream_connection

if __name__ == '__main__':
    ## Starting the kafka consumer to pull ddl records
    stream_connection.start_consumer()

