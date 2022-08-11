#!/bin/bash

DOCKER_VOLUME=oilpalm-volume

if ! docker volume inspect $DOCKER_VOLUME 2>/dev/null 1>/dev/null;then
    echo "Creating $DOCKER_VOLUME docker volume"
    docker volume create $DOCKER_VOLUME
else
    echo "Volume $DOCKER_VOLUME exists"
    echo "Proceed running POSTGRES docker"
fi


docker run -it \
	--name oilpalm-pg\
	--rm \
	-e POSTGRES_USER="root" \
	-e POSTGRES_PASSWORD="root" \
	-e POSTGRES_DB="oilpalm-db" \
	-v $DOCKER_VOLUME:/var/lib/postgresql/data \
	-p 5432:5432 \
	postgres

