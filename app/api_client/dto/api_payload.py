import json
from string import Template


def sink_connector_payload(table_name, primary_key):
    payload_variable = Template('{ "name":$name,'
                                ' "connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector","tasks.max": "1","topics": $topics, "connection.url":"jdbc:postgresql://redshift:5432/inventory?user=postgres&password=debezium","transforms": "unwrap","transforms.unwrap.type": "io.debezium.transforms.ExtractNewRecordState",'
                                '"transforms.unwrap.drop.tombstones": "false","transforms.unwrap.delete.handling.mode":"none","auto.create": '
                                '"true", "auto.evolve": "true","insert.mode": "upsert","pk.fields": $primary_key,                                        '
                                '               "pk.mode": "record_key","delete.enabled": "true"} ')
    api_name = (f"{table_name}-sink-connector")
    payload_variable = payload_variable.substitute(name=api_name)
    payload_variable = payload_variable.substitute(primary_key=primary_key)
    payload_variable = payload_variable.substitute(topics=table_name)
    payload_api_json = json.loads(payload_variable)
    print(f"Expected json output is : {payload_api_json}")
    return payload_api_json
