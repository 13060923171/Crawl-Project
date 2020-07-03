import requests
import os
import re

#用正则表达式去获取这个图片的id
imageID = re.compile('"imageId":"(.*?)"')
#构建我们的请求头
headers= {
    "Accept-Encoding":"",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.62 Safari/537.36"
}
#去获取这个页面的图片并且保存下来
def get_page():
    url = "https://stock.tuchong.com/topic?topicId=49390"
    html = requests.get(url)
    result = imageID.findall(html.text)
    for r in result:
        #这个图片的URL的格式都一样，只是每张图片的ID不同而已，所以只要我们获取它的ID就可以获取它的图片
        imgurl = "https://icweiliimg9.pstatp.com/weili/l/{}.jpg".format(r)
        name = str(r)
        downloadImg(imgurl,name)
#写一个保存图片的函数
def downloadImg(url:str,name:str) ->None:
    if not os.path.exists("./图虫"):
        os.mkdir("./图虫")
    print("正在下载图片,ID:"+name)
    with open("./图虫/{}.jpg".format(name),"wb") as f:
        #通过保存这个图片的URL来保存这个图片
        f.write(requests.get(url,headers=headers).content)

if __name__ == '__main__':
    get_page()