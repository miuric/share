import datetime
import re
from time import strftime

from base.handler.base_handler import tornado_wrap, BaseHandler
from database.stock import DbLog

DATE_RE = re.compile(r'(.*?)T(.*?)Z')

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
        size, page = int(params['size']), int(params['page'])
        prop, order = params.get('prop'), params.get('order')
        start = (page - 1) * size

        order_by, descend = None, True
        if prop and order:
            order_by = prop
            if order == 'ascending':
                descend = False

        if prop is None:
            order_by = 'created_time'
            descend = True

        all_logs = [log.strip_self() for log in await DbLog().select_all_by_limit(start, size, order_by, descend)]

        contents = all_logs
        count = await DbLog().select_count()

        resp = {
            "payload": {
                "totalElements": count,
                "content": contents
            }
        }

        return 200, resp
        # log.qq_logger.info(self)


class LogExportHandler(LogHandler):
    @tornado_wrap
    async def get(self, params, data, headers):
        start_date, end_date = params.get('date')

        start_match = DATE_RE.match(start_date)
        end_match = DATE_RE.match(end_date)

        start_date = ' '.join([start_match.group(1), '00:00:00'])
        end_date = ' '.join([end_match.group(1), '23:59:59'])

        all_logs = await DbLog.select_date(start_date, end_date)

        resp = {
            "payload": all_logs
        }

        resp = dict(self.success_resp(), **resp)

        return 200, resp