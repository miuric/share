import datetime

from base.db.db_util import BaseDbModel
from model.stock_model.streamer import Streamer


class DbStreamer(BaseDbModel):
    pkey = 'id'
    db_name = 'share'
    tab_name = 'Streamer'

    def __init__(self, obj=None):
        self.id = None
        self.status = None
        self.group_no = None
        self.qq = None
        self.name = None
        self.space_percent = None
        self.one_found = None
        self.multi_one_found = None
        self.buy_words = None
        self.sell_words = None
        self.disable_words = None
        self.start_words = None
        self.end_words = None
        super().__init__(obj)

    def input(self, obj):
        if isinstance(obj, Streamer):
            self.from_dict(obj.to_dict())
        return self

    def output(self):
        return Streamer.from_dict(self.strip_self())

    async def select_all_by_limit(self, start, size, order_by=None, descend=True):
        limit = '{}, {}'.format(start, size)
        r, m = await self.select(limit=limit, orderby=order_by, descend=descend)
        return [type(self)(row) for row in r]

    @classmethod
    async def get_all_streamer(cls, start, size, order_by=None, descend=True):
        all_streams = [db.output() for db in await cls().select_all_by_limit(start, size, order_by, descend)]

        return all_streams

    @classmethod
    async def update_streamer(cls, streamer: Streamer):
        await DbStreamer().input(streamer).update()


class DbGlobalLogic(BaseDbModel):
    db_name = 'share'
    tab_name = 'Global_logic'

    def __init__(self, obj=None):
        self.buy = None
        self.sell = None
        super().__init__(obj)


class DbLog(BaseDbModel):
    pkey = 'id'
    db_name = 'share'
    tab_name = 'Log'

    def __init__(self, obj=None):
        self.ori_words = None
        self.execute_words = None
        self.reason = None
        self.created_time = None
        super().__init__(obj)

    async def insert_log(self):
        self.created_time = datetime.datetime.now()
        self.created_time = self.created_time.strftime('%Y-%m-%d %H:%M:%S')
        await self.insert()
