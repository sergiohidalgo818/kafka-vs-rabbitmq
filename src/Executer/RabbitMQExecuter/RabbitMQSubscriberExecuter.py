from ..Executer import Executer
from multiprocessing import Queue
import pika

class RabbitMQSubscriberExecuter(Executer):

    def __init__(self, size_msg = 1, size_list = 1, incremental = False, num_execs = 10, directory_name = "", file_name = "", topic = "example-topic", separator = ";", decimal = "."):
        super().__init__(size_msg, size_list, incremental, num_execs, directory_name, file_name, topic, separator, decimal)

    def execute(self, queue: Queue):
        
        super().execute(queue,)

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

        result = channel.queue_declare('', exclusive=True)
        queue_name = result.method.queue

            
        channel.queue_bind(
                exchange='topic_logs', queue=queue_name, routing_key=self.topic)



        def callback(ch, method, properties, body):
            if body.decode('UTF-8') == "$end":
                exit()
    


        channel.basic_consume(
            queue=queue_name, on_message_callback=callback, auto_ack=True)

        channel.start_consuming()