#!/usr/bin/env python
# encoding: utf-8
'''
@author: taiyc
@file: FTXSpider
@time: 2019/7/28 0:23
'''

import requests, time, re, os, xlsxwriter, openpyxl
import pandas as pd
from datetime import datetime
from lxml.html import etree
from requests.cookies import RequestsCookieJar
from multiprocessing.dummy import Pool as ThreadPool  # 线程池
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import re



class FTXSpider(object):
    def __init__(self):
        self.start_urls = pd.read_excel('zufangcitymatch.xlsx')['https'][0:82]
        self.quchong = {}
        self.cookies = RequestsCookieJar()
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                                      ' (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
        self.cookies1 = {
            # 'Captcha': '754E4D4C6C3454576165636C4F786A793030484B7875746246667043665230336E67495A783976326A63564C56503765366D4E47384F495370303938534C627A567934485735562B5636343D',
           # 'global_cookie': '85twvihds1cqccau5cnwwlrhn20jyo3nlrm',
            #'unique_cookie': 'U_85twvihds1cqccau5cnwwlrhn20jyo3nlrm*6',
            'global_cookie': '2a8hamrvwdz0punlkee3ifojo26jyqn1d1y',
            'unique_cookie': 'U_2a8hamrvwdz0punlkee3ifojo26jyqn1d1y*1',
            'city': 'www',
            'vh_newhouse': '',
            'logGuid': '',
            'g_sourcepage': '',
            'Integrateactivity': ''
             }
        self.excel_head = ['date','city','tupian', 'price', 'renttype', 'shiting', 'mianji', 'chaoxiang', 'xiaqu', 'jiedao', 'xiaoqu', 'jiaotong']
        self.today_str = datetime.strftime(datetime.now(), '%Y-%m-%d')
    def get_html(self, url):
        browser.get(url)
        time.sleep(3)
        html = browser.page_source
        return html
        # # self.headers['Referer'] = url
        # # self.headers['Cookie'] = getcookie(url)
        # headers = {'Cookie':getcookie(url),
        #            'Refer':url,
        #            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3724.8 Safari/537.36'}
        # try:
        #     response = requests.get(url, headers=headers, timeout=3, allow_redirects=False)#, cookies=self.cookies1)
        # except:
        #     time.sleep(2)
        #     return self.get_html(url)
        # if response.status_code == 200:
        #     return response.content.decode('gb2312', errors='ignore')
        # elif response.status_code == 403:
        #     print(response.status_code)
        #     time.sleep(1)
        #     return self.get_html(url)
        # elif response.status_code == 302:
        #     print(url)
        #     print('cookies失效')
        #     html = browser.page_source
        #     return html
        # else:
        #     time.sleep(1)
        #     print(response.status_code)
        #     return self.get_html(url)

    def parse(self, current_city_url, html, city_name):
        file_name = f'租房{self.today_str}/{city_name}{self.today_str}房天下租房.xlsx'
        if not os.path.exists(file_name):
            wb = openpyxl.Workbook()
            ws = wb.worksheets[0]
            self.save_to_excel(ws, 0, self.excel_head)
            wb.save(file_name)
        wb = openpyxl.load_workbook(file_name)
        ws = wb.worksheets[0]
        next_url = True
        row_count = 1
        while next_url:
            html_eles = etree.HTML(html)
            # 获取下一页
            next_url = html_eles.xpath('//a[text()="下一页"]/@href')
            next_url = current_city_url + next_url[0][1:] if next_url else None
            # 获取网页houseList类所有租房信息
            house_eles = html_eles.xpath('//div[@class="houseList"]/dl')
            # 遍历每个房子获取租房信息
            for house_ele in house_eles:
                # 获取房子id（用于去重）
                house_id = house_ele.xpath('./dd/p[1]/a/@href')
                if house_id:  # 图片数量不存在说明，是广告，不做处理
                    try:
                        house_id = house_id[0].split('/')[-1].split('.')[0]  # 简化id
                        # 图片数量
                        tupian = house_ele.xpath('.//span[@class="iconImg"]/text()')[0]
                        # 价格
                        price = house_ele.xpath('.//span[@class="price"]/text()')[0]
                        # renttype/shiting/mianji/chaoxiang
                        main_info = [re.sub('\r|\n| |', '', field).replace('�O', '㎡') for field in
                                     house_ele.xpath('./dd/p[2]//text()') if field != '|']
                        if len(main_info) != 4:
                            continue
                        renttype = main_info[0]
                        shiting = main_info[1]
                        mianji = main_info[2]
                        chaoxiang = main_info[3]
                        # 辖区、 街道、小区名
                        position_info = [field for field in house_ele.xpath('./dd/p[3]/a/span/text()')]
                        if len(position_info) != 3:
                            continue
                        xiaqu = position_info[0]
                        jiedao = position_info[1]
                        xiaoqu = position_info[2]
                        jiaotong = ''.join(house_ele.xpath('.//span[@class="note subInfor"]//text()'))
                        jiaotong = jiaotong if jiaotong else '无'
                    except:
                        pass
                    else:
                        if row_count > 3000:
                            wb.save(file_name)
                            return
                        if house_id not in self.quchong[city_name]:
                            # print(house_id, tupian, price, renttype, shiting, mianji, chaoxiang, xiaqu, jiedao, xiaoqu, jiaotong)
                            print(f'正在爬取:{city_name}-->第{row_count}条租房信息', )
                            # 保存数据

                            self.save_to_excel(ws, row_count, [self.today_str,city_name,tupian, price, renttype, shiting, mianji, chaoxiang, xiaqu, jiedao, xiaoqu,jiaotong,])
                            row_count += 1
                            self.quchong[city_name].append(house_id)  # 将爬取过的房子id放进去，用于去重
                        else:
                            print('已存在')
            if next_url:
                html = self.get_html(next_url)
        wb.save(file_name)

    def run_spider(self, city_url_list):
        for city_url in city_url_list:
            try:
                current_city_url = city_url
                html = self.get_html(city_url)
                print(city_url)
                city_name = re.findall(re.compile('class="s4Box"><a href="#">(.*?)</a>'), html)[0]  # 获取城市名
                self.quchong[city_name] = []  # 构建{'城市名': [租房1,2,3,4,]}用于去重
                self.parse(current_city_url, html, city_name)
            except:
                pass

    # 数组拆分 (将一个大元组拆分多个小元组，用于多线程任务分配)
    def div_list(self, ls, n):
       result = []
       cut = int(len(ls)/n)
       if cut == 0:
           ls = [[x] for x in ls]
           none_array = [[] for i in range(0, n-len(ls))]
           return ls+none_array
       for i in range(0, n-1):
           result.append(ls[cut*i:cut*(1+i)])
       result.append(ls[cut*(n-1):len(ls)])
       return result

    def save_to_excel(self, ws, row_count, data):
        for index, value in enumerate(data):
            ws.cell(row=row_count+1, column=index + 1, value=value)  # openpyxl 是以1，开始第一行，第一列

if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # options.add_argument('--headless')
    browser = webdriver.Chrome(options=options,executable_path='chromedriver.exe')
    wait = WebDriverWait(browser, 10)
    spider = FTXSpider()
    if not os.path.exists(f'租房{spider.today_str}'):
        os.mkdir(f'租房{spider.today_str}')
    pool = ThreadPool(1)  # 创建一个包含5个线程的线程池
    pool.map(spider.run_spider, spider.div_list(spider.start_urls, 1))
    pool.close()  # 关闭线程池的写入
    pool.join()  # 阻塞，保证子线程运行完毕后再继续主进程



    # 单线程
    # for city_url in spider.start_urls:
    #     spider.run_spider([city_url])

