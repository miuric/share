from base.handler.base_handler import tornado_wrap, BaseHandler
import log
from database.stock import DbResume


class AnalysisHandler(BaseHandler):
    @tornado_wrap
    async def post(self, params, data, headers):

        # img_flag = flask.request.form['img_flag']
        # if img_flag == 'yes':
        #     rimg = requests.get(flask.request.form['ori_words'])
        #     with open("tmpimg.jpg", "wb") as rimgfp:
        #         rimgfp.write(rimg.content)
        #     bd_r = img_to_str('tmpimg.jpg')
        #
        #     bd_r_r = bd_r['words_result']
        #     ori_words = ""
        #     for i in bd_r_r:
        #         ori_words += i["words"] + "\n"
        #
        #
        # else:
        #     ori_words = flask.request.form['ori_words']
        ss = DbResume()
        ss.serial_no = 2
        await ss.insert()
        log.qq_logger.info(self)
