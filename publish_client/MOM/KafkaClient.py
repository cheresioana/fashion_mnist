
from kafka import KafkaProducer
from kafka import KafkaConsumer
from json import dumps, loads

from publish_client.MOM.MOMInterface import MOMInterface


class KafkaMOM(MOMInterface):
    def __init__(self):
        self.consumer = None
        self.producer = None

    def create_producer(self):
        self.producer = KafkaProducer(bootstrap_servers='localhost:9092',
                                      value_serializer=lambda x: dumps(x).encode('utf-8'))

    def create_consumer(self, topic):
        self.consumer = KafkaConsumer(topic,
                                      value_deserializer=lambda m: loads(m.decode('utf-8')))

    def send_message(self, message, topic="client"):
        """send a message to the message queue"""
        # if the producer is not initialized, initialize it
        if self.producer is None:
            self.create_producer()

        # send the actual message and add callbacks on success and on failure
        self.producer.send(topic,
                           message) \
            .add_callback(self.on_send_success) \
            .add_errback(self.on_send_error)

    def on_send_success(self, record_metadata):
        print("Message has been sent successfully topic: %s partition %s offset %s " % (
            record_metadata.topic, record_metadata.partition, record_metadata.offset))

    def on_send_error(self, excp):
        print("this is an error in sending the message: %s" % excp)

    def receive_message(self, message_function, topic="client"):
        """receive a message from the message queue"""
        # if there is no consumer create it
        if self.consumer is None:
            self.create_consumer(topic)
        # call client function every time you receive a message
        for message in self.consumer:
            message_function(message)

    def wait_current_operations(self):
        # block until all async messages are sent
        if self.producer is not None:
            self.producer.flush()
