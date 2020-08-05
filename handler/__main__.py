import tornado.httpserver
import tornado.ioloop
import tornado.web

from handler.msg_handler import MsgHandler
from handler.user_handler import LoginHandler, UserInfoHandler
from config import ms_port_config, SHARE

base_url = '/dev-api'


class ShareApp(tornado.web.Application):
    def __init__(self):
        handlers = [
            # login
            (base_url + r'/user/login', LoginHandler),
            (base_url + r'/user/info', UserInfoHandler),

            # front-end
            (base_url + r'/message', MsgHandler),

            # main

        ]
        tornado.web.Application.__init__(self, handlers)


order_check_version = 'v1'

if __name__ == '__main__':
    instance = tornado.ioloop.IOLoop.instance()
    app = ShareApp()
    server = tornado.httpserver.HTTPServer(app)
    port = ms_port_config[SHARE]
    server.listen(port)
    tornado.ioloop.IOLoop.instance().start()
