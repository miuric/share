import asyncio
import re

from base.common import get_price_min
from database.stock import DbStreamer
from model.stock_model.operation_words import ExecuteWords
from model.stock_model.streamer import Streamer

RE_CODE = re.compile(r'.*([0 3 6][0][0-9][0-9][0-9][0-9]).*')


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
    match_code = RE_CODE.match(ori_words, re.I)

    if match_code:
        match_code = match_code.group(1)

    return match_code


def _find_do_price(ori_words, streamer: Streamer, do_word, do_code):
    if None in (do_word, do_code):
        return None

    one_found = streamer.one_found

    do_price = None

    if do_word == ExecuteWords.SELL and do_code:
        do_price = get_price_min(do_code)

    if do_word == ExecuteWords.BUY:
        pass


    return do_price


def origin2execute(ori_words, streamer: Streamer):
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

    # do_code
    do_code = _find_do_code(temp_words)

    # do_price
    do_price = _find_do_price(temp_words, streamer, do_word, do_code)

    print(do_code, do_word, do_price, do_amount)

    standard = temp_words

    return standard


zb = '567700379-2448009272'
ori_words = '''2019-06-21 9:34:21 淘金尾盘股 服务中 欢迎加入(648296752)
【趋势型—兰博LS】
双塔食品(002481)
调出
7.81
1成仓
-----------------------------
【操作提示】
双塔食品 7.8左右反弹卖出 今天低开就弱了。
开盘买入 300256 星星科技 低价便宜创业板

'''


async def hey():
    db: DbStreamer = await DbStreamer().select_one_r()
    st = db.output()
    print(origin2execute(ori_words, st))


asyncio.get_event_loop().run_until_complete(hey())
