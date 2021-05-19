# dbmigration
This pipeline is for change data capture at MySql and publishing it to Redshift is real-time.
It has around 5 components:
a. kafka
b. zookeeper
c. mysql instance to pull changelog data
d. redshift instance to push data
e. debezium connect

## Setup
```shell script
Install Python
Required python version: 3.7
Install python environment
pipenv install

Install docker
# Docker
```
## Run Locally
## Restart all containers
```shell script

make purge_restart_docker
    This deletes existing docker container for all components . It does a cleanup of all images 
    that was created in the last run and finally brings up all containers.

Once all containers are up and kafka connect is running.

To do for pulling data from mysql to redshift

1. Use kafka connect api to add a mysql source which configures kafka-connect to analyse the changelog and push the 
   changes in to kafka-topic. Refer requests/requests.http first 
2. Use kafka connect api to add a postgres sink which configures kafka-connect to impart the changes in to postgres 
   based on the changes in the kafka-topic. Refer requests/requests.http second
3. Login to mysql host and try an alter table query , make sure the table that is altered has the sink
   connector(refer point 2) running on it.

## Restart specific containers

make purge_restart_docker container_name={container_name} : refer from docker-compose.
    This will restart the docker container with the above container name. It follows the same procedure
    deleting the old image and container and spins up a new one.

```

### Supported DDL Operations
```
ALTER TABLE : 
1. Make sure ddlconsumerinventory container is running and listening to dbhistory.inventory. This is the topic 
that houses all ddl CDC. 
2. For testing alter, login to mysql instance and perform ALTER Table add or drop column and you should be
able to see the changes in redshift

DROP TABLE:
1. For testing out drop table scenario, Please call the request/http 3rd api.
2. Login to mysql and drop a table and you will find the changes reflected in redshift.


```


## Architecture diagram
```
https://lucid.app/lucidchart/invitations/accept/inv_43e9b0b5-202e-493d-adb5-d3c8191987ba?viewport_loc=-3%2C-118%2C1292%2C735%2C0_0
```

## Building and Publishing Project
This will build a docker image and push to ECR.

## TODO
- [x] Unit Tests
- [x] Make documentation available to clients

# References
**Debezium documentation**
https://debezium.io/documentation/reference/1.5/tutorial.html


##Docker commands
Kafka consumer terminal commands:
./bin/kafka-console-consumer.sh --topic mysql.inventory.products --bootstrap-server kafka:9092 --from-beginning
