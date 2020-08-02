import requests
from lxml import etree
import concurrent.futures
from urllib import parse
import time
import re
import math
headers = {
    "cookie": "_T_WM=a96578de569de43753db540a141c819b; SUB=_2A25yEo2TDeRhGeNN6lsS-CrJyz-IHXVR_BPbrDV6PUJbkdANLWPgkW1NSdnQVCGHLFRbfwvsOXKxEDeKwzQ-OeZj; SUHB=04WuxbFN8-tkwi",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
}

#统一使用一个headers减轻服务器压力
session = requests.session()
session.headers = headers

def get_statua(i):
    #读取当前页面信息
    url = 'https://weibo.cn/2656274875/profile?keyword=%E8%82%BA%E7%82%8E&hasori=0&haspic=0&starttime=20200101&endtime=20200726&advancedfilter=1&page={}'.format(i)
    html = session.get(url)
    if html.status_code == 200:
        print("页面正常")
        get_html(html)
    else:
        print(html.status_code)


def get_html(html):
    content = html.text
    soup = etree.HTML(content.encode('utf-8'))

    # shijian = soup.xpath('//span[@class = "ct"]/text()')
    # for s in shijian:
    #     print(s.replace("来自微博 weibo.com","").replace("来自微博云剪","").replace("来自微博原生直播",""))
    #     time_txt(s)
    # titles = soup.xpath('//span[@class = "ctt"]')
    # for title in titles:
    #     biaoti = title.xpath("./a/text()")[0]
    #     print(biaoti)
    #     shijina_txt(biaoti)
    #定位当前页面的转发
    urls = soup.xpath('//div[@class = "c"]')
    for url in urls[:-2]:
        #获取他的转发次数
        neirong = url.xpath("./div/a/text()")[-3].replace("转发[","").replace("]","")
        #获取它的URL
        hrefs = url.xpath("./div/a/@href")[-3]
        #获取他的页数，页数是等于转发次数除以10加1就是总的转发页数了
        yeshu = int(neirong)//10
        print(yeshu,hrefs)
        # href = " https://weibo.cn/repost/JcH5N1ftY?uid=2656274875&rl=1"
        # with concurrent.futures.ThreadPoolExecutor(max_workers = 10)as e:
        #     futures = [e.submit(get_pinglun,href,yeshu)]
        #     for futuer in concurrent.futures.as_completed(futures):
        #         print(futuer.result())

def get_pinglun(href,yeshu):
    try:
        #根据获取的转发URL进入到转发里面
        for i in range(1,int(yeshu)+1):
            url = "{}&page={}".format(href,i)
            html = session.get(url)
            content = html.text
            soup = etree.HTML(content.encode('utf-8'))
            names = soup.xpath('//div[@class = "c"]')
            #从而获取转发人的名字
            for name in names[3:-1]:
                title = name.xpath('./a/text()')[0]
                print(title,end=",")
                one_zhuanfa(title)
    except:
        pass

def time_txt(time):
    with open("time.txt","a+",encoding="utf-8")as f:
        f.write(time+"\n")
        print("写入成功")
def shijina_txt(shijina):
    with open("shijian.txt","a+",encoding="utf-8")as f:
        f.write(shijina+"\n")
        print("写入成功")

def one_zhuanfa(title):
    with open("diyichizhuanfa.txt","a+",encoding="utf-8")as f:
        f.write(title+",")

        print("写入成功")

if __name__ == '__main__':
    # with concurrent.futures.ProcessPoolExecutor(max_workers = 5)as e:
    #     futures = [e.submit(get_statua,2)]
    #     for futuer in concurrent.futures.as_completed(futures):
    #         print(futuer.result())
    get_statua(6)
