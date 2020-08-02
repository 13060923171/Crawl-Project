import aiohttp
import asyncio
from bs4 import BeautifulSoup
from urllib import parse
import time
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.62 Safari/537.36"
}
#写一个异步函数去爬取微博的页面信息
async def get_html(url):
    print("正在爬取：",url)
    #异步调用header和URL的固定格式，必须得记
    async with aiohttp.ClientSession(headers= headers) as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                parse_html(await resp.text())
            else:
                print("ERROR",resp.status)
            return
#去获取微博每个热榜的标题和URL
def parse_html(html):
    soup = BeautifulSoup(html,"lxml")
    news = soup.select("table tbody tr")
    for new in news:
        title = new.select_one("td a").text
        url = new.select_one("td a")['href']
        url = parse.urljoin("https://s.weibo.com",url)
        print(title,url)

if __name__ == '__main__':
    start = time.time()
    #爬取多个热榜的URL
    urls=[
        "https://s.weibo.com/top/summary?cate=realtimehot",
        "https://s.weibo.com/top/summary?cate=socialevent"
    ]
    #创建一个列表来存放数据
    tasks = []
    #用一个循环叠带把爬取放回成功的URL添加到tasks里面
    for url in urls:
        tasks.append(get_html(url))
    #开启我们的异步函数
    loop = asyncio.get_event_loop()
    #等待我们的异步函数结束
    loop.run_until_complete(asyncio.wait(tasks))
    print(time.time()-start)
    #关闭我们的异步
    loop.close()
