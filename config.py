from aip import AipOcr

SHARE = "share"

ms_port_config = {
    SHARE: 20201,
}

db_host = '127.0.0.1'
db_user = 'root'
db_passwd = 'liuyirui'
db_port = 3306

south_base_host = "http://localhost:20202"

# 百度识图
bd_config = {
    'appId': '18898769',
    'apiKey': '80LZK2FsGUoSReVwaqhW5RN6',
    'secretKey': 'sbMp3ERC1v0yuFYtDWPYsjlDB6cXQc2I'
}

bd_client = AipOcr(**bd_config)

# log
_levels = TRACE, DEBUG, INFO, SUCCESS, WARNING, ERROR, CRITICAL = 'TRACE', 'DEBUG', 'INFO', 'SUCCESS', 'WARNING', 'ERROR', 'CRITICAL'
STDERR_DEBUG_LEVEL = DEBUG
