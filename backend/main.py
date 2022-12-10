# Libraries
import tornado.web
import tornado.ioloop
import os
import json
import pika

# Microservices

# Tornado settings:
tornado_port = 8888

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", IndexHandler)
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname("frontend"), "frontend/templates"),
            static_path=os.path.join(os.path.dirname("frontend"), "frontend/static"),
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