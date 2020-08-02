import requests
from lxml import etree
import concurrent.futures
from urllib import parse
import time
headers = {
    "cookie": "_T_WM=a96578de569de43753db540a141c819b; SUB=_2A25yEo2TDeRhGeNN6lsS-CrJyz-IHXVR_BPbrDV6PUJbkdANLWPgkW1NSdnQVCGHLFRbfwvsOXKxEDeKwzQ-OeZj; SUHB=04WuxbFN8-tkwi",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
}
keyword = input("请输入你要搜索的关键词:")
list = []
#搜索关键词一次性只有100页的内容
for i in range(1,101,1):
    #构建页数的URL，写入列表里面
    url = "https://weibo.cn/search/mblog?hideSearchFrame=&keyword={}&advancedfilter=1&hasori=1&starttime=20200301&endtime=20200701&sort=hot&page={}".format(parse.quote(keyword),i)
    list.append(url)

def get_statue(url):
    html = requests.get(url,headers= headers)
    if html.status_code ==200:
        print("页面正常")
        get_html(html)
    else:
        print(html.status_code)

def get_html(html):
    content = html.text
    soup = etree.HTML(content.encode('utf-8'))
    #去定位到每一页里面的内容
    titles = soup.xpath('//div[@class = "c"]/div/span[@class = "ctt"]/text()')
    for title in titles:
        wenzhang = title.strip()
        print(wenzhang)
        write_text(wenzhang)

def write_text(neirong):
    with open("2020-7.txt","a+",encoding='utf-8')as f:
        f.write(neirong)
        f.write("\n")
        print("写入成功")

if __name__ == '__main__':
    s = time.time()
    #开启多线程去跑，爬取一百页的内容提高我们的工作效率
    with concurrent.futures.ThreadPoolExecutor(max_workers = 5)as e:
        futures = [e.submit(get_statue,i) for i in list]
        for future in concurrent.futures.as_completed(futures):
            print(future.result())
    print(time.time()-s)
