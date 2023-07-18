SHELL := /bin/bash

export

# For the server, when we run from crontab we need to give the location
# of the docker-compose file
DC_PATH ?=

CURDATE_TIME=$(shell date +"%Y-%m-%d-%H-%M-%S")

export $(shell sed 's/=.*//' .env)

bash:
	docker-compose run --rm web /bin/bash