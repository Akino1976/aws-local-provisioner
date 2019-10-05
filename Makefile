REPOSITORY := aws-local-provisioner
CURRENT_DATE := $(shell echo `date +'%Y-%m-%d'`)
VERSION ?= $(CURRENT_DATE)
GITHUB_URL := https://github.com/akino1976/aws-local-provisioner.git
TEST_VERSION := commit_$(shell git rev-parse --short HEAD)

export CURRENT_DATE
export VERSION
export TEST_VERSION

build-provisioner:
	docker build\
		-t aws-local-provisioner:latest \
		-t aws-local-provisioner:$(VERSION) \
		provisioner

run-provisioner: build-provisioner
	docker-compose run --rm provisioner

run-moto-provisioner: build-provisioner build-moto-aws-mock
	docker-compose run --rm moto-provisioner

build-moto-aws-mock:
	docker-compose build moto-aws-mock

stop-all-containers:
	docker ps -q | xargs -I@ docker kill @

clear-all-containers: stop-all-containers
	docker ps -aq | xargs -I@ docker rm @

clear-volumes: clear-all-containers
	docker volume ls -q | xargs -I@ docker volume rm @

clear-images: clear-volumes
	docker images -q | uniq | xargs -I@ docker rmi -f @

date:
	@echo $(CURRENT_DATE)

version:
	@echo ${VERSION}
