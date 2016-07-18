branch ?= master

virtualenv:
	virtualenv venv

deploy_prod:
	git push heroku-olark-slack ${branch}:master
