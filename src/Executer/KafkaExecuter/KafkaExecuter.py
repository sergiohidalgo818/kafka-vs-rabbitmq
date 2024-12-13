from ..MainExecuter import MainExecuter
from multiprocessing import Queue
from .KafkaSubscriberExecuter import KafkaSubscriberExecuter
from .KafkaPublisherExecuter import KafkaPublisherExecuter
from kafka.admin import KafkaAdminClient, NewTopic


class KafkaExecuter(MainExecuter):

    def __init__(self, size_msg: int = 1, size_list: int = 1, incremental: bool = False, num_execs: int = 10,
                 directory_name: str = "", file_name: str = "", topic: str = "example-topic", separator: str = ";",
                 decimal: str = "."):

        subscriber = KafkaSubscriberExecuter(size_msg=size_msg, size_list=size_list, num_execs=num_execs,
                                             incremental=incremental, directory_name=directory_name,
                                             file_name=str(file_name.split(
                                                 ".")[0]+"_subscriber.csv"),
                                             topic=topic, separator=separator, decimal=decimal)

        publisher = KafkaPublisherExecuter(size_msg=size_msg, size_list=size_list, num_execs=num_execs,
                                           incremental=incremental, directory_name=directory_name,
                                           file_name=str(file_name.split(
                                               ".")[0]+"_publisher.csv"),
                                           topic=topic, separator=separator, decimal=decimal)

        super().__init__(size_msg, size_list, incremental, num_execs, directory_name,
                         file_name, topic, separator, decimal, subscriber, publisher)

    def execute(self, queue: Queue):
        admin_client = KafkaAdminClient(bootstrap_servers='localhost:9092')

        topic_list = []
        topic_list.append(NewTopic(name="example-topic",
                          num_partitions=1, replication_factor=1))

        try:
            admin_client.create_topics(
                new_topics=topic_list, validate_only=False)
        except:
            pass

        return super().execute(queue)
