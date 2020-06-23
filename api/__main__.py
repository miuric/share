import tornado.httpserver
import tornado.ioloop
import tornado.web

from api.analysis_handler import AnalysisHandler
from base.handler.base_handler import tornado_wrap, BaseHandler
from config import ms_port_config, SHARE
from model.south.order import Order
from request_api.south import OrderApi


class ShareHandler(BaseHandler):
    @tornado_wrap
    async def get(self, params, data, headers):
        c, r, h = await OrderApi().post(
            Order(symbol="23")
        )
        print('asdf')

    @tornado_wrap
    async def post(self, params, data, headers):
        return 200, {
            'code': 20000,
            'data': 'admin-token'
        }


class ShareApp(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/dev-api/vue-element-admin/user/login', ShareHandler),
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
