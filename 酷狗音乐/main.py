import requests
from lxml import etree

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"
}

def get_html():
    url = "https://www.kugou.com/yy/rank/home/1-8888.html"
    html = requests.get(url,headers= headers)
    content = html.text
    soup = etree.HTML(content)
    list = []
    #定位歌单
    songs = soup.xpath('//li[@class = " "]')
    #定位歌曲名称
    sings = soup.xpath('//a[@class="pc_temp_songname"]/text()')
    #定位排名
    qiannum = soup.xpath('//li[@class= " "]/span[@class = "pc_temp_num"]/strong/text()')
    for i in qiannum:
        list.append(i)
    for song in songs[3:]:
        num = song.xpath('./span[@class = "pc_temp_num"]/text()')[0].strip()
        list.append(num)
    for j in range(len(list)):
        #创建列表输出酷狗音乐前500的歌曲
        s =sings[j].replace("-","")
        dowloand("{} {}".format(list[j],s))

def dowloand(dir):
    with open("歌单.txt","a+",encoding='utf-8')as f:
        f.write(dir)
        f.write("\n")
        print("写入成功")




if __name__ == '__main__':
    get_html()
