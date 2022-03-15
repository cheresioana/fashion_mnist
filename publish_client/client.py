import argparse
from json import dumps, loads
import time

from image_classifier.utils.load_mnist import load_mnist
import sys

from publish_client.MOM.KafkaClient import KafkaClient
from publish_client.MOM.PubSubClient import PubSubClient

config = {
    "test_images": "data/fashion/t10k-images-idx3-ubyte.gz",
    "test_labels": "data/fashion/t10k-labels-idx1-ubyte.gz",
}


def on_send_success(record_metadata):
    print("Message has been sent successfully %s" % record_metadata)


def on_send_error(excp):
    print("this is an error in sending the message: %s" % excp)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Optional app description')
    parser.add_argument('--mom_client', type=str,
                        help='it can either be kafka or pubsub; by default the system takes pubsub')
    args = parser.parse_args()
    topic = "client"
    if args.mom_client == 'kafka':
        print("Sending messages through Kafka")
        mom = KafkaClient()
    else:
        print("Sending messages through PubSub")
        mom = PubSubClient()
    x_valid, y_valid = load_mnist(config["test_images"], config["test_labels"])
    for idx in range(0, 100):
        to_send_data = x_valid[idx]
        print("Send array of bytes that match the %d entry form the validation" % idx)
        mom.send_message({'id': idx, 'img': to_send_data.tolist()})
        time.sleep(10)

    # block until all async messages are sent
    mom.wait_publishing_operations()
