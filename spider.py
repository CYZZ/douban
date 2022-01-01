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
    # savepath = "../豆瓣电影.xls"
    # saveData(datalist, savepath)
    dbpath = "movie.db"
    save_data_to_db(datalist, dbpath)


# 影片的规则
findLink = re.compile(r'<a href="(.*?)">')  # 创建正则表达式对象，表示规则（字符串的模式）
# 影片图片的链接
findImgSrc = re.compile(r'<img.*src="(.*?)".*/>', re.S)
# 片名
findTitle = re.compile(r'<span class="title">(.*?)</span>')
# 评分
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*?)</span>')
# 评论人数
findJudge = re.compile(r'<span>(\d*)人评价</span>')
# 概况
findInq = re.compile(r'<span class="inq">(.*)</span>')
# 找到内容
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)  # re.S 用于加入默认的换行符


def getData(baseurl) -> [str]:
    datalist: [str] = []
    for i in range(0, 10):
        url = baseurl + str(i * 25)
        html = ask_url(url)
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div', class_='item'):  # div 标签里且class是item
            data = []
            item = str(item)

            # 获取到影片的超链接
            link = re.findall(findLink, item)[0]
            data.append(link)
            imgSrc = re.findall(findImgSrc, item)[0]
            data.append(imgSrc)
            titles = re.findall(findTitle, item)
            if len(titles) == 2:
                ctitle = titles[0]  # 添加中文名
                data.append(ctitle)
                otitle = titles[1].replace("/", "")  # 添加外国名
                data.append(otitle)
            else:
                data.append(titles[0])
                data.append(' ')  # 外国名留空白

            rating = re.findall(findRating, item)[0]
            data.append(rating)
            judgeNum = re.findall(findJudge, item)[0]
            data.append(judgeNum)

            inq = re.findall(findInq, item)

            if len(inq) > 0:
                data.append(inq[0].replace("。", ""))
            else:
                data.append(" ")

            bd = re.findall(findBd, item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?', " ", bd)  # 去掉 <br/>
            data.append(bd.strip())  # 去掉空格

            datalist.append(data)  # 把处理好的信息存入到datalist

        # print(datalist)
        # print(len(datalist))

    return datalist


def saveData(datalist: [[]], savepath: str):
    book = xlwt.Workbook(encoding="utf-", style_compression=0)
    sheet = book.add_sheet('豆瓣电影Top250', cell_overwrite_ok=True)  # 创建工作表
    col = ("电影详情链接", "图片链接", "影片中文名", "影片外国名", "评分", "评价数", "概况", "相关信息")
    for i in range(0, 8):
        sheet.write(0, i, col[i])
    for i in range(0, 250):
        print("第%d条", i)
        data = datalist[i]
        print("data=", data)
        for j in range(0, 8):
            sheet.write(i + 1, j, data[j])
    book.save(savepath)


def save_data_to_db(datalist, dbpath):
    init_db(dbpath)
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()
    # cur.execute(sql)
    for data in datalist:
        for index in range(len(data)):
            # if index == 4 or index == 5:
            #     continue
            data[index] = '"' + data[index] + '"'
        sql = '''
            insert into movie250 (
            info_link, pic_link,cname,ename,score,rated,instroduction,info)
            values(%s) ''' % ",".join(data)
        print(sql)
        cur.execute(sql)
        conn.commit()


def init_db(dbpath):
    sql = '''
        create table movie250
        (
        id integer primary key autoincrement,
        info_link txt,
        pic_link text,
        cname varchar,
        ename varchar,
        score numeric,
        rated numeric,
        instroduction text,
        info text
        )
    '''  # 创建数据表
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()


def ask_url(url):
    head = {
        "User-Agent": "Mozilla/5.0(Macintosh; Intel Mac OSX 10_15_7) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 96.0.4664.110 Safari / 537.36 Edg / 96.0.1054.62",
        "Referer": "https://open.weixin.qq.com/",
        'Cookie': 'bid=bD7qFO7cqtA; douban-fav-remind=1; ll="108296"; _pk_id.100001.4cf6=98d1af7a53fc4078.1640867976.1.1640867976.1640867976.; dbcl2="221590280:d6iEaGmcz1A"; ck=BGO3; push_noty_num = 0; push_doumail_num=0'
    }
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        print(e)
    return html


if __name__ == "__main__":
    main()
