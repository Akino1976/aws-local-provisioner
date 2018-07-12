REPOSITORY := aws-local-provisioner
CURRENT_DATE := $(shell echo `date +'%Y-%m-%d'`)
VERSION ?= $(CURRENT_DATE)
ARTIFACTORY_URL := bambora-dkr.jfrog.io
TEST_VERSION := commit_$(shell git rev-parse --short HEAD)

export CURRENT_DATE
export VERSION
export TEST_VERSION

build-provisioner:
	docker build \
		-t aws-local-provisioner:latest \
		-t aws-local-provisioner:$(VERSION) \
		-t $(ARTIFACTORY_URL)/aws-local-provisioner:latest \
		-t $(ARTIFACTORY_URL)/aws-local-provisioner:$(VERSION) \
		provisioner

run-provisioner: build-provisioner
	docker-compose run --rm provisioner

run-moto-provisioner: build-provisioner build-moto-aws-mock
	docker-compose run --rm moto-provisioner

build-moto-aws-mock:
	docker-compose build moto-aws-mock
