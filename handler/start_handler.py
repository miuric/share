from base.handler.base_handler import tornado_wrap, BaseHandler
from database.stock import DbStreamer

from model.stock_model.streamer import Streamer, StreamerStatusEnum


class StartHandler(BaseHandler):
    @staticmethod
    def failed_resp():
        return {
            'code': 60204,
            'message': 'Account and password are incorrect.'
        }

    @staticmethod
    def success_resp():
        return {
            'code': 20000,
        }

    @tornado_wrap
    async def post(self, params, data, headers):
        ids = data['id']

        for id in ids:
            streamer = Streamer()
            streamer.id = id

            db_streamer = DbStreamer()
            db_streamer.id = id
            db_streamer.status = StreamerStatusEnum.EXECUTE.value

            await db_streamer.update()

        return 200, self.success_resp()
