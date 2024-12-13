#!/bin/bash

# both

docker compose up -d
docker rm -f rabbitmq-broker

# only kafka

docker compose up -d
docker rm -f kafka-broker

# only rabbitmq

docker compose down