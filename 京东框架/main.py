import requests
from bs4 import BeautifulSoup
import re,json,csv
import threadpool
from urllib import parse
headers = {
    'cookie': 'unpl=V2_ZzNtbRAEQxYiDBNTKR1cAmIGEg1KVEYVcgxFBH4ZCQIyABpbclRCFnQUR1NnGlQUZwEZWUtcQRdFCEdkeB5fA2AFEFlBZxVLK14bADlNDEY1WnwHBAJfF3ILQFJ8HlQMZAEUbXJUQyV1CXZdeR1aB2QHE1tyZ0QlRThGXXMbXQZXAiJcchUXSXEKQVVzGBEMZQcUX0FTQhNFCXZX; __jdv=76161171|google-search|t_262767352_googlesearch|cpc|kwd-362776698237_0_cb12f5d6c516441a9241652a41d6d297|1593410310158; __jdu=835732507; areaId=19; ipLoc-djd=19-1601-50256-0; PCSYCityID=CN_440000_440100_440114; shshshfpa=b3947298-5c63-ba93-8e7d-b89e3e422382-1593410312; shshshfpb=eVvsT1HAgXe1EsnsQQ6HTpQ%3D%3D; __jda=122270672.835732507.1593410309.1593410309.1593410310.1; __jdc=122270672; shshshfp=158c0090e5888d932458419e12bac1d7; rkv=V0100; 3AB9D23F7A4B3C9B=VLVTNQOO6BLWETXYSO5XADLGXR7OIDM3NHDDPRNYKWBPH45RRTYXIJNGG5TFHJ5YYFBFDEARKUWAM3XO4ZWTNCDX7U; qrsc=3; shshshsID=0c6834aad4a33312fc6c9eadbfb29e65_6_1593410449685; __jdb=122270672.6.835732507|1.1593410310',
    'referer': 'https://search.jd.com/Search?keyword=python&wq=python&page=3&s=61&click=0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
}
id_comm_dict = {}
KEYWORD = parse.quote('python')

def get_comm(url,comm_num):
    #存放结果
    good_comments = ""
    #获取评论
    item_id = get_id(url)
    pages = comm_num//10
    if pages>99:
        pages = 99
    for page in range(0,pages):
        comm_url = 'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId={}&score=0&sortType=5&page={}&pageSize=10&isShadowSku=0&rid=0&fold=1'.format(item_id,page)
        headers['Referer'] = url
        html = requests.get(comm_url, headers=headers)
        json_decode = html.text
        try:
            if json_decode:
                start = json_decode.find('{"productAttr"')
                end = json_decode.find('"afterDays":0}]}') + len('"afterDays":0}]}')
                results = json.loads(json_decode[start:end])['comments']
                for result in results:
                    content = result['content']
                    good_comments += "{}|".format(content)
        except Exception as e:
            pass
    return item_id,good_comments

def get_index(url):
    session = requests.Session()
    session.headers = headers
    html = session.get(url)
    soup = BeautifulSoup(html.text,'lxml')
    items = soup.select('li.gl-item')
    for item in items:
        base = 'https://item.jd.com/'
        inner_url = item.select_one('.gl-i-wrap div.p-img a').get('href')
        inner_url = parse.urljoin(base,inner_url)
        item_id = get_id(inner_url)
        comm_num = get_comm_num(inner_url)
        # if comm_num>0:
        #     id_comm_dict[item_id] = get_comm.delay(inner_url,comm_num)
        shop_info_data = get_shop_info(inner_url)
        price = item.select('div.p-price strong i')[0].text
        shop_info_data['price'] = price
        shop_info_data['comm_num'] = comm_num
        shop_info_data['item_id'] = item_id
        print(shop_info_data)
        write_csv(shop_info_data)

head = ['shop_name','shop_evaluation','logistics','sale_server','shop_brand','price','comm_num','item_id']
def write_csv(row):
    with open('shop.csv','a+',encoding='utf-8')as f:
        csv_write = csv.DictWriter(f,head)
        csv_write.writerow(row)

def get_comm_num(url):
    item_id  = get_id(url)
    comm_url = 'https://club.jd.com/comment/productCommentSummaries.action?referenceIds={}&callback=jQuery5999681'.format(item_id)
    comment = requests.get(comm_url,headers = headers)
    json_decode = comment.text
    start = json_decode.find('{"CommentsCount":')
    end = json_decode.find('PoorRateStyle":1}]}') + len('PoorRateStyle":1}]}')
    try:
        result = json.loads(json_decode[start:end])['CommentsCount']
    except:
        return 0
    comm_num = result[0]['CommentCount']
    return comm_num
def get_shop_info(url):
    shop_data = {}
    html = requests.get(url,headers = headers)
    soup = BeautifulSoup(html.text,'lxml')
    try:
        shop_name = soup.select('div.mt h3 a')[0].text
    except:
        shop_name = '京东'
    shop_score = soup.select('.score-part span.score-detail em')
    try:
        shop_evaluation = shop_score[0].text
        logistics = shop_score[1].text
        sale_server = shop_score[2].text
    except:
        shop_evaluation = None
        logistics = None
        sale_server = None
    shop_info = soup.select('div.p-parameter ul')
    shop_brand = shop_info[0].select('ul li a')[0].text
    try:
        shop_other = shop_info[1].select('li')
        for s in shop_other:
            data = s.text.split(':')
            key = data[0]
            value = data[1]
            shop_data[key] = value
    except:
        pass
    shop_data['shop_name']= shop_name
    shop_data['shop_evaluation'] = shop_evaluation
    shop_data['logistics'] = logistics
    shop_data['sale_server'] = sale_server
    shop_data['shop_brand'] = shop_brand
    return shop_data

def get_id(url):
    id = re.compile('\d+')
    res = id.findall(url)
    return res[0]
if __name__ == '__main__':
    #先创建一个列表用来存放URL
    urls = []
    #找到他们的规律，创建一个个URL
    for i in range(1,200,2):
        url = "https://search.jd.com/Search?keyword={}&wq={}&page={}".format(KEYWORD,KEYWORD,i)
        #把创建好的URL用空元组这种形式一条条存入URLS列表里面
        urls.append(([url,],None))
    #创建100个线程
    pool = threadpool.ThreadPool(100)
    #往线程里面添加URL，makeRequests创建任务，创建100个任务
    reque = threadpool.makeRequests(get_index,urls)
    #用一个for循环线程池
    for r in reque:
        #putRequest提交这100个任务，往线程池里面提交100个任务
        pool.putRequest(r)
    #最后等待这个线程池结束
    pool.wait()