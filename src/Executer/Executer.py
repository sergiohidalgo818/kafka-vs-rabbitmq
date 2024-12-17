
from timeit import default_timer as timer
from multiprocessing import Process, Queue
import os
import pandas
import numpy as np


class Executer:

    size_msg: int
    size_list: int
    incremental: bool
    data: list
    num_execs: int
    directory_name: str
    file_name: str
    separator: str
    decimal: str

    start_time: float
    end_time: float

    def __init__(self, size_msg: int = 1, size_list: int = 1, incremental: bool = False,
                 num_execs: int = 10, directory_name: str = "", file_name: str = "",
                 topic: str = "example-topic", separator: str = ";", decimal: str = "."):

        self.size_msg = size_msg
        self.size_list = size_list
        self.incremental = incremental

        self.num_execs = num_execs
        self.directory_name = directory_name
        self.file_name = file_name
        self.topic = topic

        self.separator = separator
        self.decimal = decimal
        

        self.data_frame = pandas.DataFrame({'execution_num': [], 'num_execs': [], 'size_msg': [],
                                            'incremental': [], 'time': []})


        self.data_frame['execution_num'] = self.data_frame['execution_num'].astype(np.int64)
        self.data_frame['num_execs'] = self.data_frame['num_execs'].astype(np.int64)
        self.data_frame['size_msg'] = self.data_frame['size_msg'].astype(np.int64)
        self.data_frame['incremental'] = self.data_frame['incremental'].astype(np.bool)
        self.data_frame['time'] = self.data_frame['time'].astype(np.float128)

    def execute(self, queue: Queue):
        queue.put(timer())

    def iterate(self):

        for execution_num in range(self.num_execs):
            queue = Queue()
            p = Process(target=self.execute, args=(queue,))
            p.start()
            p.join()

            self.start_time = queue.get()
            self.end_time = timer()

            self.add_to_frame(execution_num)

        self.write_data()

    def add_to_frame(self, execution_num: int):
        aux_df = pandas.DataFrame({'execution_num': [np.int64(execution_num)], 'num_execs': [np.int64(self.num_execs)],
                                   'size_msg': [np.int64(self.size_msg)], 'incremental': [np.bool(self.incremental)],
                                   'time': [np.float128(self.end_time-self.start_time)]})

        self.data_frame = pandas.concat(
            [self.data_frame, aux_df], ignore_index=True)

    def write_data(self):

        if not os.path.exists(self.directory_name):
            os.makedirs(self.directory_name)

        if os.path.exists(self.directory_name+self.file_name):

            aux_df = pandas.read_csv(self.directory_name+self.file_name, sep=self.separator,
                                     decimal=self.decimal)

            self.data_frame = pandas.concat(
                [aux_df, self.data_frame], ignore_index=True)

        self.data_frame.to_csv(
            self.directory_name+self.file_name, sep=self.separator, decimal=self.decimal, index=False)



    def generate_data(self):
        if not self.incremental:
            list_to_ret = [''.join([str(i) for i in range(self.size_msg)])
                        for _ in range(self.size_list)]

        else:
            list_to_ret = [''.join([str(i) for i in range(max(
                int(self.size_msg*list_index/self.size_list), 1))]) for list_index in range(1, self.size_list+1)]

        list_to_ret.append("$end")
        
        self.data= list_to_ret
