#调用第三方库，去请求这个页面，从而获取对应的信息
import requests
#BeautifulSoup是用于定位的，一个解析库
from bs4 import BeautifulSoup
#转换，把中文转换成计算机看得懂的字符串
from urllib import parse
#调用时间库
import time
#写入异步爬虫库
import asyncio
#写入异步爬虫库
import aiohttp
#添加一个请求头伪装成一个网页，不让服务器检测出来是一个爬虫
headers = {
    #伪装成浏览器
    "user-agent": "user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
    #写入cookie身份验证
    'cookie': 'lid=%E5%8F%B6%E9%97%AE%E8%B0%81%E6%98%AF%E8%BE%B0%E5%8D%97; '
              'enc=UvoaKN2E%2F5qKScgssIA7s34lg2c%2B7mFKY6bD58vrwGvLTZKDyYj7UQ0p3hGnXJK11f8JrZT5ky54YNi0i73Few%3D%3D; '
              'hng=CN%7Czh-CN%7CCNY%7C156; cna=UU81Fxb46woCAWUv7c0BLoMd; sgcookie=ERElHyZEXq%2FBxbIAKkMLf; '
              't=496d0969426724e74173f0da2d1cee9a; tracknick=%5Cu53F6%5Cu95EE%5Cu8C01%5Cu662F%5Cu8FB0%5Cu5357;'
              ' _tb_token_=e1be513fe6183; cookie2=122a786f6e96fdafc60982a260d7da13; _med=dw:1280&dh:720&pw:1920&ph:1080&ist:0; '
              'res=scroll%3A1263*5595-client%3A1263*616-offset%3A1263*5595-screen%3A1280*720; cq=ccp%3D1; pnm_cku822=098%23E1hv5vvUvbpvUpCkvvvvvjiPnLF9gjEHR25vAjnEPmP'
              'W1jiURLSOtj1hPLFyljlWRuwCvvpvvUmmmphvLvpbyvvj4Omxfwowderv%2B8c6gEAfalSXS47BhC3qVUcnDOmOejIUDajxALwpEcqvaNoUrCH%2Bm7zpaNpz%2BFwcoX7aHLQg4vlrlj7Q%2Bu0tvpvIvvvvvhCvvvvvvUUvphvUIpvv99Cvpv'
              '32vvmmvhCvmhWvvUUvphvUpTyCvv9vvUmtH%2B2UhIyCvvOUvvVvJh%2BCvpvVvvpvvhCv2QhvCPMMvvvtvpvhvvvvvv%3D%3D; l=eBS73WTPOgsqiBdBBOfZourza77tLIRvouPzaNbMiOCPOU56HJM5WZkxaOLBCnGVh6z'
              'kR3ow4YKMBeYBqImRv7aStBALu4Hmn; isg=BAYG6NkRpQFaDnF45ewiaNZZV_yIZ0ohS2d9TfAvpSlT86YNWPYEMIOBzy8_7UI5',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    'referer': 'https://www.tmall.com/',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-site',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',

}

keyword = input("请输入你要搜索的信息：")
async def get_parse(url):
    #写成异步函数的固定形式去调用请求头
    async with aiohttp.ClientSession(headers = headers)as session:
        #异步函数调用URL
        async with session.get(url)as rep:
            #去请求网页的状态码
            if rep.status:
                print(rep.status)
                content = await rep.text()
    # 使用我们的解析库
    soup = BeautifulSoup(content, 'lxml')
    # 先定位到总的商品数量，然后进行叠带
    products = soup.select('div.product')
    # 写一个防错机制，防止程序出错，不能执行下一步
    try:
        for product in products:
            # 定位标题
            title = product.select_one("p.productTitle").text.strip()
            # 定位价钱
            price = product.select_one("p.productPrice em").text.strip()
            # 定位商铺名称
            shop = product.select_one("div.productShop").text.strip()
            # 定位月成交数量
            status = product.select_one("p.productStatus em").text.strip()
            # 定位评价有多少条
            target = product.select_one("p.productStatus span a").text.strip()
            print('商品名字:{}'.format(title))
            print('商品的价格：{} 月成交：{} 评价：{}'.format(price, status, target))
            print('商铺名称:{}\n'.format(shop))
            print("~" * 50)
    except:
        pass
    else:
        print("网页正常运行")
        print(rep.status)



if __name__ == '__main__':
    # 请求天猫的URL
    url = "https://list.tmall.com/search_product.htm?q={}".format(parse.quote(keyword))
    #写一个测试时间的函数
    s =time.time()
    #开启我们的异步函数
    loop = asyncio.get_event_loop()
    #等到异步执行完毕
    loop.run_until_complete(get_parse(url))
    #输出运行的总时间
    print(time.time() - s)
    #关闭我们的异步
    loop.close()


