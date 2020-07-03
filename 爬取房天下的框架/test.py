import requests
import re
import logging
from lxml import etree
from urllib import parse
from shujuku import sess,House
# url1 ="https://gz.zu.fang.com/chuzu/3_249354911_1.htm"
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    'cookie': 'global_cookie=80ezxa0k3wcub77m99wr791kw18kbvumxyn; fang_hao123_layed=1; integratecover=1; g_sourcepage=zf_fy%5Elb_pc; __utmc=147393320; city=gz; ASP.NET_SessionId=prdsdu5v3woxvlrafi4wr32a; keyWord_recenthousegz=%5b%7b%22name%22%3a%22%e7%99%bd%e4%ba%91%22%2c%22detailName%22%3a%22%22%2c%22url%22%3a%22%2fhouse-a076%2f%22%2c%22sort%22%3a1%7d%5d; Captcha=32684870505770397A38634E33774A525034374964615650397858356D577A4E664475386933586A304A6835784A76696F4D574B4B51547A573442393562527666304836557954436A64413D; unique_cookie=U_80ezxa0k3wcub77m99wr791kw18kbvumxyn*4; __utma=147393320.1634598515.1593155184.1593155184.1593157145.2; __utmz=147393320.1593157145.2.2.utmcsr=gz.zu.fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmt_t0=1; __utmt_t1=1; __utmt_t2=1; __utmb=147393320.3.10.1593157145',
    'referer': 'https://gz.zu.fang.com/',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Connection': 'keep-alive'
}
# location_url = re.compile('location.href="(.*?)"')
session = requests.session()
session.headers = headers
def get_data_next():
    url = 'https://gz.zu.fang.com/house-a078/?rfss=2-25c88db39d1d1fcc5e-86#'
    html = session.get(url)
    soup = etree.HTML(html.text)
    contents = soup.xpath('//div[@class = "houseList"]/dl')
    for content in contents:
        try:
            block = content.xpath('dd/p[@class = "gray6 mt12"]/text()')[0]
            title = content.xpath('dd/p/a/text()')[0]
            rent = content.xpath('dd/div/p/span[@class = "price"]/text()')[0]
            href = parse.urljoin('https://gz.zu.fang.com/',content.xpath('dd/p[@class = "title"]/a/@href')[0])
            get_house_data(href,block)
        except IndexError as e:
            print('content error')
        # try:
        #     house = House(
        #         block=block,
        #         title=title,
        #         rent=rent,
        #     )
        #     sess.add(house)
        #     sess.commit()
        #     print('commit')
        # except Exception as e:
        #     print('rollback', e)
        #     sess.rollback()

def get_house_data(url,block):
    url = 'http://search.fang.com/captcha-baac44ca368c9f491e/redirect?h='+url
    html = session.get(url)
    content = html.text
    location_url = re.compile('location.href="(.*?)"')
    next_url = location_url.findall(content)[0]
    logging.captureWarnings(True)
    html = session.get(next_url, verify=False)
    second_url = location_url.findall(html.text)[0]
    html = session.get(second_url)
    soup = etree.HTML(html.text)
    liandian = soup.xpath(
        '//div[@class = "mscont"]/ul/li[@class = "font14 fyld"]/div[@class = "fyms_con floatl gray3"]/text()')
    if liandian:
        liandian = "|".join(liandian)
    else:
        print("无信息")
    # jieshao = soup.xpath(
    #     '//div[@class = "mscont"]/ul/li[@class = "font14 xqjs"]/div[@class = "fyms_con floatl gray3"]/text()')
    # if jieshao:
    #     jieshao = "|".join(jieshao)
    # else:
    #     print("无信息")
    # tiaojian = soup.xpath(
    #     '//div[@class = "mscont"]/ul/li[@class = "font14 zbpt"]/div[@class = "fyms_con floatl gray3"]/text()')
    # if tiaojian:
    #     tiaojian = "|".join(tiaojian)
    # else:
    #     print("无信息")
    # traffic = soup.xpath(
    #     '//div[@class = "mscont"]/ul/li[@class = "font14 jtcx"]/div[@class = "fyms_con floatl gray3"]/text()')
    # if traffic:
    #     traffic = "|".join(traffic)
    # else:
    #     print("无信息")
    # fuzeren = soup.xpath(
    #     '//div[@class = "mscont"]/ul/li[@class = "font14 fwjs"]/div[@class = "fyms_con floatl gray3"]/text()')[0].strip()
    # if fuzeren:
    #     fuzeren = "|".join(fuzeren)
    # else:
    #     print("无信息")
    # print("房源亮点：{}\n".format(liandian),"小区介绍：{}\n".format(jieshao),"周边配套：{}\n".format(tiaojian),"交通出行：{}\n".format(traffic),"服务介绍：{}\n".format(fuzeren))
    try:
        house = House(
            block = block,
            data = liandian
        )
        sess.add(house)
        sess.commit()
        print('commit')
    except Exception as e:
        print('rollback',e)
        sess.rollback()
if __name__ == '__main__':
    get_data_next()
# url = 'http://search.fang.com/captcha-baac44ca368c9f491e/redirect?h='+url1
# html = session.get(url)
# content1 = html.text
# next_url = location_url.findall(content1)[0]
#
# logging.captureWarnings(True)
# html = session.get(next_url,verify=False)
# second_url = location_url.findall(html.text)[0]
# html = session.get(second_url)
# soup = etree.HTML(html.text)
# # contexts = soup.xpath('//div[@class = "mscont"]/ul')
# # for context in contexts:
# #     try:
# #         liandian = context.xpath('li[@class = "font14 fyld"]/div[@class = "fyms_con floatl gray3"]/text()')
# #         jieshao = context.xpath('li[@class = "font14 xqjs"]/div[@class = "fyms_con floatl gray3"]/text()')
# #         tiaojian = context.xpath('li[@class = "font14 zbpt"]/div[@class = "fyms_con floatl gray3"]/text()')
# #         traffic = context.xpath('li[@class = "font14 jtcx"]/div[@class = "fyms_con floatl gray3"]/text()')
# #         fuzeren = context.xpath('li[@class = "font14 fwjs"]/div[@class = "fyms_con floatl gray3"]/text()')[0].strip()
# #         print("房源亮点：{}\n".format(liandian),"小区介绍：{}\n".format(jieshao),"周边配套：{}\n".format(tiaojian),"交通出行：{}\n".format(traffic),"服务介绍：{}\n".format(fuzeren))
# #     except:
# #         print("没有相关内容")
#
#
# results = soup.xpath(
#     '//div[@class = "mscont"]/ul/li[@class = "font14 fyld"]/div[@class = "fyms_con floatl gray3"]/text()')
# if results:
#     results = "|".join(results)
# else:
#     print("无信息")
# jieshao = soup.xpath(
#     '//div[@class = "mscont"]/ul/li[@class = "font14 xqjs"]/div[@class = "fyms_con floatl gray3"]/text()')
# if jieshao:
#     results = "|".join(jieshao)
# else:
#     print("无信息")
# try:
#     house = House(
#         data = results+jieshao
#
#     )
#     sess.add(house)
#     sess.commit()
# except Exception as e:
#     sess.rollback()
