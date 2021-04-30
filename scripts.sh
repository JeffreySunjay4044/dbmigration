./bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --topic sundev --replication-factor 1 --partitions 3
#create topic with name from zookeeper connection

./bin/kafka-console-consumer.sh --topic sunjay-test-2 --from-beginning --bootstrap-server 127.0.0.1:9092


./bin/kafka-topics.sh --create --topic sundev--bootstrap-server localhost:9092

curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" localhost:8083/connectors/ -d '{ "name": "test-connector", "config": { "connector.class": "io.debezium.connector.mysql.MySqlConnector", "tasks.max": "1", "database.hostname": "localhost", "database.port": "3309", "database.user": "root", "database.password": "debezium", "database.server.id": "184054", "database.server.name": "mysql", "database.include.list": "test", "database.history.kafka.bootstrap.servers": "localhost:9092", "database.history.kafka.topic": "dbhistory.test" } }'


curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" localhost:8083/MySqlConnector/config/validate -d '{ "name": "test-connector", "config": { "connector.class": "io.debezium.connector.mysql.MySqlConnector", "tasks.max": "1", "database.hostname": "localhost", "database.port": "3309", "database.user": "root", "database.password": "debezium", "database.server.id": "184054", "database.server.name": "mysql", "database.include.list": "test", "database.history.kafka.bootstrap.servers": "localhost:9092", "database.history.kafka.topic": "dbhistory.test" } }'

curl -i -X PUT -H "Accept:application/json" -H "Content-Type:application/json" localhost:8083/connector-plugins/MySqlConnector/config/validate -d '{ "name": "test-connector", "config": { "connector.class": "io.debezium.connector.mysql.MySqlConnector", "tasks.max": "1", "database.hostname": "localhost", "database.port": "3309", "database.user": "root", "database.password": "debezium", "database.server.id": "184054", "database.server.name": "mysql", "database.include.list": "test", "database.history.kafka.bootstrap.servers": "localhost:9092", "database.history.kafka.topic": "dbhistory.test" } }'






0 row(s) affected, 2 warning(s): 1285 MySQL is started in --skip-name-resolve mode; you must restart it without this switch for this grant to work 1287 Using GRANT statement to modify existing user's properties other than privileges is deprecated and will be removed in future release. Use ALTER USER statement for this operation.

Error Code: 1133. Can't find any matching row in the user table
