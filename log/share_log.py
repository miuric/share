from base.log import logger

__all__ = ['logger', 'qq_logger']

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, 'log_files')
DEBUG_DIR = os.path.join(LOG_DIR, 'debug')
QQ_DIR = os.path.join(LOG_DIR, 'qq')
EXCEPTION_DIR = os.path.join(LOG_DIR, 'exception')

if not os.path.exists(DEBUG_DIR):
    os.makedirs(DEBUG_DIR)

if not os.path.exists(QQ_DIR):
    os.makedirs(QQ_DIR)

if not os.path.exists(EXCEPTION_DIR):
    os.makedirs(EXCEPTION_DIR)

ALL_DEBUG_FILE = os.path.join(DEBUG_DIR, 'all_debug.log')
QQ_FILE = os.path.join(QQ_DIR, 'qq.log')
EXCEPTION_FILE = os.path.join(EXCEPTION_DIR, 'exception.log')

# 全局debug
logger.add(ALL_DEBUG_FILE, level='DEBUG', backtrace=False, diagnose=False, rotation='1h')
# exception
logger.add(EXCEPTION_FILE, level='ERROR', backtrace=False, diagnose=False, rotation='1 days')

# qq
sss = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | " \
      "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
logger.add(QQ_FILE, filter=lambda record: "qq" in record["extra"], level='INFO', format=sss)
qq_logger = logger.bind(qq=True)

# async def llll(message):
#     ddd = message.record
#     pass
#
# logger.add(llll)
