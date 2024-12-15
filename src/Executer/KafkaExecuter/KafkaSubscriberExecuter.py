from ..Executer import Executer
from multiprocessing import Queue
from kafka import KafkaConsumer

class KafkaSubscriberExecuter(Executer):

    def __init__(self, size_msg = 1, size_list = 1, incremental = False, num_execs = 10, directory_name = "", file_name = "", topic = "example-topic", separator = ";", decimal = "."):
        super().__init__(size_msg, size_list, incremental, num_execs, directory_name, file_name, topic, separator, decimal)

    def execute(self, queue: Queue):
        consumer = KafkaConsumer('example-topic', auto_offset_reset='earliest')
        
        super().execute(queue,)

        for msg in consumer:
            if msg.value.decode('UTF-8') == "$end":
                break
