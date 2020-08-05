from base.db.db_util import BaseDbModel


class DbUser(BaseDbModel):
    pkey = 'username'
    db_name = 'share'
    tab_name = 'User'

    def __init__(self, obj=None):
        self.username = None
        self.password = None
        self.roles = None
        self.introduction = None
        self.avatar = None
        self.name = None
        self.token = None
        super().__init__(obj)

    @classmethod
    async def get_user(cls, username, password=None):
        db = cls()
        db.username = username
        db.password = password

        db = await db.select_one_r()

        return db

    @classmethod
    async def get_user_by_token(cls, token):
        db = cls()
        db.token = token

        db = await db.select_one_r()

        return db

