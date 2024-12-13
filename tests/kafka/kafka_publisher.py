#!/usr/bin/env python
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:9092')
producer.send('example-topic', 'some_message_bytes'.encode('UTF-8'))
producer.flush()