import argparse
from json import loads
from image_classifier import config as cfg
from image_classifier.CNNModel import CNNModel
from image_classifier.DataPreprocessing import DataPreprocessing
from publish_client.MOM.KafkaClient import KafkaClient
from publish_client.MOM.PubSubClient import PubSubClient

if __name__ == '__main__':
    model = CNNModel(cfg.data['checkpoints'])

    def predict_and_respond(img):
        prediction = model.predict(img)
        print(
            "Sending prediction to topic result. The image received was classified by the model as %d" % prediction[0])
        mom.send_message({'prediction': str(prediction[0])}, topic='result')

    #pubsub callback
    def pubsub_callback(message):
        print("message received pubsub")
        print(message)
        data_img = loads(message.data)
        img = data_img['img']
        predict_and_respond(img)
        message.ack()

    #kafka callback
    def kafka_callback(message):
        print("message received kafka")
        print(message)
        image = message.value['img']
        predict_and_respond(image)


    parser = argparse.ArgumentParser(description='Optional app description')
    parser.add_argument('--mom_client', type=str,
                        help='it can either be kafka or pubsub; by default the system takes pubsub')
    parser.add_argument('--run_local', type=str,
                        help='run local or from docker')
    args = parser.parse_args()
    if args.run_local == 'True':
        ip = 'localhost:19092'
    else:
        ip = 'broker:9092'
    topic = "client"

    # load the data
    dataLoader = DataPreprocessing(cfg.data['training_images'], cfg.data['training_labels'], cfg.data['test_images'],
                                   cfg.data['test_labels'])
    train_x, train_y, test_x, test_y = dataLoader.process_data()

    # try to load the model's weights. If there are no weights train the model on the existing data

    if model.load_model() is None:
        print("No model found. Proceed to train model on data")
        scores, history = model.train_evaluate_model(train_x, train_y, n_folds=2)
        model.summarize_diagnostics(history)
        model.summarize_performance(scores)

    # print the accuracy for the validation dataset to have an idea about the state in which you loaded the model
    print("Current model accuracy %f" % model.evaluate_performance(test_x, test_y))

    #Select message broker
    if args.mom_client == 'kafka':
        print("Receiving messages through Kafka ip %s" % ip)
        mom = KafkaClient()
        mom.set_ip(ip)
        mom.receive_message(kafka_callback)
    else:
        print("Receiving messages through PubSub")
        mom = PubSubClient()
        mom.receive_message(pubsub_callback)
