#哈希解密，python专门用于解密的包
import hashlib
import math
import time
import random
import requests
#写我们的headers请求头来伪装
headers = {
    'Referer': 'http://fanyi.youdao.com/',
    'Host': 'fanyi.youdao.com',
    'Cookie': 'OUTFOX_SEARCH_USER_ID=-1301778021@10.108.160.18; JSESSIONID=aaaZrrAa2NnfU_CTfOXmx; OUTFOX_SEARCH_USER_ID_NCOO=867998809.2797275; ___rl__test__cookies=1594266717266',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
}

Keyword = input("请输入你要翻译的内容：")
#为了和有道翻译的时间一样，由于python的时间戳和js不一样，所以要乘以1000，并且进行四舍五入，去掉小数点
r = math.floor(time.time()*1000)
#r + parseInt(10 * Math.random(), 10);用python的语法来重写这句js，用于解密来获取ts值
i = r+int(random.random()*10)
salt= i
ts = r
#这里用的是最经典的Md5解密可以用我们的python的哈希来，写法是一样的
#sign: n.md5("fanyideskweb" + e + i + "mmbP%A-r6U3Nw(n]BjuEU")这里e是我们的keyword值，i是我们解密出来的i值，后面再用
#encode('utf8')的解码utf-8来解码，hexdigest() 的意义是返回摘要，作为十六进制数据字符串值
#如果用的是digest() 则返回摘要，作为二进制数据字符串值
sign = hashlib.md5(("fanyideskweb" + Keyword + str(i) + "mmbP%A-r6U3Nw(n]BjuEU").encode('utf8')).hexdigest()
bv = hashlib.md5("5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36".encode('utf8')).hexdigest()
data = {
    'i': Keyword,
    'from': 'AUTO',
    'to': 'AUTO',
    'smartresult': 'dict',
    'client': 'fanyideskweb',
    'salt': salt,
    'sign': sign,
    'ts': ts,
    'bv': bv,
    'doctype': 'json',
    'version': '2.1',
    'keyfrom': 'fanyi.web',
    'action': 'FY_BY_REALTlME'
}


url = "http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"
html = requests.session()
content = requests.post(url,data=data,headers= headers).json()
fangyi = content['translateResult'][0][0]['tgt']
print("翻译结果：{}".format(fangyi))

