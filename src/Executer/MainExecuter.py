
from timeit import default_timer as timer
from multiprocessing import Process, Queue
from Executer import Executer


class MainExecuter(Executer):

    subscriber: Executer
    publisher: Executer

    def __init__(self, size_msg=1, size_list=1, incremental=False, num_execs=10, directory_name="", file_name="", topic="example-topic", separator=";", decimal=".", subscriber: Executer = Executer(), publisher: Executer= Executer()):
        super().__init__(size_msg, size_list, incremental, num_execs,
                         directory_name, file_name, topic, separator, decimal)
        
        self.subscriber = subscriber
        self.publisher = publisher


        publisher.generate_data()

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

        subscriber_process = Process(target=self.subscriber.iterate)
        publisher_process = Process(target=self.publisher.iterate)

        super().execute(queue,)

        subscriber_process.start()
        publisher_process.start()

        subscriber_process.join()
        publisher_process.join()
