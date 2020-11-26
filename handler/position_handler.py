import itertools

from base.handler.base_handler import tornado_wrap, BaseHandler
from database.stock import DbStreamer
from database.user import DbUser

import log
from model.stock_model.streamer import Streamer, StreamerStatusEnum
from request_api.south import PositionApi


class PositionHandler(BaseHandler):
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
    async def get(self, params, data, headers):
        c, r, h = await PositionApi().get_positions()

        size, page = int(params['size']), int(params['page'])
        prop, order = params.get('prop'), params.get('order')
        start = (page - 1) * size

        order_by, descend = None, True
        if prop and order:
            order_by = prop
            if order == 'ascending':
                descend = False

        rows = r['dataTable']['rows']
        keys = ['detail', 'code', 'name', 'stock_balance', 'available_balance', 'frozen_number', 'cost_price',
                'market_price', 'profit_and_loss', 'market_value', 'trading_market']

        if order_by:
            index = keys.index(order_by)
            rows = sorted(rows, key=lambda x: x[index], reverse=not descend)

        rows = itertools.islice(rows, start, start + size)

        contents = [dict(zip(keys, row)) for row in rows]

        resp = {
            "payload": {
                "totalElements": 1,
                "content": contents
            }
        }
        return 200, resp


class AccountHandler(BaseHandler):
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
    async def get(self, params, data, headers):
        c, r, h = await PositionApi().get_positions()

        rows = r['subAccounts']['人民币']
        keys = ['frozen_money', 'take_money', 'available_money', 'gain_and_loss', 'total_money', 'stock_value',
                'fund_balance']

        resp = self.success_resp()
        resp = dict(resp, **dict(zip(keys, map(lambda x: str(x), rows.values()))))

        return 200, resp
