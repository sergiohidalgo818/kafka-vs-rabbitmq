from ..Executer import Executer
from multiprocessing import Process, Queue
from .RabbitMQSubscriberExecuter import RabbitMQSubscriberExecuter
from .RabbitMQPublisherExecuter import RabbitMQPublisherExecuter
from timeit import default_timer as timer
from ..MainExecuter import MainExecuter


class RabbitMQExecuter(MainExecuter):

    def __init__(self, size_msg: int = 1, size_list: int = 1, incremental: bool = False, num_execs: int = 10,
                 directory_name: str = "", file_name: str = "", topic: str = "example-topic", separator: str = ";",
                 decimal: str = "."):
        subscriber = RabbitMQSubscriberExecuter(size_msg=size_msg, size_list=size_list, num_execs=num_execs,
                                             incremental=incremental, directory_name=directory_name,
                                             file_name=str(file_name.split(
                                                 ".")[0]+"_subscriber.csv"),
                                             topic=topic, separator=separator, decimal=decimal)

        publisher = RabbitMQPublisherExecuter(size_msg=size_msg, size_list=size_list, num_execs=num_execs,
                                           incremental=incremental, directory_name=directory_name,
                                           file_name=str(file_name.split(
                                               ".")[0]+"_publisher.csv"),
                                           topic=topic, separator=separator, decimal=decimal)

        super().__init__(size_msg, size_list, incremental, num_execs, directory_name,
                         file_name, topic, separator, decimal, subscriber, publisher)
