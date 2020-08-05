import datetime
import json
import traceback
from functools import wraps

import tornado.web
import tornado.gen
import tornado.httpclient

from base.err_manage.err_enum import JsonErrorEnum, HandlerError, ServerErrorEnum, HTTP_CODE

bytes_decode = lambda x: x.decode('utf-8') if isinstance(x, bytes) else x
json_header = {'Content-Type': 'application/json; charset=utf-8', 'Accept': 'application/json'}


def tornado_wrap(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        handler = args[0]
        try:
            params = {k: handler.decode_argument(v[0], name=k)
                      for k, v in handler.request.query_arguments.items()}
            handler.params = params
            data = handler.json_body_load()
            headers = handler.request.headers
            handler.headers = headers
            await handler.handle_start()
            result = await func(handler, params, data, headers)

        except Exception as e:
            handler.exception_reason = e
            await handler.handle_exception(e)
            await handler.handle_finish()
            if isinstance(e, HandlerError):
                e.handler_write_error(handler)
            else:
                ServerErrorEnum.INTERNAL_ERROR.write_exception(handler, e.args[0])

        else:
            await handler.handle_success()
            handler_finish(handler, *(result or [HTTP_CODE.SUCCESS, None, None]))

    def handler_finish(handler, code, resp, headers=None):
        try:
            handler._status_code = code
            if headers is not None:
                x_hdrs = {k: v for k, v in headers.items() if k.startswith('X-')}
                for k, v in x_hdrs.items():
                    handler.set_header(k, v)

            resp = handler.resp_with_output(resp)
            handler.finish(resp)
        except Exception as e:
            ServerErrorEnum.INTERNAL_ERROR.write_exception(handler, e.args[0])

    return wrapper


class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)
        self._exception = None
        self.body_json = None
        self.params = None
        self.headers = {}

    def write_error(self, http_code=HTTP_CODE.FAILED, **kwargs):
        err_cls, err, exc_traceback = kwargs['exc_info']
        if err.args:
            self.set_status(http_code)
            self.finish(self.resp_with_error(http_code, err_msg=err.args[0]))

    def finish(self, chunk=None):
        super().finish(chunk)

        log_list = [
            ('code: ', self.get_status()),
            ('resp: ', json.dumps(chunk)),
        ]

        keys, values = zip(*log_list)

        # log_util.i('\n'.join(map(lambda x: x + '{}', keys)).format(*values))

    @tornado_wrap
    async def get(self, params, data, headers):
        pass

    @tornado_wrap
    async def post(self, params, data, headers):
        pass

    @tornado_wrap
    async def put(self, params, data, headers):
        pass

    @tornado_wrap
    async def delete(self, params, data, headers):
        pass

    def resp_with_output(self, resp):
        return resp

    def resp_with_error(self, error_code, err_msg=None):
        return {}

    async def handle_exception(self, exception):
        pass

    async def handle_success(self):
        pass

    async def handle_finish(self):
        pass

    async def handle_start(self):
        pass

    def form_response(self):
        resp = {'code': 0, 'message': 'OK', 'payload': {}}
        return resp

    def set_json_header(self):
        self.set_header('Content-Type', 'application/json,charset=utf-8')

    @staticmethod
    def positive_code(code):
        if 200 <= code < 400:
            return True
        return False

    @staticmethod
    def map_obj_key(src, map):
        dst = {}
        for k in src:
            if k in map:
                dst[map[k]] = src[k]
            else:
                dst[k] = src[k]
        return dst

    @staticmethod
    @tornado.gen.coroutine
    def do_query(url, req_obj=None, auth=None, metd='POST', tmout=6, validate_cert=False, client_key=None,
                 client_cert=None, ca_certs=None, extra_hdr={}, is_response_json=True, **kwargs):
        resp = {}
        hdr = {}
        code = 500
        try:
            req_body = None
            if req_obj:
                req_body = json.dumps(req_obj)
            user = passwd = None
            if auth and 'user' in auth and 'passwd' in auth:
                user = auth['user']
                passwd = auth['passwd']

            req_hdrs = json_header
            if extra_hdr:
                req_hdrs = dict(json_header, **extra_hdr)

            body = req_body
            if (metd == 'GET' or metd == 'DELETE') and body:
                url += '?'
                url += ';'.join([str(r) + '=' + str(req_obj[r]) for r in req_obj])
                body = None
            if metd == 'POST' and not body:
                body = json.dumps({})
            http_req = tornado.httpclient.HTTPRequest(url, method=metd, body=body, headers=req_hdrs,
                                                      request_timeout=tmout,
                                                      auth_username=user, auth_password=passwd,
                                                      validate_cert=validate_cert, client_key=client_key,
                                                      client_cert=client_cert, ca_certs=ca_certs)
            client = tornado.httpclient.AsyncHTTPClient()
            start = datetime.datetime.now()
            resp = yield tornado.gen.Task(client.fetch, http_req)
            code = resp.code
            if code > 300:
                # raise tornado.gen.Return((code, resp.error.message, None))
                raise tornado.gen.Return((code, bytes_decode(resp.body), None))

            else:
                # log_util.d('Response:', '' if not resp.body is None else bytes_decode(resp.body))
                pass

            try:
                if resp:
                    hdr = resp.headers
                    if resp.body and len(resp.body) > 0:
                        resp = resp.body
                        if isinstance(resp, bytes):
                            resp = resp.decode('utf-8')

                        if is_response_json:
                            resp = json.loads(resp)
                    else:
                        resp = {}
            except:
                traceback.print_exc()
                code, resp = 500, 'Internal Server Error'
                pass
        except (LookupError, TypeError):
            traceback.print_exc()
            pass

        raise tornado.gen.Return((code, resp, hdr))

    def json_body_load(self):
        try:
            if self.request.body:
                req = self.request.body.decode('utf-8')
                obj = json.loads(req)
                self.body_json = obj
                return obj
        except Exception:
            self.body_json = self.request.arguments
            for k, v in self.body_json.items():
                self.body_json[k] = v[0].decode('utf-8')

            return self.body_json
            # raise JsonErrorEnum.INVALID.exception()
