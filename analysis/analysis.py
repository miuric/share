# -*- coding:utf-8 -*-
import flask
import time
import json
from urllib import request
import re
import requests

from aip import AipOcr


def tpanduan(tnow):  # 时间判断
    a = time.localtime(tnow)
    zstime = 0
    if (a.tm_hour < 9):
        return -1
    elif a.tm_hour >= 21:
        return -1
    else:
        return 0


bd_config = {
    'appId': '18898769',
    'apiKey': '80LZK2FsGUoSReVwaqhW5RN6',
    'secretKey': 'sbMp3ERC1v0yuFYtDWPYsjlDB6cXQc2I'
}

bd_client = AipOcr(**bd_config)


def get_file_content(file):
    with open(file, 'rb') as fp:
        return fp.read()


def img_to_str(image_path):
    image = get_file_content(image_path)
    # 通用文字识别（可以根据需求进行更改）
    result = bd_client.basicGeneral(image)
    return result


# import logging
# import strategyease_sdk


fp = open('config_list.cfg', 'r', encoding='utf-8')
config_list = json.loads(fp.read())
fp.close()

timelist = []
x19list = []
endx10list = []
namecodedict = {}


# logging.basicConfig(level=logging.DEBUG)

# client = strategyease_sdk.Client(host='localhost', port=8888, key='')


# def update_zhangben():#更新账本 use py sdk ver
#     p = client.get_positions()
#     p_p = p['positions']
#     pp = p_p.to_dict(orient='index')
#     if pp[0]['证券名称'] == '':
#         fp_zb=open('zhangben.data','w',encoding='utf-8')
#         fp_zb.write(json.dumps({}))
#         fp_zb.close()
#     else:
#         ppp = {}
#         for i in pp:
#             ppp[i['证券代码']] = i['证券数量']
#         fp_zb=open('zhangben.data','w',encoding='utf-8')
#         fp_zb.write(json.dumps(ppp))
#         fp_zb.close()

def update_zhangben():  # 更新账本
    print('更新账本')
    url = 'http://localhost:8888/api/v1.0/positions'
    r = requests.get(url).json()['dataTable']['rows']
    print(r)
    # if r[0][1] == '':
    if r == []:
        fp_zb = open('zhangben.data', 'w', encoding='utf-8')
        fp_zb.write(json.dumps({}))
        fp_zb.close()
        fp_zb_name = open('zhangben_name.data', 'w', encoding='utf-8')
        fp_zb_name.write(json.dumps({}))
        fp_zb_name.close()
    else:
        p = {}
        pn = {}
        for i in r:
            p[i[0]] = i[3]
            pn[i[0]] = i[1]
        fp_zb = open('zhangben.data', 'w', encoding='utf-8')
        fp_zb.write(json.dumps(p))
        fp_zb.close()
        fp_zb_name = open('zhangben_name.data', 'w', encoding='utf-8')
        fp_zb_name.write(json.dumps(pn))
        fp_zb_name.close()


def go_buy(code, price, amount):  # 格式 go_buy('600001',0.7,200)
    print('func go_buy ' + code, price, amount)
    header = {'Content-Type': 'application/json'}
    payload = {'action': 'BUY', 'amount': amount, 'price': price, 'priceType': 0, 'symbol': code, 'type': 'LIMIT'}
    url = 'http://localhost:8888/api/v1.0/orders'
    r = requests.post(url, json=payload, headers=header, verify=False)
    print('api返回值：', r.content.decode())


def go_sell(code, price, amount):  # 格式 gp_sell('600001',0.7,200)
    print('func go_sell ' + code, price, amount)
    header = {'Content-Type': 'application/json'}
    payload = {'action': 'SELL', 'amount': amount, 'price': price, 'priceType': 0, 'symbol': code, 'type': 'LIMIT'}
    url = 'http://localhost:8888/api/v1.0/orders'
    r = requests.post(url, json=payload, headers=header, verify=False)
    print('api返回值：', r.content.decode())


def mylog(zb, nr):
    file = zb + '.csv'
    with open(file, 'a+', encoding='gbk') as f:
        f.write(nr)


def timestr():
    return time.asctime(time.localtime(time.time())) + '  '


def getname(code):  # 股票名
    url_base = "http://qt.gtimg.cn/q=s_"
    if code[0] == '6':
        url = url_base + 'sh' + code
    else:
        url = url_base + 'sz' + code
    req = request.Request(url)
    response = request.urlopen(req)
    page = response.read().decode('gbk')
    data = page.split('~')
    return (data[1])


def getprice(code):  # 股票价格
    url_base = "http://qt.gtimg.cn/q=s_"
    if code[0] == '6':
        url = url_base + 'sh' + code
    else:
        url = url_base + 'sz' + code
    # print(url)
    req = request.Request(url)
    response = request.urlopen(req)
    page = response.read().decode('gbk')
    data = page.split('~')
    # print(data)
    return (data[3])


def getpricemax(code):  # 股票最高价格
    url_base = "http://qt.gtimg.cn/q="
    if code[0] == '6':
        url = url_base + 'sh' + code
    else:
        url = url_base + 'sz' + code
    req = request.Request(url)
    response = request.urlopen(req)
    page = response.read().decode('gbk')
    data = page.split('~')
    return (data[47])


def getpricekaipan(code):  # 开盘价
    url_base = "http://qt.gtimg.cn/q="
    if code[0] == '6':
        url = url_base + 'sh' + code
    else:
        url = url_base + 'sz' + code
    req = request.Request(url)
    response = request.urlopen(req)
    page = response.read().decode('gbk')
    data = page.split('~')
    return (data[5])


def getpricekaipanbfb(code):  # 开盘价格百分比
    url_base = "http://qt.gtimg.cn/q="
    if code[0] == '6':
        url = url_base + 'sh' + code
    else:
        url = url_base + 'sz' + code
    req = request.Request(url)
    response = request.urlopen(req)
    page = response.read().decode('gbk')
    data = page.split('~')
    return (data[32])


def getpricemin(code):  # 最低价
    url_base = "http://qt.gtimg.cn/q="
    if code[0] == '6':
        url = url_base + 'sh' + code
    else:
        url = url_base + 'sz' + code
    req = request.Request(url)
    response = request.urlopen(req)
    page = response.read().decode('gbk')
    data = page.split('~')
    return (data[48])


def gogoodprice(c, pp):  # 价格弄到最高到最低之间
    p = float(pp)
    x1 = float(getpricemax(c))
    x2 = float(getpricemin(c))
    if p > x1:
        return x1
    if p < x2:
        return x2
    if p < x1 and p > x2:
        return p


def goanalysys(zb, ori_words):
    tologstr = ''
    for one_zb_config in config_list:
        if zb == one_zb_config['id']:
            sw_last = ''
            sw_pos_tmp = 0

            for sw in one_zb_config['start_words']:
                if sw in ori_words:

                    if ori_words.rfind(sw) > sw_pos_tmp:
                        sw_last = sw
                        sw_pos_tmp = ori_words.rfind(sw)

            ew_first = ''
            ew_pos_tmp = len(ori_words)

            for ew in one_zb_config['end_words']:
                if ew in ori_words:

                    if ori_words.rfind(ew) < ew_pos_tmp:
                        ew_first = ew
                        ew_pos_tmp = ori_words.find(ew)
            tologstr += (',最后开始词：' + sw_last + ' 最初结束词：' + ew_first)
            print('最后开始词：' + sw_last + ' 最初结束词：' + ew_first)

            sw_pos = 0 if sw_last == '' else ori_words.rfind(sw_last) + len(sw_last)
            ew_pos = len(ori_words) if ew_first == '' else ori_words.find(ew_first)
            new_words = ori_words[sw_pos:ew_pos]

            tologstr += (',截取后：' + new_words)
            print('截取后：' + new_words)

            do_word = ''
            do_code = ''
            do_price = ''
            do_amount = ''

            code_found_flag = 0

            for one_buy_words in one_zb_config['buy_words']:
                if one_buy_words in new_words:
                    do_word = 'buy'
                    print('BUY')
            for one_sell_words in one_zb_config['sell_words']:
                if one_sell_words in new_words:
                    do_word = 'sell'
                    print('SELL')

            tologstr += (',' + do_word)

            new_words = new_words.replace('\n', '@')
            re_code = '.*([0 3 6][0][0-9][0-9][0-9][0-9]).*'

            test_code = re.match(re_code, new_words)
            print('xxx---------------------')
            print(new_words)
            print('xxx---------------------')
            print(test_code)
            print('xxx---------------------')
            if (test_code):
                do_code = test_code.group(1)

                new_words_no_code = new_words.replace(do_code, '')

                find_price = re.findall('\d+\.?\d*', new_words_no_code)

                if do_word == 'buy':
                    price_now = getprice(do_code)
                    print('ppp1------------' + price_now)

                    do_price = price_now
                    new_do_price = ''

                    for one_price in find_price:
                        print('ppp2------------' + one_price)
                        if abs(float(one_price) - float(price_now)) / float(price_now) < 0.11:
                            if new_do_price == '':
                                new_do_price = one_price
                            else:
                                if abs(float(one_price) - float(price_now)) < abs(
                                        float(new_do_price) - float(price_now)):
                                    new_do_price = one_price
                    if new_do_price != '':
                        do_price = new_do_price
                    tologstr += (',加钱之前的价格' + do_price)
                    do_price = str(round(float(do_price) + float(one_zb_config['buy_add_money']), 2))

                    tologstr += (',加钱之后的价格' + do_price)

                if do_word == 'sell':
                    do_price = getpricemin(do_code)

                print('价格:' + do_price)

                if do_word == 'buy':
                    do_amount_tmp = '1'
                    for one_amount_words in one_zb_config['amount_words']:
                        if one_amount_words in new_words:
                            do_amount_tmp = one_zb_config['amount_words'][one_amount_words]

                    one_money = float(one_zb_config['one_money'])
                    max_to_buy = one_money * float(do_amount_tmp) / float(do_price)
                    to_buy = int(max_to_buy / 100) * 100
                    do_amount = str(to_buy)
                    print(do_amount)

                    if (to_buy < 100):
                        max_to_buy_plus1 = one_money * (float(do_amount_tmp) + 1) / float(do_price)
                        to_buy_plus1 = int(max_to_buy_plus1 / 100) * 100
                        if (to_buy_plus1 < 100):
                            do_amount = ''
                            tologstr += (',触发逻辑 +100也买不起')
                            print('+100也买不起')
                        else:
                            do_amount = str(to_buy_plus1)
                            print('+100之后买得起')
                            tologstr += (',触发逻辑 +100之后买得起')

                    if ((float(do_amount_tmp) == 1) and do_amount != ''):
                        if ((one_money - float(do_amount) * float(do_price)) * 1.5 >= 100 * float(do_price)):
                            do_amount = str(int(do_amount) + 100)
                            print('闲置+100')
                            tologstr += (',触发逻辑 闲置 自动+100')

                    print('数量:' + do_amount)
                    tologstr += (',数量:' + do_amount)

                # if do_word == 'sell':
                #     update_zhangben()#sell之前 更新账本
                #     fp_zb=open('zhangben.data','r',encoding='utf-8')
                #     zhangben = json.loads(fp_zb.read())
                #     fp_zb.close()

                #     sell_flag = 0
                #     for one_record in zhangben:
                #         if one_record == do_code:
                #             sell_flag = 1
                #             do_amount = str(zhangben[one_record])
                #     if sell_flag == 0:
                #         do_amount = ''
                #         print('未持仓不用卖')
                #         tologstr += (',未持仓不用卖')

                if do_word == 'sell':
                    do_amount = '0'
            else:
                print('尝试匹配名字#sell')
                fp_zb_name = open('zhangben_name.data', 'r', encoding='utf-8')
                zhangben_name = json.loads(fp_zb_name.read())
                fp_zb_name.close()
                if fp_zb_name != {}:
                    for r_name_code in zhangben_name:
                        if zhangben_name[r_name_code] in new_words:
                            print('找到 ' + zhangben_name[r_name_code] + ' 代码 ' + r_name_code)
                            do_code = r_name_code
                            if do_word == 'sell':
                                do_price = getpricemin(do_code)

                            print('价格:' + do_price)
                            if do_word == 'sell':
                                do_amount = '0'
                            break
                print('尝试匹配名字#buy')
                if namecodedict != {}:
                    for r_name_code in namecodedict:
                        if namecodedict[r_name_code] in new_words:
                            print('找到 ' + namecodedict[r_name_code] + ' 代码 ' + r_name_code)
                            do_code = r_name_code

                            new_words_no_code = new_words.replace(do_code, '')
                            find_price = re.findall('\d+\.?\d*', new_words_no_code)

                            if do_word == 'buy':
                                price_now = getprice(do_code)
                                print('ppp1------------' + price_now)

                                do_price = price_now
                                new_do_price = ''

                                for one_price in find_price:
                                    print('ppp2------------' + one_price)
                                    if abs(float(one_price) - float(price_now)) / float(price_now) < 0.11:
                                        if new_do_price == '':
                                            new_do_price = one_price
                                        else:
                                            if abs(float(one_price) - float(price_now)) < abs(
                                                    float(new_do_price) - float(price_now)):
                                                new_do_price = one_price
                                if new_do_price != '':
                                    do_price = new_do_price
                                tologstr += (',加钱之前的价格' + do_price)
                                do_price = str(round(float(do_price) + float(one_zb_config['buy_add_money']), 2))

                                tologstr += (',加钱之后的价格' + do_price)

                            if do_word == 'buy':
                                do_amount_tmp = '1'
                                for one_amount_words in one_zb_config['amount_words']:
                                    if one_amount_words in new_words:
                                        do_amount_tmp = one_zb_config['amount_words'][one_amount_words]

                                one_money = float(one_zb_config['one_money'])
                                max_to_buy = one_money * float(do_amount_tmp) / float(do_price)
                                to_buy = int(max_to_buy / 100) * 100
                                do_amount = str(to_buy)
                                print(do_amount)

                                if (to_buy < 100):
                                    max_to_buy_plus1 = one_money * (float(do_amount_tmp) + 1) / float(do_price)
                                    to_buy_plus1 = int(max_to_buy_plus1 / 100) * 100
                                    if (to_buy_plus1 < 100):
                                        do_amount = ''
                                        tologstr += (',触发逻辑 +100也买不起')
                                        print('+100也买不起')
                                    else:
                                        do_amount = str(to_buy_plus1)
                                        print('+100之后买得起')
                                        tologstr += (',触发逻辑 +100之后买得起')

                                if ((float(do_amount_tmp) == 1) and do_amount != ''):
                                    if ((one_money - float(do_amount) * float(do_price)) * 1.5 >= 100 * float(
                                            do_price)):
                                        do_amount = str(int(do_amount) + 100)
                                        print('闲置+100')
                                        tologstr += (',触发逻辑 闲置 自动+100')

                                print('数量:' + do_amount)
                                tologstr += (',数量:' + do_amount)

                            break

            if do_word != '' and do_code != '' and do_price != '' and do_amount != '':
                dis_flag = 0
                for dis_word in one_zb_config['disable_words']:
                    if dis_word in ori_words:
                        dis_flag = 1
                        tologstr += (',检测到无关词')
                        print('检测到无关词')
                if dis_flag == 0:
                    namecodedict[do_code] = getname(do_code)
                    print('更新今天的股票代码名字对应')
                    print(namecodedict)
                    return [one_zb_config['enable'], do_word, do_code, do_price, do_amount, tologstr]
    return [-1, tologstr]


# def go_trader(do_action):
#     print('test')

def go_trader(action, code, price, amount):
    if action == 'buy':
        go_buy(code, float(price), int(amount))  # 注释则不操作
        print('调用股票软件买入', code, float(price), int(amount))
    if action == 'sell':
        # update_zhangben()
        fp_zb = open('zhangben.data', 'r', encoding='utf-8')
        zhangben = json.loads(fp_zb.read())
        fp_zb.close()

        sell_flag = 0
        for one_record in zhangben:
            if one_record == code:
                sell_flag = 1
                do_amount = str(zhangben[one_record])
        if sell_flag == 0:
            do_amount = ''
            print('未持仓不用卖')
        else:
            go_sell(code, float(price), int(do_amount))  # 注释则不操作
            print('调用股票软件卖出', code, float(price), int(do_amount))


def action_func(zb, ori_words):
    print(timestr() + '获取到' + zb + '原始指令如下')

    print(ori_words)
    print(timestr() + '原始指令结束')
    print(timestr() + '开始解析指令')
    do_action = goanalysys(zb, ori_words)
    if do_action[0] == -1:
        print(timestr() + '解析指令结束 未解析到操作')
        mylog(zb, '###分隔符开始###\n' + ori_words + ',' + '解析指令结束 未解析到操作' + do_action[1] + '###分隔符结束###\n')
    else:
        print(
            timestr() + '解析指令结束 已解析到操作：' + do_action[1] + '代码' + do_action[2] + '价格' + do_action[3] + '数量' + do_action[
                4])
        mylog(zb, '###分隔符开始###\n' + ori_words + ',' + '解析指令结束 已解析到操作' + do_action[1] + '代码' + do_action[2] + '价格' +
              do_action[3] + '数量' + do_action[4] + do_action[5] + '###分隔符结束###\n')
        if (do_action[0] == 0):
            print('已禁用该主播执行操作')
        else:
            print(
                timestr() + '下发执行操作到客户端：' + do_action[1] + '代码' + do_action[2] + '价格' + do_action[3] + '数量' + do_action[
                    4])
            go_trader(do_action[1], do_action[2], do_action[3], do_action[4])


def test_go():
    ori_words = '''2019-06-21 9:34:21 淘金尾盘股 服务中 欢迎加入(648296752)
【趋势型—兰博LS】
双塔食品(002481)
调出
7.81
1成仓
-----------------------------
【操作提示】
双塔食品 7.8左右反弹卖出 今天低开就弱了。
开盘买入 300256 星星科技 低价便宜创业板


'''
    zb = '567700379-2448009272'
    action_func(zb, ori_words)


def test_go_many():
    fgf = '@#￥#@'
    with open('testword.txt', 'r', encoding='UTF-8') as ff:
        all_words = ff.read()
        sp_all = all_words.split(fgf)
        for ori_words in sp_all:
            zb = '648296752'
            action_func(zb, ori_words)

        # zb = '648296752'
        # action_func(zb,sp_all[1])


app = flask.Flask(__name__)


# ori_words=''
@app.route('/ori_words', methods=['POST'])
def analysis():
    img_flag = flask.request.form['img_flag']
    if img_flag == 'yes':
        rimg = requests.get(flask.request.form['ori_words'])
        with open("tmpimg.jpg", "wb") as rimgfp:
            rimgfp.write(rimg.content)
        bd_r = img_to_str('tmpimg.jpg')

        bd_r_r = bd_r['words_result']
        ori_words = ""
        for i in bd_r_r:
            ori_words += i["words"] + "\n"


    else:
        ori_words = flask.request.form['ori_words']

    # ori_words = flask.request.form['ori_words']
    print(ori_words)
    zb = flask.request.form['zb']
    zb = flask.request.form['zb'].replace('|', '-')
    newtimere = re.match(r"(\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})", ori_words)
    action_flag = 1
    print('收到新的#########################################################')
    if newtimere:
        newtime = newtimere.groups()[0]
        ori_words = ori_words.replace(newtime, '')
        if newtime in timelist:
            action_flag = 0
            print('日期时间一样 不解析')
        else:
            timelist.append(newtime)
    if ori_words[:19]:
        x19 = ori_words[:19]
        if x19 in x19list:
            action_flag = 1
        #           print('前19一样 不解析')
        else:
            x19list.append(x19)
    if ori_words.replace('''</r/n>''', '').replace(' ', '')[-10:]:
        endx10 = ori_words.replace('''</r/n>''', '').replace(' ', '')[-10:]
        print('aaaaaaaaaaaaaaaaaaaaaa')
        print(endx10)
        print('aaaaaaaaaaaaaaaaaaaaaaend')
        if endx10 in endx10list:
            action_flag = 0
            print('去rn后10一样 不解析')
        else:
            endx10list.append(endx10)
    tnow = time.time()
    if tpanduan(tnow) == -1:
        #        action_flag = 0
        print('不执行时间')

    print('#######################timelist:')
    print(timelist)
    print('############actionflag:')
    print(action_flag)
    print('#######################flag end')
    if action_flag == 1:
        print('新内容')
        action_func(zb, ori_words)

    return '200 OK'


if __name__ == '__main__':
    test_flag = 0

    # update_zhangben()

    if test_flag == 0:
        print(timestr() + '程序启动')
        app.run(port=2333, debug=False)
    elif test_flag == 2:
        test_go_many()
    else:
        test_go()
