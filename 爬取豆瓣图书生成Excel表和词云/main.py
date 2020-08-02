import time
from urllib.parse import quote
from bs4 import BeautifulSoup
import xlwt
import requests
import jieba
from wordcloud import WordCloud, STOPWORDS
from imageio import imread

headers = {
    "Referer": "https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4?start=20&type=T",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.62 Safari/537.36",
    "Cookie": "ll='118281'; bid=O7ufDRQf-EM; ap_v=0,6.0; __utma=30149280.824434074.1589705958.1589705958.1589705958.1; __utmc=30149280; __utmz=30149280.1589705958.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utma=81379588.1042792723.1589705961.1589705961.1589705961.1; __utmc=81379588; __utmz=81379588.1589705961.1.1.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; gr_user_id=fe84be7b-7be1-48cd-96b7-db1a1bcb1df7; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=8a7d4654-db1a-4780-a80d-426a80bb2eba; gr_cs1_8a7d4654-db1a-4780-a80d-426a80bb2eba=user_id%3A0; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1589705961%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.3ac3=*; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03_8a7d4654-db1a-4780-a80d-426a80bb2eba=true; _pk_id.100001.3ac3=e2ddd2d20afe5226.1589705961.1.1589705990.1589705961.; __utmb=30149280.5.10.1589705958; __utmb=81379588.4.10.1589705961"
}

def parse_html(i):
    url = "https://book.douban.com/tag/{}?start={}&type=T".format(quote(KEYWORD), i)
    html = requests.get(url,headers= headers)
    text = html.text
    try:
        #这些就是以往的写法了没什么好说的，这里用到的是BeautifulSoup解析器
        soup = BeautifulSoup(text,"lxml")
        books = soup.select("li.subject-item")
        list = []
        list1 = []
        list2 = []
        list3 = []
        list4 = []
        for book in books:
            title = book.select_one(".info h2 a").text.strip().replace(" :","").replace(" ","").replace("\n","")
            info = book.select_one(".info div.pub").text.strip().replace("\n","")
            star = book.select_one("span.rating_nums").text
            pingfeng = book.select_one("span.pl").text.strip().replace("\n","")
            text = book.select_one(".info p").text
            print(title,info,star,pingfeng)
            print(text)
            print("="*50)
            write_txt(title)
            list.append(title)
            list1.append(info)
            list2.append(star)
            list3.append(pingfeng)
            list4.append(text)
            write_excel(list,list1,list2,list3,list4)
    except:
        pass

#设置表格样式
def set_style(name,height,bold=False):
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = name
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font
    return style

#书名保存到txt的函数
def write_txt(title):
    with open("test.text","a+",encoding="utf8")as f:
        f.write(title)


#写Excel
def write_excel(list,list1,list2,list3,list4):
    f = xlwt.Workbook()
    sheet1 = f.add_sheet('小说',cell_overwrite_ok=True)
    row0 = ["书名","作家和相关内容","评分","有多少人评价","简介"]
    #写第一行
    for i in range(0,len(row0)):
        sheet1.write(0,i,row0[i],set_style('Times New Roman',220,True))
    #写第一列
    for i in range(0,len(list)):
        sheet1.write(i+1,0,list[i],set_style('Times New Roman',220,True))
    #写第二列
    for i in range(0,len(list1)):
        sheet1.write(i+1,1,list1[i],set_style('Times New Roman',220,True))
    #写第三列
    for i in range(0,len(list2)):
        sheet1.write(i+1,2,list2[i],set_style('Times New Roman',220,True))
    #写第四列
    for i in range(0,len(list3)):
        sheet1.write(i+1,3,list3[i],set_style('Times New Roman',220,True))
    #写第五列
    for i in range(0,len(list4)):
        sheet1.write(i+1,4,list4[i],set_style('Times New Roman',220,True))
    #保存到Excel表
    f.save('test.xls')

#生成词云
def ciyun():
    #先读取文件获取相关信息
    with open("test.text","r",encoding="utf8") as f:
        contents = f.read()
    print("contents变量的类型：", type(contents))

    # 使用jieba分词，获取词的列表
    contents_cut = jieba.cut(contents)
    print("contents_cut变量的类型：", type(contents_cut))
    contents_list = " ".join(contents_cut)
    print("contents_list变量的类型：", type(contents_list))

    # 制作词云图，collocations避免词云图中词的重复，mask定义词云图的形状，图片要有背景色
    wc = WordCloud(stopwords=STOPWORDS.add("一个"), collocations=False,
                   background_color="white",
                   font_path=r"C:\Windows\Fonts\simhei.ttf",
                   width=400, height=300, random_state=42,
                   mask=imread('axis.png', pilmode="RGB"))
    wc.generate(contents_list)
    #要读取的形状的图片
    wc.to_file("ciyun.png")



if __name__ == '__main__':
    KEYWORD = input("请输入你要搜索的类型：")
    #设置爬取的页数
    for i in range(0,100,20):
        parse_html(i)
        #爬取全部内容，等待结束
    ciyun()
    time.sleep(3)

