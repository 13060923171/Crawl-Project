import requests
import re
from urllib import parse
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
    "referer": "https://tb.alicdn.com/snapshot/index.html",
    'cookie': 't=884491259d4aed9aac3cd83e5798c433; cna=UU81Fxb46woCAWUv7c0BLoMd; sgcookie=ERElHyZEXq%2FBxbIAKkMLf; tracknick=%5Cu53F6%5Cu95EE%5Cu8C01%5Cu662F%5Cu8FB0%5Cu5357; _cc_=V32FPkk%2Fhw%3D%3D; enc=UvoaKN2E%2F5qKScgssIA7s34lg2c%2B7mFKY6bD58vrwGvLTZKDyYj7UQ0p3hGnXJK11f8JrZT5ky54YNi0i73Few%3D%3D; tfstk=cIOdBdvB3cmha_TF3QHGFR3VyY-dafFd2ys4w4-E6MTnQmN8NsxviIpfnv_Yv13O.; thw=cn; hng=CN%7Czh-CN%7CCNY%7C156; cookie2=1165897f57a1ed424d42db9d3a99ff7d; v=0; _tb_token_=77a6e3fa3eb98; alitrackid=tb.alicdn.com; lastalitrackid=tb.alicdn.com; JSESSIONID=42FB5C5D5D65C270436BAF43224830CB; isg=BPb2H7f2tUx9pkBnqiw8IaAaRyz4FzpR25dtfWDcO1mro5U9yaZ-YfUau3_PPzJp; l=eBTUSTCcQZnRM5Q_BO5alurza77TaQdf1nVzaNbMiInca6TFta8TVNQqOBKvSdtjgt5j2eKrb3kJjRhM8W4LRjkDBeYBRs5mpfpp8e1..',
}

keyword = input("请输入你要搜索的信息：")
def get_parse(url):
    html = requests.get(url,headers= headers)
    if html.status_code ==200:
        print('页面正常')
        get_html(html)
    else:
        print(html.status_code)

def get_html(html):
    #用正则表达式去获取商品的名称，价格，商家名称和商家位置
    content = html.text
    #定位商品名称
    names = re.compile('"raw_title":"(.*?)"', re.I | re.S)
    name = names.findall(content)
    #定位价格
    prices = re.compile('"view_price":"(.*?)"',re.I|re.S)
    price = prices.findall(content)
    #定位商家名称
    nicks = re.compile('"nick":"(.*?)"',re.I|re.S)
    nick = nicks.findall(content)
    #定位商家位置
    item_locs = re.compile('"item_loc":"(.*?)"', re.I | re.S)
    item_loc= item_locs.findall(content)
    #先算出爬出来正则的长度，从而确定循环，把商品的名称，价格，位置全部有序的全部打印出来
    for j in range(len(name)):
        print('商品名称：{}\n价格：{}\n商家名称：{}\n商家位置：{}\n'.format(name[j], price[j], nick[j], item_loc[j]))

if __name__ == '__main__':
    for i in range(0,45,44):
        url = 'https://s.taobao.com/search?q={}&imgfile=&commend=all&ssid=s5-e&' \
              'search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&' \
              'ie=utf8&initiative_id=tbindexz_20170306&bcoffset=1&ntoffset=1&p4ppushleft=2%2C48&s={}'.format(parse.quote(keyword),i)
        get_parse(url)



