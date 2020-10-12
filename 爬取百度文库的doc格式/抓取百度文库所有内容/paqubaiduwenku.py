import requests
import re

#首先先去获取这个函数
def get_html(url):
    try:
        #这里用到防错机制先获取这个页面用get方法
        r = requests.get(url,headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.62 Safari/537.36"})
        #这句话的意思就是这个HTTP回应内容的编码方式 =这个内容的备用编码方式，
        # 这样写的意义就是不用指定某种编码，而是直接调用这个内容的编码
        r.encoding = r.apparent_encoding
        #放回这个内容以text的形式
        return r.text
    except:
        print("URL request error")

#开始解析我们的doc文件
def parse_doc(html):
    #先设置result为空，方便存放
    result = ''
    #用我们的正则去获取我们想要的URL
    url_list = re.findall("(https.*?0.json.*?)\\\\x22}", html)
    #并且把获取到的URL替换成正确的URL
    url_list = [addr.replace("\\\\\\/","/") for addr in url_list]
    #最后打印出来
    print(url_list)
    #开始调用我们的URL，因为最后5条是用不了的，所以对它们进行切片
    for url in url_list[:-5]:
        content = get_html(url)
        y = 0
        #把这个列表全部打印出来，因为这里是用到了反爬虫机制，所以我们要开始解析页面
        txtlists = re.findall('"c":"(.*?)".*?"y":(.*?),',content)
        for item in txtlists:
            if not y==item[1]:
                y = item[1]
                n = '\n'
            else:
                n = ''
            result += n
            #最后的结果，把我们破解好的内容一条条的打印上去，解码方式就是utf-8，因为还有因为解码还没解，所以我采用了最大的解码方法
            result += item[0].encode("utf-8").decode("unicode_escape","ignore")
    return result

def main():
    #输入我们想要爬取这个文章的连接
    url = input("请输入你要获取百度文库的URL连接:")
    html = get_html(url)
    #爬取这个页面的一些信息
    wenku_title = re.findall("\'title\'.*?\'(.*?)\'",html)[0]
    wenku_type = re.findall("\'docType\'.*?\'(.*?)\'",html)[0]
    wenku_id = re.findall("'docId'.*?'(.*?)'",html)[0]
    print("文章类型",wenku_type)
    print("文档ID",wenku_id)
    result =parse_doc(html)
    filename= wenku_title+'.doc'
    with open(filename,"w",encoding="utf-8") as f:
        f.write(result)
    print("文件保存为{}.doc".format(wenku_title))

if __name__ == '__main__':
    main()