from base.handler.base_handler import tornado_wrap, BaseHandler
import log
from config import bd_client
from database.stock import DbResume


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

        return 200, '200 OK'
        # log.qq_logger.info(self)
