import requests
import re
from shujuku import sess,Tik
from concurrent.futures import ThreadPoolExecutor


list = []
with open('shuju6.text', 'r')as f:
    contents = f.readlines()
    for c in contents:
        content = c.strip()
        list.append(content)
headers = {
    'accept': 'application/json',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
}


def get_html(url):
    html = requests.get(url,headers= headers)
    contents = html.text
    #抖音个人简介
    signature = re.compile('signature":"(.*?)"',re.I | re.S)
    intro = signature.findall(contents)
    #抖音用户的名字
    nickname = re.compile('"nickname":"(.*?)"',re.I | re.S)
    name = nickname.findall(contents)
    #抖音上面的粉丝数量
    follower_count = re.compile('"follower_count":(.*?),',re.I | re.S)
    fans = follower_count.findall(contents)
    #抖音ID
    unique_id = re.compile('"unique_id":"(.*?)"',re.I | re.S)
    ID = unique_id.findall(contents)
    print('用户名称：{}\n用户ID：{}\n个人简介：{}\n粉丝数量：{}\n'.format(name,ID,intro,fans))
    try:
        tik = Tik(
            name = name,
            user_id = ID,
            intro = intro,
            fans = fans
        )
        sess.add(tik)
        sess.commit()
        print('commit')
    except Exception as e:
        print("rollback",e)
        sess.rollback()

if __name__ == '__main__':
    count = 0
    for uid in list:
        url = 'https://www.iesdouyin.com/web/api/v2/user/info/?' \
          'sec_uid={}'.format(uid)
        with ThreadPoolExecutor(max_workers=10)as e:
            futures = [e.submit(get_html,url)]
        count += 1
        print(count)
    sess.close()