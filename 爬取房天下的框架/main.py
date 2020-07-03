import requests
from lxml import etree
import re
#获取连接需要用到的
from urllib import parse
#判断是否连接正确用到的
import logging
#调用我们的多线程和多进程
from concurrent.futures import ProcessPoolExecutor,ThreadPoolExecutor
#连接数据库，并且把数据储存到数据库里面
from shujuku import sess,House

#定义我们的headers请求头，用于伪装
headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        'cookie': 'global_cookie=80ezxa0k3wcub77m99wr791kw18kbvumxyn; fang_hao123_layed=1; integratecover=1; g_sourcepage=zf_fy%5Elb_pc; __utmc=147393320; city=gz; ASP.NET_SessionId=prdsdu5v3woxvlrafi4wr32a; keyWord_recenthousegz=%5b%7b%22name%22%3a%22%e7%99%bd%e4%ba%91%22%2c%22detailName%22%3a%22%22%2c%22url%22%3a%22%2fhouse-a076%2f%22%2c%22sort%22%3a1%7d%5d; Captcha=32684870505770397A38634E33774A525034374964615650397858356D577A4E664475386933586A304A6835784A76696F4D574B4B51547A573442393562527666304836557954436A64413D; unique_cookie=U_80ezxa0k3wcub77m99wr791kw18kbvumxyn*4; __utma=147393320.1634598515.1593155184.1593155184.1593157145.2; __utmz=147393320.1593157145.2.2.utmcsr=gz.zu.fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmt_t0=1; __utmt_t1=1; __utmt_t2=1; __utmb=147393320.3.10.1593157145',
        'referer': 'https://gz.zu.fang.com/',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Connection': 'keep-alive'
    }
#长连接，就是把几个请求连接起来变成一个，防止对那个网站损害太大
session = requests.session()
session.headers = headers

#先写一个判断函数，是否get成功
def get_index(url):
    html = session.get(url,headers = headers)
    if html.status_code == 200:
        get_data(html)
    else:
        print("请求页面{}出错".format(url))
#获取我们想要获取的数据
def get_data(html):
    #页数是根据它给出来的URL来构造的
    pages = get_pages(html)
    if not pages:
        pages=1
    #根据它的页数，用一个循环函数把它给叠带出来
    urls =['https://gz.zu.fang.com/house-a078/i3%d/'%i for i in range(1,pages+1)]
    #因为是爬取页面信息，所以用我们的多线程去爬
    with ThreadPoolExecutor(max_workers =5)as t:
        for url in urls:
            print('crawl page {}'.format(url))
            #多线程调用函数的固定格式
            t.submit(get_data_next,url)
#判断这个URL有多少页
def get_pages(html):
    #用到的是xpath语法
    soup = etree.HTML(html.text)
    pages = soup.xpath('//div[@class = "fanye"]/span[@class = "txt"]/text()')
    number = get_number(pages[0])
    if number:
        #获取成功之后返还一个页面的数字
        return int(number)
    return None
#根据URL去获取它页面对应的数字，因为每一页对应的数字
def get_number(text):
    number = re.compile('\d+')
    return number.findall(text)[0]
#获取首页里面的全部信息
def get_data_next(url):
    html = session.get(url)
    soup = etree.HTML(html.text)
    contents = soup.xpath('//div[@class = "houseList"]/dl')
    for content in contents:
        try:
            block = content.xpath('dd/p[@class = "gray6 mt12"]/text()')[0]
            title = content.xpath('dd/p/a/text()')[0]
            rent = content.xpath('dd/div/p/span[@class = "price"]/text()')[0]
            href = parse.urljoin('https://gz.zu.fang.com/',content.xpath('dd/p[@class = "title"]/a/@href')[0])
            get_house_data(href,rent,title,block)
        except IndexError as e:
            print('content error')

#并且进一步获取它页面里每一个房子的信息
def get_house_data(href,*args):
    #这里因为涉及到反爬虫机制，我们用到了跳转机制，跳了2次才来到我们真正需要的页面
    url = 'http://search.fang.com/captcha-baac44ca368c9f491e/redirect?h='+href
    html = session.get(url)
    content = html.text
    #用到正则表达式去获取url的连接
    location_url = re.compile('location.href="(.*?)"')
    #把URL打印出来
    next_url = location_url.findall(content)[0]
    #判断这个URL是否是正确的
    logging.captureWarnings(True)
    #无视证书要求
    html = session.get(next_url, verify=False)
    second_url = location_url.findall(html.text)[0]
    #获取最终url
    html = session.get(second_url)
    #然后开始我们爬虫最拿手的获取信息了
    soup = etree.HTML(html.text)
    liandian = soup.xpath(
        '//div[@class = "mscont"]/ul/li[@class = "font14 fyld"]/div[@class = "fyms_con floatl gray3"]/text()')
    if liandian:
        liandian = "|".join(liandian)
    else:
        print("无信息")
    jieshao = soup.xpath(
        '//div[@class = "mscont"]/ul/li[@class = "font14 xqjs"]/div[@class = "fyms_con floatl gray3"]/text()')
    if jieshao:
        jieshao = "|".join(jieshao)
    else:
        print("无信息")
    tiaojian = soup.xpath(
        '//div[@class = "mscont"]/ul/li[@class = "font14 zbpt"]/div[@class = "fyms_con floatl gray3"]/text()')
    if tiaojian:
        tiaojian = "|".join(tiaojian)
    else:
        print("无信息")
    traffic = soup.xpath(
        '//div[@class = "mscont"]/ul/li[@class = "font14 jtcx"]/div[@class = "fyms_con floatl gray3"]/text()')
    if traffic:
        traffic = "|".join(traffic)
    else:
        print("无信息")
    fuzeren = soup.xpath(
        '//div[@class = "mscont"]/ul/li[@class = "font14 fwjs"]/div[@class = "fyms_con floatl gray3"]/text()')[0].strip()
    if fuzeren:
        fuzeren = "|".join(fuzeren)
    else:
        print("无信息")
    print("房源亮点：{}\n".format(liandian),"小区介绍：{}\n".format(jieshao),"周边配套：{}\n".format(tiaojian),"交通出行：{}\n".format(traffic),"服务介绍：{}\n".format(fuzeren))
    try:
        #这里用到防错机制，因为有一些房子可能没有信息
        house = House(
            #第一个是你数据库的名字，第二个就是存进入的信息
            block = args[2],
            title = args[1],
            rent = args[0],
            data=liandian,
            data2=jieshao,
            data3=tiaojian,
            data4=traffic,
            data5=fuzeren
        )
        #全部增加到数据库里面
        sess.add(house)
        #连接数据库
        sess.commit()
        print('commit')
        #如果失败了启动回滚
    except Exception as e:
        print('rollback',e)
        sess.rollback()


def main():
    #获取地区的连接，这个也是根据网页的URL来模拟的
    urls = ["https://gz.zu.fang.com/house-a0{}/".format(i) for i in range(70,81)]
    #然后开启我们的多进程来对每个地方不同的区进行分开爬取，来提高爬取速度
    with ProcessPoolExecutor(max_workers =4)as p:
        for url in urls:
            p.submit(get_index,url)

if __name__ == '__main__':
    main()
    session.close()
