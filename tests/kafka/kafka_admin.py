#!/usr/bin/env python
from kafka.admin import KafkaAdminClient, NewTopic


admin_client = KafkaAdminClient( bootstrap_servers='localhost:9092')

topic_list = []
topic_list.append(NewTopic(name="example-topic", num_partitions=1, replication_factor=1))
admin_client.create_topics(new_topics=topic_list, validate_only=False)