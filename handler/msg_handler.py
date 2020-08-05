from base.handler.base_handler import tornado_wrap, BaseHandler
from database.stock import DbStreamer
from database.user import DbUser

import log
from model.stock_model.streamer import Streamer, StreamerStatusEnum


class MsgHandler(BaseHandler):
    @tornado_wrap
    async def get(self, params, data, headers):
        size, page = int(params['size']), int(params['page'])
        start = (page - 1) * size

        content = {
            'status': 'finish',
            'seq': '1',
            'group_no': 'group_no',
            'qq': 'qq',
            'name': 'name',
            'space_percent': 'space_percent',
            'one_found': 'one_found',
            'multi_one_found': 'multi_one_found',
            'esn': 'esn',
            'liuyirui': 'asdfasdfasdfasdfasdf',
            'buy_words': ','.join(["调入", "买", "关注", "加仓"]),
            'sell_words': ','.join(["调出", "卖", "止盈", "止损", "出局", "减半仓", "T出去", "减仓"]),
            'disable_words': ','.join(
                ["无关", "买卖", "复盘", "观望", "暂时持有", "持股待涨", "恭喜", "可以注意", "追高", "买了", "关注了", "不建议", "暂不", "暂", "不加仓",
                 "可以加仓", "暂时不", "如果封不死", "如果打开封不住", "如果打开", "如果封不住", "还能", "，", "分钟内不", "分钟之内不"]),
            'start_words': ','.join(["】", ":"]),
            'end_words': ','.join(["----------", "[操作提示]", "</r/n></r/n>", "</r/n> </r/n>"]),

        }
        contents = [content] * 10

        all_streamers = [streamer.to_dict() for streamer in await DbStreamer.get_all_streamer(start, size)]

        contents = all_streamers
        count = await DbStreamer().select_count()
        resp = {
            "payload": {
                "totalElements": count,
                "content": contents
            }
        }
        return 200, resp

    @tornado_wrap
    async def post(self, params, data, headers):
        streamer = Streamer.from_dict(data)
        streamer.status = StreamerStatusEnum.NO_EXECUTE.value

        db_streamer = DbStreamer().input(streamer)
        await db_streamer.insert()

    @tornado_wrap
    async def put(self, params, data, headers):
        id = params['id']
        streamer = Streamer.from_dict(data)
        streamer.id = id

        await DbStreamer.update_streamer(streamer)
