from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from urllib.parse import quote
from pyquery import PyQuery
import time
import json
import re
#定义一个变量，最好用大写这个是约定俗成
KEYWORD = '月饼'
#定位Chromedriver这个工具的位置
browser = webdriver.Chrome(executable_path="C:\\Users\\96075\\Desktop\\全部资料\\Python\\爬虫\\chromedriver.exe")
#设置等待时间
wait = WebDriverWait(browser,10)
url ='https://www.taobao.com/'

def crawl_page():
    try:
        browser.get(url)#获取网页
        input = wait.until(EC.presence_of_element_located((
            By.XPATH,'//*[@id="q"]'
        )))#等到输入框加载出来
        button = wait.until(EC.element_to_be_clickable((
            By.XPATH,'//*[@id="J_TSearchForm"]/div[1]/button'
        )))#等到搜索框加载出来
        input.send_keys(KEYWORD)#输入关键词
        button.click()#模拟鼠标点击
        total = wait.until(EC.presence_of_element_located((
            By.XPATH,'//*[@id="mainsrp-pager"]/div/div/div/div[1]'
        ))).text#等到python爬虫页面的总页数加载出来
        total = re.sub(r',|，','',total)#发现总页数有逗号
        #数据清洗，将共100页后面的逗号去掉,淘宝里的是大写的逗号
        print(total)
        totalnum = int(re.compile('(\d+)').search(total).group(1))
        # 只取出100这个数字
        print("第1页:")
        get_products()#获取数据(下面才写到)
        return totalnum
    except:
        crawl_page()

def get_products():
    #用工具去爬取这个页面
    html = browser.page_source
    #打印这个页面的信息
    doc = PyQuery(html)
    #去定位获取我们需要的信息
    items = doc("#mainsrp-itemlist .items .item").items()
    for item in items:
        product ={
            "image": item.find(".img").attr("data-src"),
            "price": item.find(".price").text(),
            "deal": item.find(".deal-cnt").text(),
            "title": item.find(".title").text(),
            "shop": item.find(".shop").text(),
            "location": item.find(".location").text(),
        }
        print(product)
        #保存我们获取的信息
        save_to_file(product)
#写一个保存文件的函数
def save_to_file(result):
    #a是追加信息的意思
    with open("result.text","a",encoding='utf-8') as f:
        #把python转化为json，然后用json的形式保存下来，ensure_ascii=False是识别有没有中文的意思
        f.write(json.dumps(result,ensure_ascii=False)+"\n")
        print("存储到text成功")

def next_page():
    totalnum = crawl_page()#获取总页数的值，并且调用search获取第一页数据
    num = 1#初始为1，因为我第一页已经获取过数据了
    while num != totalnum - 1:#首先进来的是第1页，共100页，所以只需要翻页99次
        print("第%s页:" %str(num+1) )
        browser.get('https://s.taobao.com/search?q={}&s={}'.format(KEYWORD,44 * num))
        #用修改s属性的方式翻页
        browser.implicitly_wait(10)
        #等待10秒
        get_products()#获取数据
        time.sleep(3)
        num +=1#自增

#写一个循环函数，用于爬取多页信息的内容
def main():
    next_page()
if __name__ == '__main__':
    main()