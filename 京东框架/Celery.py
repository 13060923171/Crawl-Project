from celery import Celery
import requests,re,json
app = Celery(
    'tasks',
    backend='redis://127.0.0.1:6379/2',
    broker='redis://127.0.0.1:6379/1',
)
headers = {
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
}
def get_id(url):
    id = re.compile('\d+')
    res = id.findall(url)
    return res[0]
@app.task
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
        json_decode = requests.get(comm_url,headers = headers).text
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
