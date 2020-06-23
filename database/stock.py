import json

from base.db.db_util import BaseDbModel


class DbResume(BaseDbModel):
    pkey = 'id'
    db_name = 'nod_kafka'
    tab_name = 'Resume'

    def __init__(self, obj=None):
        self.id = None
        self.group_id = None
        self.service = None
        self.url = None
        self.methd = None
        self.serial_no = None
        self.body_json = None
        super().__init__(obj)

    @classmethod
    def init(cls, service=None, url=None, methd=None, serial_no=None, body_json: dict = None):
        db_resume = cls()
        db_resume.group_id = 3
        db_resume.service = service

        if url is None:
            return db_resume

        db_resume.url = url
        db_resume.methd = methd
        db_resume.serial_no = serial_no
        return db_resume

    def output(self):
        self.body_json = json.loads(self.body_json)

        return self

    async def select_all(self):
        r, m = await self.select()
        db_resumes = []

        for row in r:
            db_resume = type(self)(row).output()
            db_resumes.append(db_resume)

        return db_resumes
