import tornado.web
import tornado.ioloop
import asyncio
import os
import json
import pika
from pika.adapters.tornado_connection import TornadoConnection

# RMQ settings
rmq_user = 'guest'
rmq_password = 'guest'
rmq_host = 'localhost'
rmq_port = 5672
# channel = None

# Tornado settings:
tornado_port = 8888


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
        self.connection.channel(self.on_channel_open)
        print('Successfully connected to RabbitMQ')

    def on_channel_open(self, new_channel):
        # When a channel is open
        global channel
        channel = new_channel
        print('A new channel has been opened')

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", IndexHandler)
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=True,
            autoreload=True
        )
        tornado.web.Application.__init__(self, handlers, **settings)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')
        
    def post(self):
        try:
            data = {
                'lname': self.get_argument('lname'),
                'fname': self.get_argument('fname'),
                'mname': self.get_argument('mname'),
                'phone': self.get_argument('phone'),
                'message': self.get_argument('message')
                }
            json_obj = json.dumps(data)
            channel.basic_publish(
                exchange='', 
                routing_key='message', 
                properties=pika.BasicProperties(content_type='application/json'), 
                body=json_obj
            )
            self.render('index.html')
        except Exception as e:
            print(f'IndexHandler Post Error: {e}')

# async def main():
application = Application()


    # http_server = tornado.httpserver.HTTPServer(Application())
    # port = 8888
    # http_server.listen(port)
    # print(f'Running server on {port}')
    # await asyncio.Event().wait()

if __name__ == "__main__":
    application.pika = PikaClient()
    application.listen(tornado_port)
    rabbit = pika.BlockingConnection()
    channel = rabbit.channel()
    channel.queue_declare(queue='message')
    ioloop = tornado.ioloop.IOLoop.instance().start()
    # asyncio.run(main())