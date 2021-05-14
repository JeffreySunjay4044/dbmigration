purge_restart_docker:
	sh scripts/deploy_debezium_local.sh

app_consumer_run:
	pipenv run python app/main.py --log=INFO --reload

app_consumer_debug:
	pipenv debug python app/main.py --log=INFO --reload