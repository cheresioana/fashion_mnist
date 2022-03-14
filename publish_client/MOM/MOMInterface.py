class MOMInterface:
    def send_message(self, message):
        '''send a message to the message queue'''
        pass

    def receive_message(self, message_function):
        '''receive a message from the message queue'''
        pass

    def on_send_success(self, record_metadata):
        '''Track the messages that were sent successfully'''
        pass

    def on_send_error(self, excp):
        '''Track the messages that were NOT sent successfully'''
        pass
