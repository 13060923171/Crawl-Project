import requests
from lxml import etree
import json
import time
import threading
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.62 Safari/537.36"
}
News_set = set()
#单线程版，获取网易新闻里面新冠肺炎的实时数据
def getData():
    url = "https://wp.m.163.com/163/page/news/virus_report/index.html?_nw_=1&_anw_=1"
    html = requests.get(url,headers=headers)
    soup = etree.HTML(html.text)
    #先是获取相应数据，这里是时间和数据
    current_time =soup.xpath('//div[@class = "cover_time"]/text()')[0]
    cover_data = soup.xpath('//div[@class = "cover_data_china"]/div[starts-with(@class,"cover")]')
    #开始一个无限循环
    while 1:
        #进行不断爬取，从而达到我们的目的，实时获取数据
        for cover in cover_data:
            title = cover.xpath('h4/text()')[0]
            number = cover.xpath('div[@class = "number"]/text()')[0]
            result = current_time+" "+title+" "+ number
            if result not in News_set:
                News_set.add(result)
                print(result,end=" ")
                #间隔时间为60秒
        time.sleep(60)
#多线程版，百度版新冠肺炎实时数据
def getNews():
    url = "https://opendata.baidu.com/data/inner?tn=reserved_all_res_tn&dspName=iphone&from_sf=1&dsp=iphone&resource_id=28565&alr=1&query=%E8%82%BA%E7%82%8E&cb=jsonp_1588237477067_8878"
    html = requests.get(url,headers=headers)
    html_text = html.text
    #用获取json开始的位置
    start = html_text.find('{"ResultCode"')
    #获取json末尾的位置
    end = html_text.find(r'recall_srcids\u0000\u0000"}')+len(r'recall_srcids\u0000\u0000"}')
    #把json给拼接起来，并且把json转化为python的形式
    json_data = json.loads(html_text[start:end])
    #最新的数据，用json来定位
    data_new = json_data['Result'][0]["DisplayData"]["result"]['items']
    #写一个循环函数来达到我们的目的
    while 1:
        for data in data_new:
            new_title = data["eventDescription"]
            new_time = data["eventTime"]
            new_url = data['eventUrl']
            local_time = time.localtime(int(new_time))
            current_time = time.strftime("%Y-%m-%d %H-%M-%S",local_time)
            result = new_title+current_time+" "+new_url
            if result not in News_set:
                News_set.add(result)
                print(result)
        time.sleep(60)
def xingXi():
    print("新冠肺炎情况：")
    #单线程开启网易新闻的新冠肺炎的实时情况
    print("实时新闻:")
    getNews()
    #多线程开启百度新冠肺炎的实时情况
    print("百度提供实时新闻")
    threading.Thread(target=getNews().start())

if __name__ == '__main__':
    xingXi()
