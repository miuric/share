import tornado.httpserver
import tornado.ioloop
import tornado.web

from handler.analysis_handler import AnalysisHandler
from handler.buy_handler import BuyHandler, SellHandler
from handler.end_handler import EndHandler
from handler.log_handler import LogHandler, LogExportHandler
from handler.logic_handler import LogicHandler
from handler.msg_handler import MsgHandler, MsgExportHandler, MsgImportHandler
from handler.position_handler import PositionHandler, AccountHandler
from handler.start_handler import StartHandler
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
            (base_url + r'/message/(?P<id>.+)', MsgHandler),
            (base_url + r'/message', MsgHandler),
            (base_url + r'/message_export', MsgExportHandler),
            (base_url + r'/message_import', MsgImportHandler),
            (base_url + r'/log', LogHandler),
            (base_url + r'/log_export', LogExportHandler),
            (base_url + r'/start', StartHandler),
            (base_url + r'/end', EndHandler),
            (base_url + r'/logic', LogicHandler),
            (base_url + r'/buy', BuyHandler),
            (base_url + r'/sell', SellHandler),
            (base_url + r'/position', PositionHandler),
            (base_url + r'/account', AccountHandler),

            # main
            (r'/ori_words', AnalysisHandler)

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
