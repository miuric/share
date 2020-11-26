import json

from base.err_manage.err_enum import LogicErrorEnum
from base.handler.base_handler import tornado_wrap, BaseHandler
from business_logic.trader import go_trader
from database.stock import DbLog
from log import logger
from model.stock_model.operation_words import ExecuteWords


class BuyHandler(BaseHandler):
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

    async def handle_exception(self, exception):
        logger.exception(self.exception_reason)
        self.db_log.reason = self.exception_reason

    async def handle_success(self):
        self.db_log.reason = '成功'

    async def handle_finish(self):
        await self.db_log.insert_log()

    async def handle_start(self):
        self.db_log = DbLog()

    @tornado_wrap
    async def post(self, params, data, headers):
        code, amount, price = data.get('code'), data.get('amount'), data.get('price')

        logger.debug('开始交易')

        execute_words = ExecuteWords(ExecuteWords.BUY, code, price, amount)
        self.db_log.execute_words = execute_words
        self.db_log.ori_words = '手动操作买入'

        c, r, h = await go_trader(execute_words)
        try:
            logger.debug(r)
            self.db_log.api = json.dumps(r)
            self.db_log.is_execute = '是'
            if not self.positive_code(c):
                raise Exception('')
        except:
            self.db_log.reason = c
            raise LogicErrorEnum.COMMON.exception(f'http: {c}')

        return 200, self.success_resp()


class SellHandler(BaseHandler):
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

    async def handle_exception(self, exception):
        logger.exception(self.exception_reason)
        self.db_log.reason = self.exception_reason

    async def handle_success(self):
        self.db_log.reason = '成功'

    async def handle_finish(self):
        await self.db_log.insert_log()

    async def handle_start(self):
        self.db_log = DbLog()

    @tornado_wrap
    async def post(self, params, data, headers):
        code, amount, price = data.get('code'), data.get('amount'), data.get('price')

        logger.debug('开始交易')

        execute_words = ExecuteWords(ExecuteWords.SELL, code, price, amount)
        self.db_log.execute_words = execute_words
        self.db_log.ori_words = '手动操作卖出'

        c, r, h = await go_trader(execute_words)
        try:
            logger.debug('api返回值: ', r)
            self.db_log.api = json.dumps(r)
            self.db_log.is_execute = '是'
            if not self.positive_code(c):
                raise Exception('')
        except:
            self.db_log.reason = c
            raise LogicErrorEnum.COMMON.exception(f'http: {c}')

        return 200, self.success_resp()
