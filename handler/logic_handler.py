from base.handler.base_handler import tornado_wrap, BaseHandler
from database.stock import DbStreamer, DbGlobalLogic

from model.stock_model.streamer import Streamer, StreamerStatusEnum


class LogicHandler(BaseHandler):
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
        buy, sell = data.get('buy'), data.get('sell')

        db_logic = await DbGlobalLogic().select_one_r()

        if buy:
            new_logic = DbGlobalLogic()
            new_logic.buy = buy
            await new_logic.update(db_logic)

        if sell:
            new_logic = DbGlobalLogic()
            new_logic.sell = sell
            await new_logic.update(db_logic)

        db_logic = await DbGlobalLogic().select_one_r()

        resp = self.success_resp()
        resp['buy'], resp['sell'] = db_logic.buy, db_logic.sell

        return 200, resp

    @tornado_wrap
    async def get(self, params, data, headers):
        db_logic = await DbGlobalLogic().select_one_r()

        resp = self.success_resp()
        resp['buy'], resp['sell'] = db_logic.buy, db_logic.sell

        return 200, resp
