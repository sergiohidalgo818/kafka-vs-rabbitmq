from ..Executer import Executer
from multiprocessing import Process, Queue
from .KafkaSubscriberExecuter import KafkaSubscriberExecuter
from .KafkaPublisherExecuter import KafkaPublisherExecuter
from kafka.admin import KafkaAdminClient, NewTopic
from timeit import default_timer as timer

class KafkaExecuter(Executer):

    def __init__(self, size_msg = 1, size_list = 1, incremental = False, num_execs = 10, directory_name = "", file_name = "", topic = "example-topic", separator = ";", decimal = "."):
        super().__init__(size_msg, size_list, incremental, num_execs, directory_name, file_name, topic, separator, decimal)


    def iterate(self):

        for execution_num in range(1):
            queue = Queue()
            p = Process(target=self.execute, args=(queue,))
            p.start()
            p.join()

            self.start_time = queue.get()
            self.end_time = timer()

            self.add_to_frame(execution_num)

        self.write_data()

    def execute(self, queue: Queue):
        
        subscriber = KafkaSubscriberExecuter (size_msg = self.size_msg, size_list = self.size_list, num_execs = self.num_execs,
                                              incremental = self.incremental, directory_name = self.directory_name,
                                              file_name = str(self.file_name.split(".")[0]+"_subscriber.csv"),
                                              topic = self.topic, separator = self.separator, decimal = self.decimal)
        
        publisher = KafkaPublisherExecuter (size_msg = self.size_msg, size_list = self.size_list, num_execs = self.num_execs,
                                              incremental = self.incremental, directory_name = self.directory_name,
                                              file_name = str(self.file_name.split(".")[0]+"_publisher.csv"),
                                              topic = self.topic, separator = self.separator, decimal = self.decimal)

        subscriber_process = Process(target=subscriber.iterate)
        publisher_process = Process(target=publisher.iterate)
        
        admin_client = KafkaAdminClient( bootstrap_servers='localhost:9092')

        topic_list = []
        topic_list.append(NewTopic(name="example-topic", num_partitions=1, replication_factor=1))

        try:
          admin_client.create_topics(new_topics=topic_list, validate_only=False)
        except:
            pass
        
        super().execute(queue,)

        subscriber_process.start()
        publisher_process.start()

        subscriber_process.join()
        publisher_process.join()