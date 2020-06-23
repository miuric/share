from .err_base import *

__all__ = ['ServerErrorEnum', 'JsonErrorEnum', 'ArgsErrorEnum']


# region 服务器内部错误
class ServerErrorEnum(BaseErrorEnum):
    INTERNAL_ERROR = "服务器内部错误: "


# endregion


# region JSON格式错误
class JsonErrorEnum(BaseErrorEnum):
    INVALID = "POST/PUT body is not valid JSON"

    def get_handler_error_cls(self):
        return JsonError


# endregion

class ArgsErrorEnum(BaseErrorEnum):
    BIGMODEL = "input json can not be transferred to big model."
    SERIALNO = "The serialno is duplicated."

    def get_handler_error_cls(self):
        return ArgsError


# region 业务逻辑错误
class LogicErrorEnum(BaseErrorEnum):
    COMMON = "{}"
    CLOUD_EXIST = "Cloud is exists"
    INTERNET_EXIST = "Internet is exists"
    INTERNET_BUILDING = "Internet is building"
    CLOUD_BUILDING = "Cloud is building"
    BUSINESS_NOT_EXIST = "Business is not exists"
    INTERNET_NOT_ACTIVE = "Internet is not in active status. Now is {}"
    INTERNET_NOT_STOP = "Internet is not in stop status. Now is {}"
    INTERNET_NOT_ACTIVE_OR_STOP = "Internet is not in active | stop status. Now is {}"

    CLOUD_NOT_ACTIVE = "Cloud is not in active status. Now is {}"
    CLOUD_NOT_ACTIVE_OR_STOP = "Cloud is not in active | stop status. Now is {}"
    CLOUD_NOT_STOP = "Cloud is not in stop status. Now is {}"
    CSVLAN_USED = "{}, {} has bounded with {} in {} device"
    A8C_USED = "a8-c is exists"
    A8C_LINE_NOT_EXISTS = "Line is not exists"
    A8C_INTERNET_STATUS = "Can not ip change because of the wrong internet status {}"
    POP_NOT_EXISTS = 'Pop not exists.'
    ASBR_NOT_EXISTS = 'ASBR not exists.'
    ASBR_INTERFACE_NOT_EXISTS = 'ASBR WAN interface is not exists.'
    CLOUD_MOVE = "Can not move cloud."
    RETURN_BACK = 'Error.'
    VNFM_NOT_EXISTS = "VNFM is not exists."
    CONTROLLER_NOT_EXISTS = "controller is not exists."
    def get_handler_error_cls(self):
        return LogicError
# endregion


# region 设备、接口错误
class DeviceErrorEnum(BaseErrorEnum):
    COMMON = "{}"
    DEVICE_NAGUAN_FAILED = 'Device naguan failed.'
    DEVICE_WITH_WAN_IP = "Device with wan_ip ({}) "
    DEVICE_NOT_EXIST = DEVICE_WITH_WAN_IP + "is not exist"
    DEVICE_INACTIVE = "Device is inactive."
    INTERFACE_NOT_EXISTS = "Interface is not exists"

    def get_handler_error_cls(self):
        return DeviceError


# endregion