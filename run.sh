#!/bin/bash

NETWORK=test-network

init_network(){
    docker network inspect "$NETWORK" >/dev/null 2>&1 || docker network create $NETWORK
}

db(){
    init_network;

    docker run \
        --rm \
        -d \
        --network $NETWORK \
        -p 5432:5432 \
        --env-file .env \
        -v test-pg:/var/lib/postgresql \
        --name test_postgres \
        postgres:19rc1-alpine
}

build_dev(){
    docker build -t pdb:dev --target dev .
}

dev(){
    init_network;
    docker run \
        --rm \
        --env-file .env \
        --network $NETWORK \
        -p 8000:8000 \
        -v "${PWD}":/app \
        --name run_dev \
        pdb:dev
}

build_prod(){
    docker build -t pdb:prod --target prod .
}

prod(){
    init_network;
    docker run \
        --rm \
        --env-file .env \
        --network $NETWORK \
        -p 8000:8000 \
        --name run_prod \
        pdb:prod
}

$@