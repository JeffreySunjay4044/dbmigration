purge_restart_docker:
	sh scripts/deploy_debezium_local.sh

## To run this make container_name=ddlconsumerinventory purge_restart_containery
purge_restart_container:
	sh scripts/purge_restart_container.sh $(container_name)

app_consumer_run:
	pipenv run python app/main.py --log=INFO --reload

app_consumer_debug:
	pipenv debug python app/main.py --log=INFO --reload