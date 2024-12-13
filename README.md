# kafka-vs-rabbitmq
Performance comparison between the two data-streaming platforms 

## Instalation and quick start
Here is explained step by step the installation of kafka and rabbitmq for Arch Linux with Docker.

### Docker
The following steps are subtracted from the [arch linux instalation guide](https://docs.docker.com/desktop/setup/install/linux/archlinux/) on the Docker docs.

#### Install docker client
```bash
wget https://download.docker.com/linux/static/stable/x86_64/docker-27.4.0.tgz -qO- | tar xvfz - docker/docker --strip-components=1
mv ./docker /usr/local/bin
```

#### Download lastest Arch package
It can be found on the [release notes](https://docs.docker.com/desktop/release-notes/)

```bash
wget https://desktop.docker.com/linux/main/amd64/178034/docker-desktop-x86_64.pkg.tar.zst -qO-
```

#### Install the package
```bash
sudo pacman -U ./docker-desktop-x86_64.pkg.tar.zst
```


### Kafka

#### Kafka image instalation and run

This steps can be found on [apache kafka docker docs](https://hub.docker.com/r/apache/kafka) 
To start the broker execute the following command (the image will be automatically pulled):

```bash
docker run -d --name kafka-broker apache/kafka:latest
```

But it can also be done from Docker Desktop.

#### Kafka testing

For testing the instalation 2 terminals are needed. One for the publisher and one for the subscriber.

For opening a terminal a broker terminal execute:
```bash
docker exec --workdir /opt/kafka/bin/ -it kafka-broker sh
```

For creating a topic execute this on one of the broker terminals:
```bash
./kafka-topics.sh --bootstrap-server localhost:9092 --create --topic example_topic
```

For the publisher, type in one of the terminals the following command:
```bash
./kafka-console-producer.sh --bootstrap-server localhost:9092 --topic test-topic
```


And then for the subscriber type this on the other:
```bash
./kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test-topic --from-beginning
```

As we write in the publisher terminal we should be seeing the same text on the subscriber one.


In the directory `tests/kafka` there are python scripts to check that all the installation is correct.


#### Kafka deleting

For deleting a topic execute this on a broker terminal:
```bash
./kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic test-topic
```

For deleting the container, type this on a normal terminal:
```bash
docker rm -f kafka-broker
```

### RabbitMQ
#### RabbitMQ image instalation and run
Like the previous case its only necesary to install the following command:
```bash
docker run -d --name rabbitmq-broker -p 5672:5672 -p 15672:15672 rabbitmq:3

```
#### RabbitMQ testing
The testing is inside the directory `tests/rabbitmq`.

In one terminal execute the subscriber:
```bash
python3 tests/rabbitmq/rabbitmq_subscriber.py "#"
```
In the other terminal execute the publisher:
```bash
python3 tests/rabbitmq/rabbitmq_publisher.py 
```
A `Hello World` should appear on the subscriber terminal.

#### Kafka deleting

Like Kafka, for deleting the container type:
```bash
docker rm -f rabbitmq-broker
```

### Using compose

On the base directory, execute the following command:
```bash
docker compose up -d
``` 
This will initialize both kafka and rabbitmq.

For removing the containers:
```bash
docker compose down
``` 

## Procedure




## Procedure
