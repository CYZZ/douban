# -*- codeing = utf-8 -*-
from bs4 import BeautifulSoup
import re
import urllib.request, urllib.error
import xlwt
import sqlite3


def main():
    baseurl = "https://movie.douban.com/top250?start="
    # 爬取网页
    datalist = getData(baseurl)
    # 解析数据
    # 3保存数据
    savepath = "testpath"
    saveData(savepath)


def getData(baseurl) -> [str]:
    datalist: [str] = []
    return datalist


def saveData(savepath: str):
    pass


if __name__ == "__main__":
    main()
