
from kafka import KafkaProducer, TopicPartition
from kafka import KafkaConsumer
from json import dumps, loads

from publish_client.MOM.MOMInterface import MOMInterface


class KafkaClient(MOMInterface):
    def __init__(self):
        self.consumer = None
        self.producer = None
        self.ip = None

    def set_ip(self, ip):
        self.ip = ip

    def __create_producer(self):
        self.producer = KafkaProducer(bootstrap_servers=[self.ip], api_version=(0, 10, 2),
                                      value_serializer=lambda x: dumps(x).encode('utf-8'))
        print(self.producer.config)

    def __create_consumer(self, topic):
        self.consumer = KafkaConsumer(topic, bootstrap_servers=[self.ip],
                                      auto_offset_reset='earliest',
                                      group_id=None,
                                      enable_auto_commit=True,
                                      api_version=(0, 10, 2),
                                      value_deserializer=lambda m: loads(m.decode('utf-8')))

    def send_message(self, message, topic="client"):
        """send a message to the message queue"""
        # if the producer is not initialized, initialize it
        if self.producer is None:
            self.__create_producer()

        # send the actual message and add callbacks on success and on failure
        self.producer.send(topic,
                           message)
        self.producer.flush()
        print('Message published successfully.')

    def receive_message(self, message_callback, topic="client"):
        """receive a message from the message queue"""
        # if there is no consumer create it
        if self.consumer is None:
            self.__create_consumer(topic)
        # call client function every time you receive a message
        print("listening for kafka message on topic %s"%topic)
        for message in self.consumer:
            message_callback(message)

    def wait_publishing_operations(self):
        # block until all async messages are sent
        if self.producer is not None:
            self.producer.flush()
