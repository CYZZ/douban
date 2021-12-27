import bs4
import re  # 正则表达式
import urllib.request, urllib.error
import xlwt
import sqlite3

response = urllib.request.urlopen("https://www.baidu.com")
print(response.read().decode('utf-8'))
