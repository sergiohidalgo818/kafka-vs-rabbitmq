from ..Executer import Executer
from multiprocessing import Queue
import pika

class RabbitMQPublisherExecuter(Executer):

    def __init__(self, size_msg = 1, size_list = 1, incremental = False, num_execs = 10, directory_name = "", file_name = "", topic = "example-topic", separator = ";", decimal = "."):
        super().__init__(size_msg, size_list, incremental, num_execs, directory_name, file_name, topic, separator, decimal)

    def execute(self, queue: Queue):

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.exchange_declare(exchange='topic_logs', exchange_type='topic')
       
        channel.confirm_delivery()

        super().execute(queue,)
        
        for msg in self.data:
            channel.basic_publish(exchange='topic_logs',
                              routing_key=self.topic, body=msg.encode('UTF-8'))
       
        connection.close()