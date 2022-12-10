import pika
from pika.adapters.tornado_connection import TornadoConnection
import logging

# Logging settings
LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)


# RMQ settings
rmq_user = 'guest'
rmq_password = 'guest'
rmq_host = 'localhost'
rmq_port = 5672

class PikaClient():
    def connect(self):
        try:
            credentials = pika.PlainCredentials(rmq_user, rmq_password)
            param = pika.ConnectionParameters(host=rmq_host, port=rmq_port, credentials=credentials)
            self.connection = TornadoConnection(param, on_open_callback=self.on_connected)
        except Exception as e:
            print(f'Pika Client Connect Error: {e}')   

    def on_connected(self, connection):
        # When successfully connected to RabbitMQ
        self.open_channel()
        # self.connection.channel(self.on_channel_open)
        print('Successfully connected to RabbitMQ')

    def on_channel_open(self, new_channel):
        # When a channel is open
        global channel
        channel = new_channel
        print('A new channel has been opened')