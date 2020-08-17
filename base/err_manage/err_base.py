import sys
from collections import Iterable
from enum import Enum

from .status_code import HTTP_CODE


class HandlerError(Exception):
    def __init__(self, message, code=HTTP_CODE.FAILED):
        self.message = message
        self.err_code = code
        super().__init__(message)

    def get_exc_info(self):
        return type(self), self, sys.exc_info()[2]

    def handler_write_error(self, handler):
        exc_info = self.get_exc_info()
        handler.write_error(self.err_code, exc_info=exc_info)


class ArgsError(HandlerError):
    pass


class JsonError(HandlerError):
    pass


class DeviceError(HandlerError):
    pass


class InterfaceError(HandlerError):
    pass


class LogicError(HandlerError):
    pass


class ValueErrorYaml(HandlerError):
    pass


class BaseErrorEnum(Enum):
    def write_exception(self, handler, e_args, code=HTTP_CODE.FAILED):
        HandlerError(self.value + str(e_args), code=code).handler_write_error(handler)

    def exception(self, format_args=None, code=HTTP_CODE.FAILED):
        ignore_types = (str, bytes, dict)
        if format_args is None:
            format_args = ()
        elif not isinstance(format_args, Iterable) or isinstance(format_args, ignore_types):
            format_args = (format_args,)

        handler_error = self.get_handler_error_cls()
        return handler_error(message=self.value.format(*format_args), code=code)

    def get_handler_error_cls(self):
        return HandlerError
