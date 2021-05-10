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
```Install Python```
Required python version: 3.7
Install python environment
pipenv install

Install docker
# Docker
```
## Run Locally
```shell script
docker-compose up.
Docker compose up brings up all containers 
Once all containers are up and kafka connect is running.

To do for pulling data from mysql to redshift

1. Use kafka connect api to add a mysql source which configures kafka-connect to analyse the changelog and push the 
   changes in to kafka-topic. Refer requests/requests.http first 
2. Use kafka connect api to add a postgres sink which configures kafka-connect to impart the changes in to postgres 
   based on the changes in the kafka-topic. Refer requests/requests.http second

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
