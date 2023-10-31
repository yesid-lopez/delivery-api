APP = delivery_api

DC = docker compose $(addprefix -f ,$(DC_FILES))
DC_FILES = docker-compose.yml

BUILD = docker build
DOCKER_RUN = docker run --rm --interactive --tty
DC_EXEC = $(DC) exec

RUN_APP = $(DOCKER_RUN) \
			--volume '$(PWD)/delivery_api:/app/delivery_api' \
			--volume '$(PWD)/.pylintrc:/app/.pylintrc' \
			--volume '$(PWD)/tests:/app/tests' \
			delivery-api:dev

###################
## Docker Images ##
###################

all: app-dev app-prod cache-runner

app-%:
	$(BUILD) -t 'delivery-api:$*' --target '$*' .

cache-runner:
	$(BUILD) -t cache-runner:latest cache_utils

#################
## code style ##
################

type-check:
	$(RUN_APP) mypy $(APP)

lint:
	$(RUN_APP) flake8 $(APP)
	$(RUN_APP) pylint --rcfile=.pylintrc $(APP)


###########
## tests ##
###########

unit-test:
	$(RUN_APP) pytest tests

###########
## utils ##
###########

seed_redis:
	$(DC_EXEC) cache_runner python insert_venue_preparation.py

#################################
## Docker-Compose Environments ##
#################################

run-dev: DC_FILES += docker-compose.dev.yml
run-dev:
	$(DC) up

down:
	$(DC) down --volumes