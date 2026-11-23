#!/bin/bash

NETWORK=test-network

init_network(){
    docker network inspect "$NETWORK" >/dev/null 2>&1 || docker network create $NETWORK
}

run_db(){
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
    docker build -t pdb --target dev .
}

run_dev(){
    init_network;
    docker run \
        --rm \
        --env-file .env \
        --network $NETWORK \
        -p 8000:8000 \
        -v "${PWD}":/app \
        --name run_dev \
        pdb
}
        # -e WATCHFILES_FORCE_POLLING=true \
$@