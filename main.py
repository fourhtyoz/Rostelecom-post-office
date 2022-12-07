import tornado.web
import tornado.ioloop
import asyncio
import os
import json

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
        data = {
            'lname': self.get_argument('lname'),
            'fname': self.get_argument('fname'),
            'mname': self.get_argument('mname'),
            'phone': self.get_argument('phone'),
            'message': self.get_argument('message')
            }
        json_obj = json.dumps(data)
        self.render('index.html')

async def main():
    http_server = tornado.httpserver.HTTPServer(Application())
    port = 8888
    http_server.listen(port)
    print(f'Running server on {port}')
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())