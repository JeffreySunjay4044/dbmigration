docker-compose down
docker-compose rm
docker image rm dbmigration_redshift:latest -f
docker image rm dbmigration_connect:latest -f
docker image rm dbmigration_mysql:latest -f
docker-compose up