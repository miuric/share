import json

from business_logic.trader import go_trader
from business_logic.word_analysis import origin2execute
from base.err_manage.err_enum import LogicErrorEnum
from base.handler.base_handler import tornado_wrap, BaseHandler
from config import bd_client
from database.stock import DbStreamer, DbGlobalLogic, DbLog
from log import logger
from model.stock_model.streamer import StreamerStatusEnum


def get_file_content(file):
    with open(file, 'rb') as fp:
        return fp.read()


def img_to_str(image_path):
    image = get_file_content(image_path)
    result = bd_client.basicGeneral(image)
    return result


class AnalysisHandler(BaseHandler):
    async def handle_exception(self, exception):
        logger.exception(self.exception_reason)
        self.db_log.reason = self.exception_reason

    async def handle_success(self):
        self.db_log.reason = '成功'

    async def handle_finish(self):
        await self.db_log.insert_log()

    async def handle_start(self):
        self.db_log = DbLog()

    @tornado_wrap
    async def post(self, params, data, headers):
        img_flag = data.get('img_flag')

        if img_flag is None:
            raise LogicErrorEnum.COMMON.exception('img_flag 参数未传')

        zb = data.get('zb')

        if zb is None:
            raise LogicErrorEnum.COMMON.exception('zb 参数未传')

        group_no, qq = zb.split('-')

        if None in (group_no, qq):
            raise LogicErrorEnum.COMMON.exception('zb 参数格式错误')

        ori_words = None

        if img_flag == 'yes':
            rimg = data.get('ori_words')
            with open("tmpimg.jpg", "wb") as rimgfp:
                rimgfp.write(rimg.content)
            bd_r = img_to_str('tmpimg.jpg')
            # bd_r = img_to_str('tmpimg.png')

            bd_r_r = bd_r['words_result']
            ori_words = ""
            for i in bd_r_r:
                ori_words += i["words"] + "\n"
        else:
            ori_words = data.get('ori_words')

            if ori_words is None:
                raise LogicErrorEnum.COMMON.exception('ori_words 参数未传')

        self.db_log.ori_words = ori_words

        db_logic = await DbGlobalLogic().select_one_r()

        if db_logic is None:
            db_logic = DbGlobalLogic()
            db_logic.buy = 0
            db_logic.sell = 0
            await db_logic.insert()
            db_logic = await DbGlobalLogic().select_one_r()

        streamer = await DbStreamer.find_streamer_by_qq(group_no, qq)

        if streamer is None:
            raise LogicErrorEnum.COMMON.exception('未找到')

        logger.debug('原始指令: \n{}'.format(ori_words))

        logger.debug('开始分析原始指令')
        execute_words = origin2execute(ori_words, streamer, db_logic)

        self.db_log.execute_words = execute_words

        if not execute_words.is_success():
            raise LogicErrorEnum.COMMON.exception('原始命令到执行命令解析错误')

        logger.debug('原始指令转化为执行指令成功')

        if streamer.status == StreamerStatusEnum.EXECUTE.value:
            logger.debug('开始交易')
            c, r, h = await go_trader(execute_words)
            try:
                logger.debug('api返回值: ', r)
                self.db_log.api = json.dumps(r)
            except:
                pass
        else:
            logger.debug('不执行交易')

        return 200, '200 OK'
