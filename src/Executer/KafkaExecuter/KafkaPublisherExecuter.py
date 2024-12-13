from ..Executer import Executer
from multiprocessing import Queue
from kafka import KafkaProducer

class KafkaPublisherExecuter(Executer):

    def __init__(self, size_msg = 1, size_list = 1, incremental = False, num_execs = 10, directory_name = "", file_name = "", topic = "example-topic", separator = ";", decimal = "."):
        super().__init__(size_msg, size_list, incremental, num_execs, directory_name, file_name, topic, separator, decimal)

    def execute(self, queue: Queue):

        producer = KafkaProducer(bootstrap_servers='localhost:9092')

        super().execute(queue,)
        
        for msg in self.data:
            producer.send('example-topic', msg.encode('UTF-8'))
        
        producer.flush()
        return