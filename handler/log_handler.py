from analysis.analysis2 import origin2execute
from base.handler.base_handler import tornado_wrap, BaseHandler
from database.stock import DbStreamer, DbGlobalLogic, DbLog


class LogHandler(BaseHandler):
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
        db_logs = await DbLog().select_all()
        count = len(db_logs)

        contents = [log.strip_self() for log in db_logs]

        resp = {
            "payload": {
                "totalElements": count,
                "content": contents
            }
        }

        return 200, resp
        # log.qq_logger.info(self)
