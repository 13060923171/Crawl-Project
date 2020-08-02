import requests
import re
from bs4 import BeautifulSoup
import time
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Cookie": "Hm_lvt_2ce94714199fe618dcebb5872c6def14=1594741637; Hm_lpvt_2ce94714199fe618dcebb5872c6def14=1594741768",
    "Host": "www.zuihaodaxue.cn",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
}
session = requests.session()
session.headers = headers

def get_html9(url):
    html = session.get(url)
    #它的解码等于他当前的页面的解码，这样破解里面字体的反爬
    html.encoding = html.apparent_encoding
    if html.status_code == 200:
        content = html.text
        #用正则去定位排名
        rankings = re.compile('"><td>(.*?)</td>',re.I|re.S)
        ranking = rankings.findall(content)
        soup = BeautifulSoup(content,'lxml')
        list = []
        for i in range(len(ranking)):
            #定位大学名称
            daxues = soup.select("td.align-left a")[i].text
            list.append(daxues)
            print(list)
        #定位大学排名
        states = re.compile('title="查看(.*?)大学排名">', re.I | re.S)
        state = states.findall(content)
        state_ranks = re.compile('</a></td><td class="hidden-xs">(.*?)</td><td>',re.I|re.S)
        state_rank = state_ranks.findall(content)
        grades = re.compile('\d+</td><td>(.*?)</td><td', re.I | re.S)
        grade = grades.findall(content)
        indexs = re.compile('class="hidden-xs need-hidden alumni">(.*?)</td><td', re.I | re.S)
        index = indexs.findall(content)
        for j in range(len(ranking)):
            with open('2019.text', 'a+',encoding='utf-8')as f:
                f.write('{} {} {} {} {} {}'.format(ranking[j],list[j],state[j],state_rank[j],grade[j],index[j]))
                f.write('\n')
                print('写入成功')
            print('{} {} {} {} {} {}'.format(ranking[j],list[j],state[j],state_rank[j],grade[j],index[j]))
    else:
        print(html.status_code)

def get_html8(url):
    html = session.get(url)
    html.encoding = html.apparent_encoding
    if html.status_code == 200:
        content = html.text
        rankings = re.compile('"><td>(.*?)</td>',re.I|re.S)
        ranking = rankings.findall(content)
        soup = BeautifulSoup(content,'lxml')
        list = []
        for i in range(len(ranking)):
            daxues = soup.select("td.align-left a")[i].text
            list.append(daxues)
            print(list)
        states = re.compile('title="查看(.*?)大学排名">', re.I | re.S)
        state = states.findall(content)
        state_ranks = re.compile('</a></td><td class="hidden-xs">(.*?)</td><td>',re.I|re.S)
        state_rank = state_ranks.findall(content)
        grades = re.compile('\d+</td><td>(.*?)</td><td', re.I | re.S)
        grade = grades.findall(content)
        indexs = re.compile('class="hidden-xs need-hidden alumni">(.*?)</td><td', re.I | re.S)
        index = indexs.findall(content)
        for j in range(len(ranking)):
            with open('2018.text', 'a+',encoding='utf-8')as f:
                f.write('{} {} {} {} {} {}'.format(ranking[j],list[j],state[j],state_rank[j],grade[j],index[j]))
                f.write('\n')
                print('写入成功')
            print('{} {} {} {} {} {}'.format(ranking[j],list[j],state[j],state_rank[j],grade[j],index[j]))
    else:
        print(html.status_code)

def get_html7(url):
    html = session.get(url)
    html.encoding = html.apparent_encoding
    if html.status_code == 200:
        content = html.text
        rankings = re.compile('"><td>(.*?)</td>',re.I|re.S)
        ranking = rankings.findall(content)
        soup = BeautifulSoup(content,'lxml')
        list = []
        for i in range(len(ranking)):
            daxues = soup.select("td.align-left a")[i].text
            list.append(daxues)
            print(list)
        states = re.compile('title="查看(.*?)大学排名">', re.I | re.S)
        state = states.findall(content)
        state_ranks = re.compile('</a></td><td class="hidden-xs">(.*?)</td><td>',re.I|re.S)
        state_rank = state_ranks.findall(content)
        grades = re.compile('\d+</td><td>(.*?)</td><td', re.I | re.S)
        grade = grades.findall(content)
        indexs = re.compile('class="hidden-xs need-hidden alumni">(.*?)</td><td', re.I | re.S)
        index = indexs.findall(content)
        for j in range(len(ranking)):
            with open('2017.text', 'a+',encoding='utf-8')as f:
                f.write('{} {} {} {} {} {}'.format(ranking[j],list[j],state[j],state_rank[j],grade[j],index[j]))
                f.write('\n')
                print('写入成功')
            print('{} {} {} {} {} {}'.format(ranking[j],list[j],state[j],state_rank[j],grade[j],index[j]))
    else:
        print(html.status_code)




if __name__ == '__main__':
    start = time.time()
    url = "http://www.zuihaodaxue.cn/ARWU2019.html"
    get_html9(url)
    time.sleep(90)
    url2 = "http://www.zuihaodaxue.cn/ARWU2018.html"
    get_html8(url2)
    time.sleep(90)
    url3 = "http://www.zuihaodaxue.cn/ARWU2017.html"
    get_html7(url3)
    print(time.time()-start)