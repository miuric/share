import asyncio
import datetime
import json
import re

from base.common import get_price_min, getprice
from database.stock import DbStreamer, DbGlobalLogic
from log import logger
from model.stock_model.operation_words import ExecuteWords
from model.stock_model.streamer import Streamer

RE_CODE = re.compile(r'.*([0 3 6][0][0-9][0-9][0-9][0-9]).*', re.I | re.M | re.S)
RE_PRICE = re.compile(r'\d+\.?\d*', re.I)


def _find_do_work(ori_words, streamer: Streamer):
    buy_words, sell_words = streamer.buy_words, streamer.sell_words

    do_word = None

    for one_buy_words in buy_words.split(','):
        if one_buy_words in ori_words:
            do_word = ExecuteWords.BUY
            break

    for one_sell_words in sell_words.split(','):
        if one_sell_words in ori_words:
            do_word = ExecuteWords.SELL
            break

    return do_word


def _find_do_code(ori_words):
    match_code = RE_CODE.match(ori_words)

    if match_code:
        match_code = match_code.group(1)

    return match_code


def _find_do_price(ori_words, streamer: Streamer, do_word, do_code, global_logic: DbGlobalLogic):
    if None in (do_word, do_code):
        return None

    do_price = None

    if do_word == ExecuteWords.SELL and do_code:
        do_price = get_price_min(do_code)

    if do_word == ExecuteWords.BUY:
        price_now = getprice(do_code)
        do_price = price_now
        new_words_no_code = ori_words.replace(do_code, '')
        new_do_price = None
        find_price = RE_PRICE.findall(new_words_no_code)

        for one_price in find_price:
            if abs(float(one_price) - float(price_now)) / float(price_now) < 0.11:
                if not new_do_price:
                    new_do_price = one_price
                else:
                    if abs(float(one_price) - float(price_now)) < abs(
                            float(new_do_price) - float(price_now)):
                        new_do_price = one_price
        if new_do_price:
            do_price = new_do_price
        do_price = round(float(do_price) + global_logic.buy, 2)

    return do_price


def _find_do_amount(ori_words, streamer: Streamer, do_word, do_price):
    do_amount_tmp = '1'
    do_amount = None

    if do_word == ExecuteWords.BUY:
        amount_words = json.loads(streamer.space_percent)
        one_found = streamer.one_found
        max_to_buy = one_found * float(do_amount_tmp) / float(do_price)

        for one_amount_words in amount_words:
            if one_amount_words in ori_words:
                do_amount_tmp = amount_words[one_amount_words]
                break

        to_buy = int(max_to_buy / 100) * 100

        if to_buy < 100:
            max_to_buy_plus1 = one_found * (float(do_amount_tmp) + 1) / float(do_price)
            to_buy_plus1 = int(max_to_buy_plus1 / 100) * 100
            if to_buy_plus1 < 100:
                pass
            else:
                do_amount = str(to_buy_plus1)
        else:
            do_amount = str(to_buy)

        if float(do_amount_tmp) == 1 and do_amount:
            if (one_found - float(do_amount) * float(do_price)) * 1.5 >= 100 * float(do_price):
                do_amount = str(int(do_amount) + 100)

    if do_word == ExecuteWords.SELL:
        do_amount = '0'

    return do_amount


def origin2execute(ori_words, streamer: Streamer, global_logic: DbGlobalLogic):
    temp_words = ori_words

    disable_words, start_words, end_words = streamer.disable_words, streamer.start_words, streamer.end_words

    do_code, do_word, do_price, do_amount = None, None, None, None

    # disable
    for word in disable_words:
        temp_words = temp_words.replace(word, '')

    # start & end words
    if start_words:
        start_words_list = start_words.split(',')

        for word in start_words_list:
            index = temp_words.find(word)

            if index > 0:
                temp_words = temp_words[index + 1:]

    if end_words:
        end_words_list = end_words.split(',')

        for word in end_words_list:
            index = temp_words.find(word)

            if index > 0:
                temp_words = temp_words[:index]

    # do_word
    do_word = _find_do_work(temp_words, streamer)
    logger.debug('do_word: {}'.format(do_word))

    # do_code
    do_code = _find_do_code(temp_words)
    logger.debug('do_code: {}'.format(do_code))

    # do_price
    do_price = _find_do_price(temp_words, streamer, do_word, do_code, global_logic)
    logger.debug('do_price: {}'.format(do_price))

    # do_amount
    do_amount = _find_do_amount(temp_words, streamer, do_word, do_price)
    logger.debug('do_amount: {}'.format(do_amount))

    execute_words = ExecuteWords(do_word, do_code, do_price, do_amount)

    return execute_words


zb = '567700379-2448009272'
ori_words = '''2019-06-21 9:34:21 淘金尾盘股 服务中 欢迎加入(648296752)
【趋势型—兰博LS】
双塔食品(002481)
调入
17.81
1成仓
-----------------------------
【操作提示】
双塔食品 7.8左右反弹卖出 今天低开就弱了。
开盘买入 300256 星星科技 低价便宜创业板

'''


async def hey():
    db: DbStreamer = await DbStreamer().select_one_r()
    db_logic = await DbGlobalLogic().select_one_r()
    st = db.output()
    print(origin2execute(ori_words, st, db_logic))

# asyncio.get_event_loop().run_until_complete(hey())

# print(type(datetime.datetime.now()))
