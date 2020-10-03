from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pyquery import PyQuery
import time
import json
import re

#定义一个变量，最好用大写这个是约定俗成
KEYWORD = '月饼'
#定位Chromedriver这个工具的位置
options = webdriver.ChromeOptions()
options.add_experimental_option("prefs",{"profile.mamaged_default_content_settings.images":2})
options.add_experimental_option('excludeSwitches',['enable-automation'])
browser = webdriver.Chrome(executable_path="C:\\Users\\96075\\Desktop\\全部资料\\Python\\爬虫\\chromedriver.exe",options=options)
#设置等待时间
wait = WebDriverWait(browser,10)
url ='https://www.taobao.com/'

list_property = []
#先写一个去调动输入框定位一个商品类型的函数，并且获取总的页数
def crawl_page():
    try:
        browser.get(url)#获取网页
        #用xpath语法定位到输入框
        input = wait.until(EC.presence_of_element_located((
            By.XPATH,'//*[@id="q"]'
        )))
        #用xpath语法定位到搜索框
        button = wait.until(EC.element_to_be_clickable((
            By.XPATH,'//*[@id="J_TSearchForm"]/div[1]/button'
        )))
        input.send_keys(KEYWORD)#输入关键词
        button.click()#模拟鼠标点击
        #等到python爬虫页面的总页数加载出来
        total = wait.until(EC.presence_of_element_located((
            By.XPATH,'//*[@id="mainsrp-pager"]/div/div/div/div[1]'
        ))).text
        # 发现总页数有逗号
        total = re.sub(r',|，','',total)
        #数据清洗，将共100页后面的逗号去掉,淘宝里的是大写的逗号
        print(total)
        totalnum = int(re.compile('(\d+)').search(total).group(1))
        # 只取出100这个数字
        print("第1页:")
        # 获取数据
        get_products()
        #返回总的页数
        return totalnum
    except:
        crawl_page()
#然后根据获取总的页数来获取每一页商品的内容和信息
def next_page():
    # 获取总页数的值，并且调用search获取第一页数据
    totalnum = crawl_page()
    # 初始为1，因为我第一页已经获取过数据了
    num = 1
    # 首先进来的是第1页，共100页，所以只需要翻页99次
    while num != totalnum - 1:
        print("第%s页:" %str(num+1) )
        # 用修改s属性的方式翻页
        browser.get('https://s.taobao.com/search?q={}&s={}'.format(KEYWORD,44 * num))
        # 等待10秒
        browser.implicitly_wait(10)
        # 获取数据
        get_products()
        #延迟3秒
        time.sleep(3)
        # 自增
        num +=1
#再根据获取到的商品信息来定位来商品的链接从而进入商品的详细页面
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

#获取到详细页面之后去获取每个商品信息的属性，并且把这些属性抓取下来
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
    with open("商品属性.text","a",encoding='utf-8') as f:
        #把python转化为json，然后用json的形式保存下来，ensure_ascii=False是识别有没有中文的意思
        f.write(json.dumps(result,ensure_ascii=False)+"\n")
        print("存储到text成功")

if __name__ == '__main__':
    next_page()