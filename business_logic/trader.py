from base.handler import base_handler
from base.handler.base_handler import BaseHandler
from model.stock_model.operation_words import ExecuteWords
from request_api.south import OrderApi


async def go_buy(code, price, amount):
    return await OrderApi().buy(code, price, amount)


async def go_sell(code, price, amount):
    return await OrderApi().sell(code, price, amount)


async def go_trader(execute: ExecuteWords):
    if execute.do_word == ExecuteWords.BUY:
        return await go_buy(execute.do_code, float(execute.do_price), int(execute.do_amount))
    if execute.do_word == ExecuteWords.SELL:
        return await go_sell(execute.do_code, float(execute.do_price), int(execute.do_amount))
