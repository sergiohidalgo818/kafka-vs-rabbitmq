#!/bin/bash

# both
docker compose up -d
sleep 3
echo "iterating with different message sizes on kafka"
# msg size
for i in {100..1000000..100000}
do
python3 src/main_executer.py -e kafka -ms $i
python3 src/main_executer.py -e kafka -ms $i -ims
done

echo "iterating with different message sizes on rabbitmq"
for i in {100..1000000..100000}
do
python3 src/main_executer.py -e rabbitmq -ms $i
python3 src/main_executer.py -e rabbitmq -ms $i -ims
done

# number of publishers

docker compose down
echo "finish"