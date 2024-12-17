import argparse
import pandas
import os
from matplotlib import pyplot as plt
import numpy as np


def general_plot_comparision(kafka_df: pandas.DataFrame, rabbitmq_df: pandas.DataFrame,
                             graphs_directory: str, graph_name: str, graph_title: str):

    plt.plot(kafka_df['size_msg'], kafka_df['time'])

    plt.plot(rabbitmq_df['size_msg'], rabbitmq_df['time'])

    plt.legend(['kafka', 'rabbit'])

    plt.title(graph_title)
    plt.xlabel("size of msg (characters)")
    plt.ylabel("time of execution (seconds)")

    plt.savefig(graphs_directory+graph_name)
    plt.close()


def generate_main_graphs(kafka_df: pandas.DataFrame, rabbitmq_df: pandas.DataFrame, graphs_directory: str,
                         non_incremental_name: str, non_incremental_title: str, incremental_name: str, incremental_title: str):

    kafka_aux = kafka_df[kafka_df['incremental'] == False]
    rabbitmq_aux = rabbitmq_df[rabbitmq_df['incremental'] == False]

    kafka_aux.loc[:, 'time'] = kafka_aux['time']/kafka_aux['num_execs']
    rabbitmq_aux.loc[:, 'time'] = rabbitmq_aux['time'] / \
        rabbitmq_aux['num_execs']

    general_plot_comparision(kafka_aux, rabbitmq_aux,
                             graphs_directory, non_incremental_name, non_incremental_title)

    kafka_aux = kafka_df[kafka_df['incremental'] == True]
    rabbitmq_aux = rabbitmq_df[rabbitmq_df['incremental'] == True]

    kafka_aux.loc[:, 'time'] = kafka_aux['time']/kafka_aux['num_execs']
    rabbitmq_aux.loc[:, 'time'] = rabbitmq_aux['time'] / \
        rabbitmq_aux['num_execs']

    general_plot_comparision(kafka_aux, rabbitmq_aux,
                             graphs_directory, incremental_name, incremental_title)


def generate_sub_graphs(kafka_df: pandas.DataFrame, rabbitmq_df: pandas.DataFrame, graphs_directory: str,
                        non_incremental_name: str, non_incremental_title: str, incremental_name: str, incremental_title: str):

    kafka_aux = kafka_df[kafka_df['incremental'] == False]
    rabbitmq_aux = rabbitmq_df[rabbitmq_df['incremental'] == False]

    kafka_aux = pandas.DataFrame(kafka_aux.groupby(["size_msg"]).apply(lambda x: x['time'].mean(),
                                                                       include_groups=False))
    kafka_aux = kafka_aux.reset_index()
    kafka_aux = kafka_aux.rename(columns={0: "time"})

    rabbitmq_aux = pandas.DataFrame(rabbitmq_aux.groupby(["size_msg"]).apply(lambda x: x['time'].mean(),
                                                                             include_groups=False))
    rabbitmq_aux = rabbitmq_aux.reset_index()
    rabbitmq_aux = rabbitmq_aux.rename(columns={0: "time"})


    general_plot_comparision(kafka_aux, rabbitmq_aux,
                             graphs_directory, non_incremental_name, non_incremental_title)

    kafka_aux = kafka_df[kafka_df['incremental'] == True]
    rabbitmq_aux = rabbitmq_df[rabbitmq_df['incremental'] == True]

    kafka_aux = pandas.DataFrame(kafka_aux.groupby(["size_msg"]).apply(lambda x: x['time'].mean(),
                                                                       include_groups=False))
    kafka_aux = kafka_aux.reset_index()
    kafka_aux = kafka_aux.rename(columns={0: "time"})

    rabbitmq_aux = pandas.DataFrame(rabbitmq_aux.groupby(["size_msg"]).apply(lambda x: x['time'].mean(),
                                                                             include_groups=False))
    rabbitmq_aux = rabbitmq_aux.reset_index()
    rabbitmq_aux = rabbitmq_aux.rename(columns={0: "time"})

    general_plot_comparision(kafka_aux, rabbitmq_aux,
                             graphs_directory, incremental_name, incremental_title)


def main(data_directory: str = "data/", separator: str = ";", decimal: str = ".", graphs_directory: str = "graphs/"):

    kafka_main = "KafkaExecuter.csv"
    kafka_subscriber = "KafkaExecuter_subscriber.csv"
    kafka_publisher = "KafkaExecuter_publisher.csv"
    rabbitmq_main = "RabbitMQExecuter.csv"
    rabbitmq_subscriber = "RabbitMQExecuter_subscriber.csv"
    rabbitmq_publisher = "RabbitMQExecuter_publisher.csv"

    col_types = {'execution_num': np.int64, "num_execs": np.int64, "size_msg": np.int64,
                 "incremental": np.bool, "time": np.float128}

    kafka_df = pandas.read_csv(
        data_directory+kafka_main, sep=separator, decimal=decimal, dtype=col_types)
    rabbitmq_df = pandas.read_csv(
        data_directory+rabbitmq_main, sep=separator, decimal=decimal, dtype=col_types)

    kafka_df_subscriber = pandas.read_csv(
        data_directory+kafka_subscriber, sep=separator, decimal=decimal, dtype=col_types)
    kafka_df_publisher = pandas.read_csv(
        data_directory+kafka_publisher, sep=separator, decimal=decimal, dtype=col_types)

    rabbitmq_df_subscriber = pandas.read_csv(
        data_directory+rabbitmq_subscriber, sep=separator, decimal=decimal, dtype=col_types)
    rabbitmq_df_publisher = pandas.read_csv(
        data_directory+rabbitmq_publisher, sep=separator, decimal=decimal, dtype=col_types)

    generate_main_graphs(kafka_df, rabbitmq_df, graphs_directory, "general_execution_not_incremental.png",
                         "Main Kafka vs RabbitMQ no incremental size", "general_execution_incremental.png",
                         "Main Kafka vs RabbitMQ incremental size")

    generate_sub_graphs(
        kafka_df_subscriber, rabbitmq_df_subscriber, graphs_directory, "subscriber_execution_not_incremental.png",
        "Kafka vs RabbitMQ subscriber no incremental size", "subscriber_execution_incremental.png",
        "Kafka vs RabbitMQ subscriber incremental size")

    generate_sub_graphs(
        kafka_df_publisher, rabbitmq_df_publisher, graphs_directory, "publisher_execution_not_incremental.png",
        "Kafka vs RabbitMQ publisher no incremental size", "publisher_execution_incremental.png",
        "Kafka vs RabbitMQ publisher incremental size")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Generates the graphs for the comparison')

    parser.add_argument('-dd', '--data-directory',
                        default="data/",
                        help='data directory')

    parser.add_argument('-s', '--separator',
                        default=";",
                        help='separator for the data csv')

    parser.add_argument('-d', '--decimal',
                        default=".",
                        help='decimal for the data csv')

    parser.add_argument('-gd', '--graphs-directory',
                        default="graphs/",
                        help='graphs directory')

    args = parser.parse_args()

    if not os.path.exists(args.data_directory):
        print("Data directory don't exist")
        exit()

    if not os.path.exists(args.graphs_directory):
        os.makedirs(args.graphs_directory)

    main(data_directory=args.data_directory,
         separator=args.separator, decimal=args.decimal,
         graphs_directory=args.graphs_directory)
