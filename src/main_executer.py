import argparse
from Executer import KafkaExecuter
from Executer import RabbitMQExecuter


def main(execution: str,  message_size: int,
         iteration_size: int, incremental_message_size: bool,
         number_iterations: int, data_directory: str, file_indicator: str,
         separator: str, decimal: str):

    match execution:
        case 'kafka':
            kfk_exec = KafkaExecuter(size_msg=message_size, size_list=iteration_size,
                                     incremental=incremental_message_size, num_execs=number_iterations,
                                     directory_name=data_directory,
                                     file_name=f"KafkaExecuter{file_indicator}.csv",
                                     separator=separator, decimal=decimal)

            kfk_exec.iterate()

        case 'rabbitmq':
            rbmq_exec = RabbitMQExecuter(size_msg=message_size, size_list=iteration_size,
                                         incremental=incremental_message_size, num_execs=number_iterations,
                                         directory_name=data_directory,
                                         file_name=f"RabbitMQExecuter{file_indicator}.csv",
                                         separator=separator, decimal=decimal)

            rbmq_exec.iterate()

        case 'both':
            kfk_exec = KafkaExecuter(size_msg=message_size, size_list=iteration_size,
                                     incremental=incremental_message_size, num_execs=number_iterations,
                                     directory_name=data_directory,
                                     file_name=f"KafkaExecuter{file_indicator}.csv",
                                     separator=separator, decimal=decimal)

            kfk_exec.iterate()

            rbmq_exec = RabbitMQExecuter(size_msg=message_size, size_list=iteration_size,
                                         incremental=incremental_message_size, num_execs=number_iterations,
                                         directory_name=data_directory,
                                         file_name=f"RabbitMQExecuter{file_indicator}.csv",
                                         separator=separator, decimal=decimal)

            rbmq_exec.iterate()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Executes the different routines for testing performance')
    parser.add_argument('-e', '--execution',
                        default='both',
                        choices=['kafka', 'rabbitmq', 'both'],
                        help='executes servers, storage, or both (default: %(default)s)')

    parser.add_argument('-ms', '--message-size',
                        default=100,
                        help='size of each message')

    parser.add_argument('-is', '--iteration-size',
                        default=10,
                        help='number of iterations in the execution')

    parser.add_argument('-ims', "--incremental-message-size", action="store_true",
                        default=False, help="makes message size incremental (starts in one ends in message-size)")

    parser.add_argument('-ni', '--number-iterations',
                        default=100,
                        help='number of iterations for each execution')

    parser.add_argument('-dd', '--data-directory',
                        default="data/",
                        help='data directory')

    parser.add_argument('-fi', '--file-indicator',
                        default="",
                        help='extra indicator to file')

    parser.add_argument('-s', '--separator',
                        default=";",
                        help='separator for the data csv')

    parser.add_argument('-d', '--decimal',
                        default=".",
                        help='decimal for the data csv')

    args = parser.parse_args()

    main(execution=args.execution,  message_size=int(args.message_size),
         iteration_size=int(args.iteration_size), incremental_message_size=bool(args.incremental_message_size),
         number_iterations=int(args.number_iterations), data_directory=args.data_directory,
         file_indicator=args.file_indicator, separator=args.separator,decimal=args.decimal)
