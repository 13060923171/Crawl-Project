import concurrent
import requests
from lxml import etree
import json
from concurrent.futures import ThreadPoolExecutor
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.62 Safari/537.36",
    "Cookie":"channelid=0; sid=1589982237213115; _ga=GA1.2.1825006235.1589983601; _gid=GA1.2.280479633.1589983601; _gat=1; Hm_lvt_7ed65b1cc4b810e9fd37959c9bb51b31=1589983601; Hm_lpvt_7ed65b1cc4b810e9fd37959c9bb51b31=1589983601"
}
#先解析我们的页面，看看状态码怎么样
def get_html(i):
    url ="https://www.kuaidaili.com/free/inha/{}/".format(i)
    html = requests.get(url,headers = headers)
    if html.status_code == 200:
        print("获取成功...")
        parse_html(html)
    else:
        print("error")

#然后用xpath语法来定位获取我们需要的东西
def parse_html(html):
    soup = etree.HTML(html.text)
    trs = soup.xpath('//div[@id = "list"]/table/tbody/tr')
    for tr in trs:
        ip = tr.xpath('./td[@data-title = "IP"]/text()')[0]
        port = tr.xpath('./td[@data-title = "PORT"]/text()')[0]
        if ip and port:
            daili = ip + ":" + port
            #构建一个代理池来检测IP地址是否能用
            proxies = {
                "http":"http://" + daili,
                "https":"http://"+daili
            }
            verify_ip(proxies)

#构建一个函数来解析我们的IP地址是否能用，并且保存下来
def verify_ip(proxies):
    try:
        html = requests.get("https://www.baidu.com/",proxies=proxies,timeout =3)
        print("可以使用的代理:{}".format(proxies))
        write_txt(proxies)
    except :
        print("代理有问题:{}".format(proxies))

#构建一个把数据用json保存下来的函数
def write_txt(row):
    with open('ip_pool.json','a+',encoding='utf8')as f:
        json.dump(row,f)

#构建一个可以读取json的函数，用于读取json文件里面的ip地址是否失效了
def read_txt():
    with open('ip_pool.json','r',encoding='utf8')as f:
        content = json.load(f)
        print(content)
        html = requests.get('https://www.baidu.com/',proxies=content,timeout=3)
        print(html.text)


if __name__ == '__main__':
    #采用多线程的方法，开10个多线程，大大提高效率，这个是固定写法得牢记
    with concurrent.futures.ThreadPoolExecutor(max_workers = 10 )as e:
        #创建一个列表，在里面开始循环200次这个函数
        futures = [e.submit(get_html,i) for i in range(200,400,1)]
        #用叠带方法把内容一一打印出来，防止CPU瞬间占满，这个用于多线程循环的固定写法
        for future in concurrent.futures.as_completed(futures):
            print(future.result())
    #调用读取这个函数
    # read_txt()