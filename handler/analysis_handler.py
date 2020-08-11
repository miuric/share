from analysis.analysis2 import origin2execute
from base.handler.base_handler import tornado_wrap, BaseHandler
import log
from config import bd_client
from database.stock import DbStreamer, DbGlobalLogic, DbLog
from model.stock_model.operation_words import ExecuteWords


def get_file_content(file):
    with open(file, 'rb') as fp:
        return fp.read()


def img_to_str(image_path):
    image = get_file_content(image_path)
    result = bd_client.basicGeneral(image)
    return result


class AnalysisHandler(BaseHandler):
    @tornado_wrap
    async def post(self, params, data, headers):
        img_flag = data.get('img_flag')

        if img_flag == 'yes':
            rimg = data.get('ori_words')
            with open("tmpimg.jpg", "wb") as rimgfp:
                rimgfp.write(rimg.content)
            bd_r = img_to_str('tmpimg.jpg')

            bd_r_r = bd_r['words_result']
            ori_words = ""
            for i in bd_r_r:
                ori_words += i["words"] + "\n"
        else:
            ori_words = data.get('ori_words')

        ori_words = '''2019-06-21 9:34:21 淘金尾盘股 服务中 欢迎加入(648296752)
        【趋势型—兰博LS】
        双塔食品(002481)
        调入
        17.81
        1成仓
        -----------------------------
        【操作提示】
        双塔食品 7.8左右反弹卖出 今天低开就弱了。
        开盘买入 300256 星星科技 低价便宜创业板

        '''
        db: DbStreamer = await DbStreamer().select_one_r()
        db_logic = await DbGlobalLogic().select_one_r()
        st = db.output()
        execute_words = origin2execute(ori_words, st, db_logic)

        log = DbLog()
        log.ori_words = ori_words
        log.execute_words = execute_words

        await log.insert_log()

        return 200, '200 OK'
        # log.qq_logger.info(self)
