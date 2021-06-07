## Forward traffic from local to remote db endpoint like redshift

```
Debezium kafka connect does not suport data sink from to remote db.
Linux has long adapted this feature of port-forwarding, so enabling
portforwarding by adapting a http sink connector.
https://camel.apache.org/camel-kafka-connector/latest/connectors/camel-http-kafka-sink-connector.html

Expose a python api listening to above connector and making underlying 
redshift calls.

Flow is kafkaconnecr----http sink connector---------> python api ---forward to---->  redshift remote

kafka the python wau

```

