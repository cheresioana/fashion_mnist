import argparse
from json import dumps, loads
import time

from image_classifier.utils.load_mnist import load_mnist
import sys

from publish_client.MOM.KafkaClient import KafkaClient
from publish_client.MOM.PubSubClient import PubSubClient

config = {
    "test_images": "image_classifier/data/fashion/t10k-images-idx3-ubyte.gz",
    "test_labels": "image_classifier/data/fashion/t10k-labels-idx1-ubyte.gz",
}


def on_send_success(record_metadata):
    print("Message has been sent successfully %s" % record_metadata)


def on_send_error(excp):
    print("this is an error in sending the message: %s" % excp)


def kafka_callback(message):
    print("message received kafka")
    print(message)


if __name__ == '__main__':
    print("enters the client")
    parser = argparse.ArgumentParser(description='Optional app description')
    parser.add_argument('--mom_client', type=str,
                        help='it can either be kafka or pubsub; by default the system takes pubsub')
    parser.add_argument('--run_local', type=str,
                        help='run local or from docker')
    args = parser.parse_args()
    # wait for kafka
    time.sleep(5)
    topic = "client"

    if args.run_local == 'True':
        ip = 'localhost:19092'
    else:
        ip = 'broker:9092'

    if args.mom_client == 'kafka':
        print("Sending messages through Kafka ip %s"%ip)
        mom = KafkaClient()
        mom.set_ip(ip)
    else:
        print("Sending messages through PubSub")
        mom = PubSubClient()
    x_valid, y_valid = load_mnist(config["test_images"], config["test_labels"])
    for idx in range(0, 10):
        to_send_data = x_valid[idx]
        print("Send array of bytes that match the %d entry form the validation" % idx)
        mom.send_message({'id': idx, 'img': to_send_data.tolist()})
        time.sleep(2)

    # block until all async messages are sent
    mom.wait_publishing_operations()
