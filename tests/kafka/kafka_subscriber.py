#!/usr/bin/env python
from kafka import KafkaConsumer
consumer = KafkaConsumer('example-topic')
for msg in consumer:
    print (msg)
    print (msg.value.decode('UTF-8'))

