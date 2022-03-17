# fashion_mnist

![alt text](https://github.com/cheresioana/fashion_mnist/blob/master/docs/diagram.jpg)

## Instructions

1. Create a service account for GCP PubSub service and get json authorization. Place it in the root directory with the name gcpkey.json
2. Create a topic “client” with a subscription “client0” and a topic called “result” with a subscription called “result” in GCP

2. Run the app:
	docker-compose up
3. For adding more component just add them in Docker-compose.yaml , changing only the ergument variable to “kafka” of “pubsub”, depending on which message broker you prefere.

4. For running the code locally
The project also works in a combination of containers and locally runned code.


4.1 Make sure the points 1 and 2 are respected

4.2 Create a virtual env and run pip install -r requirements.txt

4.3 Start kafka: sudo docker-compose up broker

4.4 Start the ml component
python mlcomponent.py – mom_client [kafka/pubsub] --run_local True

4.4 Start the client component
python client.py – mom_client [kafka/pubsub] --run_local True

## Code docs

1. Image classifier

The main code for the classification task is in mlcomponent.py. It checks if the weights of the classification model are already computed, and if so it loads the model. If mot, it trains the model and save the weights. Then it connects to the message middleware and waits for classification tasks.

The DataPreprocessing class contain usefull methods for reading and parsing the data
The CNN model contains usefull methods for working with the CNN Model

2. Messaging Client

MOMInterface folder provides a unified interfact for two messaging dydtems: kafka and pubsub.
The client.py only reads some validation entries and sends them using a message broker


## Deployment

For this project I chose Docker for demonstration purposes of the deployment configuration of the microservices.





