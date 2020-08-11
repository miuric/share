import datetime
import random
import string
from urllib import request
from uuid import uuid5, NAMESPACE_X500

UUID = lambda x: str(uuid5(NAMESPACE_X500, str(x) + str(datetime.datetime.now()) + ''.join(
    random.sample(string.ascii_letters + string.digits, 8))))


def get_price_min(code):  # 最低价
    url_base = "http://qt.gtimg.cn/q="
    if code[0] == '6':
        url = url_base + 'sh' + code
    else:
        url = url_base + 'sz' + code
    req = request.Request(url)
    response = request.urlopen(req)
    page = response.read().decode('gbk')
    data = page.split('~')
    return data[48]


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
    return data[3]
