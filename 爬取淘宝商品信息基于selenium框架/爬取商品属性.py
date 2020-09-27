from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from urllib.parse import quote
from pyquery import PyQuery
import time
import pandas as pd
import requests
from  urllib import parse
import json

#定义一个变量，最好用大写这个是约定俗成
KEYWORD = input("请输入要搜索的关键词:")
#定位Chromedriver这个工具的位置
options = webdriver.ChromeOptions()
options.add_experimental_option("prefs",{"profile.mamaged_default_content_settings.images":2})
options.add_experimental_option('excludeSwitches',['enable-automation'])
browser = webdriver.Chrome(executable_path="C:\\Users\\96075\\Desktop\\全部资料\\Python\\爬虫\\chromedriver.exe",options=options)
#设置等待时间
wait = WebDriverWait(browser,10)

list_property = []

def crawl_page(page):
    try:
        #爬取这个页面，quote的作用就是将我们输入的文字转化成计算机看得懂的文字
        url = "https://s.taobao.com/search?q="+quote(KEYWORD)
        #然后用我们的工具去获取这个页面的信息
        browser.get(url)
        time.sleep(5)
        #如果页面大于1，则执行下一步
        if page>1:
            #先是定位到下一页的位置，这里我们用到的是selenium语法
            page_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"input.input.J_Input")))
            #然后点击按钮，实现页面跳转
            sumbit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"span.btn.J_Submit")))
            #然后关闭
            page_box.clear()
            #发送页数到page这个参数里面
            page_box.send_keys(page)
            #停止点击事件
            sumbit_button.click()
        #等待这个页面的施行
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".m-itemlist .items .item")))
        #去爬取这个页面的信息
        get_products()
    except:
        crawl_page(page)

def get_products():
    #用工具去爬取这个页面
    html = browser.page_source
    #打印这个页面的信息
    doc = PyQuery(html)
    #去定位获取我们需要的信息
    items = doc("#mainsrp-itemlist .items .item").items()
    for item in items:
        product ={
            "href":item.find(".pic-link").attr("href"),
        }
        href = product["href"]
        url = "https:{}".format(href).replace("https:https:","https:")
        get_url(url)

#http://g-search3.alicdn.com/img/bao/uploaded/i4/i1/652684261/O1CN01SNuqML1hLaFlM5ijz_!!652684261.jpg_460x460Q90.jpg_.webp
def get_url(url):
    browser.get(url)
    time.sleep(2)
    html= browser.page_source
    doc = PyQuery(html)
    items = doc('div#attributes.attributes .attributes-list li').text()

    data = {
        'property':items
    }
    print(data['property'])
    save_to_file(data['property'])
#写一个保存文件的函数
def save_to_file(result):
    #a是追加信息的意思
    with open("result.text","a",encoding='utf-8') as f:
        #把python转化为json，然后用json的形式保存下来，ensure_ascii=False是识别有没有中文的意思
        f.write(json.dumps(result,ensure_ascii=False)+"\n")
        print("存储到text成功")


#最大页数
MAX_PAGE = 100
#写一个循环函数，用于爬取多页信息的内容
def main():
    for i in range(1,MAX_PAGE+1):
        crawl_page(i)
if __name__ == '__main__':
    main()