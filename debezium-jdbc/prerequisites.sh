#!/bin/bash
url='http://connect:8083/connectors'
status_code=$(curl --write-out %{http_code} --silent --output /dev/null url)

if [[ "$status_code" -ne 200 ]] ; then
  echo "Site status changed to $status_code" | curl -X PUT \
  http://connect:8083/connectors/source-connector-test/config \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'Postman-Token: 8bafbc79-6cef-471a-b26c-8a15a009ec11' \
  -H 'cache-control: no-cache' \
  # shellcheck disable=SC2016
  -d ' { "connector.class": "io.debezium.connector.mysql.MySqlConnector",
   "tasks.max": "1", "database.hostname": "mysql", "database.port": "3306",
  "database.user": "debezium", "database.server.id": "184054",
  "database.password": "dbz", "database.server.name": "mysql",
  "database.include.list": "inventory", "database.history.kafka.bootstrap.servers": "kafka:9092",
  "database.history.kafka.topic": "dbhistory.inventory",
  "name":"product-connector-test","transforms": "route",
  "transforms.route.type": "org.apache.kafka.connect.transforms.RegexRouter",
  "transforms.route.regex": "([^.]+)\\.([^.]+)\\.([^.]+)",
  "transforms.route.replacement": "$3" }'
else
  exit 0
fi


