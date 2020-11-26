from base.handler.base_handler import BaseHandler
from config import key


class Api:
    base_host = ''
    base_path = ''
    api = ''

    def __repr__(self):
        return self.url()

    def url(self):
        return self.base_host + self.base_path + self.api

    async def http_query(self, metd: str, req_obj, is_response_json=True):
        if hasattr(req_obj, 'to_dict'):
            req_obj = req_obj.to_dict()

        elif isinstance(req_obj, dict):
            req_obj = req_obj

        else:
            req_obj = None

        url = self.url()

        if (metd == 'GET' or metd == 'DELETE') and req_obj is not None:
            url += '?'
            url += '&'.join([str(k) + '=' + str(v) for k, v in req_obj.items()])
            req_obj = None
            url += f'&key={key}'

        else:
            url += '?'
            url += f'key={key}'

        c, r, h = await BaseHandler.do_query(url=url, metd=metd, req_obj=req_obj, is_response_json=is_response_json)

        return c, r, h

    async def post(self, model, is_response_json=True):
        c, r, h = await self.http_query('POST', model, is_response_json)
        return c, r, h

    async def get(self, model=None, is_response_json=True):
        c, r, h = await self.http_query('GET', model, is_response_json)
        return c, r, h

    async def delete(self, model, is_response_json=True):
        c, r, h = await self.http_query('DELETE', model, is_response_json)
        return c, r, h

    async def put(self, model, is_response_json=True):
        c, r, h = await self.http_query('PUT', model, is_response_json)
        return c, r, h
