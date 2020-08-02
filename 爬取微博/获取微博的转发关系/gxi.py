import requests
from lxml import etree
import concurrent.futures

headers = {
    "cookie": "_T_WM=a96578de569de43753db540a141c819b; SUB=_2A25yEo2TDeRhGeNN6lsS-CrJyz-IHXVR_BPbrDV6PUJbkdANLWPgkW1NSdnQVCGHLFRbfwvsOXKxEDeKwzQ-OeZj; SUHB=04WuxbFN8-tkwi",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
}
session = requests.session()
session.headers = headers

def get_pinglun(href,yeshu):
    try:
        for i in range(1,int(yeshu)+1):
            url = "{}&page={}".format(href,i)
            html = session.get(url)
            content = html.text
            soup = etree.HTML(content.encode('utf-8'))
            names = soup.xpath('//div[@class = "c"]')
            for name in names[3:-1]:
                title = name.xpath('./a/text()')[0]
                print(title)
    except:
        pass
            # one_zhuanfa(title)


def one_zhuanfa(title):
    with open("diyichizhuanfa.txt","a+",encoding="utf-8")as f:
        f.write(title)

if __name__ == '__main__':
    href = 'https://weibo.cn/repost/Jd6djg2hY?uid=2656274875&rl=1'
    yeshu = 281
    with concurrent.futures.ThreadPoolExecutor(max_workers=10)as e:
        futures = [e.submit(get_pinglun, href, yeshu)]
        for futuer in concurrent.futures.as_completed(futures):
            print(futuer.result())
