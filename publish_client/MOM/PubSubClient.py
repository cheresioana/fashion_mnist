from json import dumps

from google.cloud import pubsub_v1
from concurrent import futures
from publish_client.MOM.MOMInterface import MOMInterface
import publish_client.config as cfg


class PubSubClient(MOMInterface):
    def __init__(self):
        self.publish_futures = []
        self.subscriber = None
        self.publisher = None
        self.project_id = cfg.gcp_project_id

    def __create_producer(self):
        self.publisher = pubsub_v1.PublisherClient()

    def __get_topic(self, topic):
        """Check if the topic exists. If not, create it"""
        project_path = f"projects/{self.project_id}"
        found = False
        topic_name = 'projects/%s/topics/%s' % (self.project_id, topic)
        for existing_topic in self.publisher.list_topics(request={"project": project_path}):
            if existing_topic.name == topic_name:
                found = True
        if not found:
            self.publisher.create_topic(name=topic_name)
        else:
            self.publisher.topic_path(self.project_id, topic)

    def __create_consumer(self, topic):
        self.subscriber = pubsub_v1.SubscriberClient()

    def send_message(self, message, topic="client"):
        """send a message to the message queue"""
        topic_name = 'projects/%s/topics/%s' % (self.project_id, topic)
        if self.publisher is None:
            self.__create_producer()
            self.__get_topic(topic)
        binary_message = bytes(dumps(message).encode('utf-8'))
        publish_future = self.publisher.publish(topic_name, binary_message)
        self.publish_futures.append(publish_future)
        return publish_future

    def receive_message(self, message_callback, topic="client", subscription_id="client0"):
        """receive a message from the message queue"""
        if self.subscriber is None:
            self.__create_consumer(topic)

        subscription_path = self.subscriber.subscription_path(self.project_id, subscription_id)
        streaming_pull_future = self.subscriber.subscribe(
            subscription_path, callback=message_callback
        )
        print(f"Listening for messages on {subscription_path}..\n")
        try:
            streaming_pull_future.result()
        except:
            streaming_pull_future.cancel()  # Trigger the shutdown.
            streaming_pull_future.result()  # Block until the shutdown is complete.

        self.subscriber.close()

    def wait_publishing_operations(self):
        # wait for all the publishing to be completed
        futures.wait(self.publish_futures, return_when=futures.ALL_COMPLETED)
