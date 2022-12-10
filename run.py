from backend import Application
from rabbitmq import PikaClient
import pika
import tornado.ioloop

# Tornado settings:
tornado_port = 8888

if __name__ == "__main__":
    application = Application()
    application.pika = PikaClient()
    application.listen(tornado_port)
    rabbit = pika.BlockingConnection()
    channel = rabbit.channel()
    channel.queue_declare(queue='message')
    ioloop = tornado.ioloop.IOLoop.instance().start()