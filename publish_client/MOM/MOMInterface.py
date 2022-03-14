class MOMInterface:
    def __create_producer(self):
        """create producer object"""
        pass

    def __create_consumer(self, topic):
        """create consumer object"""
        pass

    def send_message(self, message, topic="client"):
        """send a message to the message queue"""
        pass

    def receive_message(self, message_callback, topic="client"):
        """receive a message from the message queue"""
        pass

    def wait_publishing_operations(self):
        """ block until all publishing operations are done"""
        pass
