import requests
from lxml import etree
import concurrent.futures
import time
headers = {
    "cookie": "_T_WM=80006864411; SUB=_2A25yLV_pDeRhGeNN6lsS-CrJyz-IHXVR7mGhrDV6PUJbkdANLRLikW1NSdnQVAQz39AMWYkEgssRUk6zryot_An8; SUHB=0YhRxyhmco90XH; SCF=AsMbwcRKK_jAOmIDD96RXELSkFJnEvDB2VX15SWPKvBVmHSXglPApzr4afyij6iE0CEfixrvQ1ETFDSEMPvKMgA.; MLOGIN=1; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D1076035492443184; WEIBOCN_FROM=1110106030",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
}

list = []
for i in range(500,700,1):
    url = "https://weibo.cn/comment/Jfb66BseB?uid=5492443184&rl=0&page={}".format(i)
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
    titles = soup.xpath('//div/span[@class = "ctt"]/text()')
    for title in titles:
        wenzhang = title.strip()
        print(wenzhang)
        write_text(wenzhang)

def write_text(wenzhang):
    with open("王一博最新评论.txt","a+",encoding='utf-8')as f:
        f.write(wenzhang)
        f.write("\n")
        print("写入成功")

if __name__ == '__main__':
    # s = time.time()
    # with concurrent.futures.ThreadPoolExecutor(max_workers = 5)as e:
    #     futures = [e.submit(get_statue,i) for i in list]
    #     for future in concurrent.futures.as_completed(futures):
    #         print(future.result())
    # print(time.time()-s)
    for i in list:
        get_statue(i)