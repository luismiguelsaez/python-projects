# Set DockerHUB user variable
DOCKERHUB_USER=luismiguelsaez
DOCKERHUB_IMAGE=fastapi-cache
DOCKERHUB_TAG=latest

PHONY: build push

build:
	docker build -t ${DOCKERHUB_USER}/${DOCKERHUB_IMAGE}:${DOCKERHUB_TAG} .

push:
	docker push ${DOCKERHUB_USER}/${DOCKERHUB_IMAGE}:${DOCKERHUB_TAG}

run:
	docker run --name fastapi-cache -d -p 8000:8000 -e CACHE_CONTROL="max-age=600, public" ${DOCKERHUB_USER}/${DOCKERHUB_IMAGE}:${DOCKERHUB_TAG}

clean:
	docker rm -f fastapi-cache
