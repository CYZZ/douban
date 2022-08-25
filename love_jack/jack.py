from math import fabs
import clipboard
import requests
from typing import Iterable

def request_ulist_stocks(secids: Iterable[str]):
        """
        获取多个股票的收盘价
        secids: 股票代码, ctye.code例如([0.002466])

        """
        url = "https://push2.eastmoney.com/api/qt/ulist.np/get"

        params = {
            "secids": ",".join(secids),
            "fields": "f3,f12,f14,f1,f2,f4",
            "fltt": 2,
            "invt": 2,
            "_": "1657945282430"
        }
        response = requests.get(url,  params=params).json()
        return [obj["f2"] for obj in response["data"]["diff"]]

def getStockData(follower, diff):
    codes = ["1.601012", "0.000776", "0.300750"]

    obj = request_ulist_stocks(codes)

    out_str = "每日统计：\n"
    ninde_highest = 692
    ninde_close = obj[2]
    ninde_str = "  跌的跟狗一样只值350乌云盖顶新能源宁德时代距历史最高点回撤：({high:.2f}-{close:.2f})/{high:.2f}={rate:.2f}%\n"
    ninde_str = ninde_str.format(high=ninde_highest, close=ninde_close,
                                rate=(ninde_highest - ninde_close) / ninde_highest * 100)

    longji_highest = 73.6
    longji_close = obj[0]
    longji_str = "  严重破位快逃命隆基绿能距历史最高点回撤：({high:.2f}-{close:.2f})/{high:.2f}={rate:.2f}%\n"
    longji_str = longji_str.format(high=longji_highest, close=longji_close,
                                rate=(longji_highest - longji_close) / longji_highest * 100)

    guangfa_highest = 26.72
    guangfa_close = obj[1]
    guangfa_str = "  广● 横盘代替下跌●铁底跌无可跌●券商蛇王●足足七年没有行情●北交所圣经之子●全面注册制大利好●庄家跟杰克做对手盘●发证券距去年最高点回撤：({high:.2f}-{close:.2f})/{high:.2f}={rate:.2f}%\n"
    guangfa_str = guangfa_str.format(high=guangfa_highest, close=guangfa_close,
                                    rate=(guangfa_highest - guangfa_close) / guangfa_highest * 100)
    end_str = "  待广发超越宁隆十个点两个月后便不再统计。\n  (请●所有券商人起立，在评论区集合，{}粉丝联名杰克清仓剩下持仓！)\n"
    end_str = end_str.format(follower)
    diff = "  粉丝做T成就:较上期统计" + ("增加" if diff > 0 else "减少") + str(abs(diff)) + "人"
    clipboard.copy(out_str + ninde_str + longji_str + guangfa_str + end_str + diff)
    print(clipboard.paste())

def getJackFollower():
    url = "https://api.bilibili.com/x/relation/stat"
    params = {
        "vmid":2142101977,
        "jsonp":"jsonp"
    }
    response = requests.get(url,params=params).json()
    print(response)
    return response['data']['follower']

def str_of_num(num: int):
    '''
    递归实现，精确为最大单位值 + 小数点后三位
    '''
    def strofsize(num, level):
        if level >= 2:
            return num, level
        elif num >= 10000:
            num /= 10000
            level += 1
            return strofsize(num, level)
        else:
            return num, level
    units = ['', '万', '亿']
    num, level = strofsize(num, 0)
    if level > len(units):
        level -= 1
    return '{}{}'.format(round(num, 3), units[level])

if __name__ == '__main__':
    follwer = getJackFollower()
    obj = str_of_num(follwer)
    # pre_follwer = 187023
    pre_follwer = 186975 # 传入上期统计的数据
    diff = follwer - pre_follwer
    getStockData(obj, diff)

# 每日统计：
#        跌的跟狗一样只值350乌云盖顶新能源宁德时代距历史最高点回撤：（692-493.55）/692=28.67%
#        严重破位快逃命隆基股份距历史最高点回撤：（103.3-80.51）/103.3=22.06%
#       广● 横盘代替下跌●铁底跌无可跌●券商蛇王●足足七年没有行情●北交所圣经之子●全面注册制大利好●庄家跟杰克做对手盘●发证券距去年最高点回撤：（27.22-17.14）/27.22=37.03%
#      待广发超越宁隆十个点两个月后便不再统计。
#   （请●所有券商人起立，在评论区集合，二十万粉丝联名杰克清仓剩下持仓！
