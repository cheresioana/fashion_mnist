# fashion_mnist

![alt text](https://github.com/cheresioana/fashion_mnist/blob/master/docs/diagram.jpg)

## Instructions

1. Create a service account for GCP PubSub service and get json authorization. Place it in the root directory with the name gcpkey.json
2. Create a topic “client” with a subscription “client0” and a topic called “result” with a subscription called “result” in GCP

2. Run the app:
	docker-compose up
3. For adding more component just add them in Docker-compose.yaml , changing only the environment variable to “kafka” of “pubsub”, depending on which message broker you prefere.

4. For running the code separately

4.1 Make sure the points 1 and 2 are respected
4.2 run pip install -r requirements.txt
4.3 Start the ml component
python mlcomponent.py – mom_client [kafka/pubsub]
4.4 Start the client component
python client.py – mom_client [kafka/pubsub]

