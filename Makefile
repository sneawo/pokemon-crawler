help: ## show this help
	@echo 'usage: make [target] ...'
	@echo ''
	@echo 'targets:'
	@egrep '^(.+)\:\ .*##\ (.+)' ${MAKEFILE_LIST} | sed 's/:.*##/#/' | column -t -c 2 -s '#'

migrate: ## migrate db
	docker-compose run --rm web python manage.py migrate

lint: ## migrate db
	docker-compose run --rm web flake8 app
	docker-compose run --rm web mypy --ignore-missing-imports --follow-imports=silent app
