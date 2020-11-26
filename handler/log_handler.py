from base.handler.base_handler import tornado_wrap, BaseHandler
from database.stock import DbLog


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
