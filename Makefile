#!make

include Envfile
export $(shell sed 's/=.*//' Envfile)

.PHONY: help
help:
	@echo "Available actions:"
	@echo "  build-container      Build $(REGISTRY_NAME)/$(IMAGE_NAME):$(IMAGE_TAG) docker container image"
	@echo "  push-container       Publish $(REGISTRY_NAME)/$(IMAGE_NAME):$(IMAGE_TAG) docker container image"

.PHONY: all
all: build-container push-container

.PHONY: build-container
build-container:
	@docker run -it --rm=true -v $$(pwd):/source -v /var/lib/containers:/var/lib/containers -v /var/run/docker.sock:/var/run/docker.sock -e SOURCE_PATH="/source" -e BUILD_ARGS=$(BUILD_ARGS) -e REGISTRY_NAME="$(REGISTRY_NAME)" -e IMAGE_NAME="$(IMAGE_NAME)" -e IMAGE_TAG="$(IMAGE_TAG)" cznewt/container-tools:latest docker-build-container
	@docker run -it --rm=true -v $$(pwd):/source -v /var/lib/containers:/var/lib/containers -v /var/run/docker.sock:/var/run/docker.sock -e SOURCE_PATH="/source" -e REGISTRY_NAME="$(REGISTRY_NAME)" -e IMAGE_NAME="$(IMAGE_NAME)" -e IMAGE_TAG="$(IMAGE_TAG)" -e IMAGE_NEW_TAG="latest" cznewt/container-tools:latest docker-tag-container

.PHONY: push-container
push-container:
	@docker run -it --rm=true -v $$(pwd):/source -v /var/lib/containers:/var/lib/containers -v /var/run/docker.sock:/var/run/docker.sock -e SOURCE_PATH="/source" -e REGISTRY_NAME="$(REGISTRY_NAME)" -e REGISTRY_AUTH_CONFIG="$$(cat ~/.docker/config.json)" -e IMAGE_NAME="$(IMAGE_NAME)" -e IMAGE_TAG="$(IMAGE_TAG)" cznewt/container-tools:latest docker-push-container
	@docker run -it --rm=true -v $$(pwd):/source -v /var/lib/containers:/var/lib/containers -v /var/run/docker.sock:/var/run/docker.sock -e SOURCE_PATH="/source" -e REGISTRY_NAME="$(REGISTRY_NAME)" -e REGISTRY_AUTH_CONFIG="$$(cat ~/.docker/config.json)" -e IMAGE_NAME="$(IMAGE_NAME)" -e IMAGE_TAG="latest" cznewt/container-tools:latest docker-push-container
