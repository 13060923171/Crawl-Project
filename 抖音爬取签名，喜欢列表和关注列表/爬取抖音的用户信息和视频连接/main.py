from urllib import parse
from xgorgon import douyin_xgorgon
import requests
import re

cookies = "sessionid="
xtttoken = ""

device_dict ={'iid': '',
              'device_id': '',
              'openudid': '',
              'uuid': '',
              'cdid': ''
              }

def change_params(url,device_dict=None):
    params_item = {}
    lot_url = url.split('?')[0]+'?'
    for i in parse.urlparse(url).query.split('&'):
        k = i.split('=')[0]
        try:
            params_item[k] = i.split('=')[1]
        except:
            params_item[k] = None
    if device_dict:
        params_item['openudid'] = device_dict['openudid']
        params_item['iid']= device_dict['iid']
        params_item['device_id']= device_dict['device_id']
        params_item['uuid']= device_dict['uuid']
        params_item['cdid']= device_dict['cdid']
    new_url = lot_url+parse.unquote_plus(parse.urlencode(params_item))
    return new_url

def get(url,proxies=None):
    headers = douyin_xgorgon(url=url,cookies=cookies,xtttoken=xtttoken)
    doc = requests.get(url, headers=headers,proxies=proxies, verify=False).json()
    return doc


device_dict ={'iid': '3729134641503981',
              'device_id': '2743971277974349',
              'openudid': 'c5c0babc0b33a19b',
              'uuid': '866174600901389',
              'cdid': 'a4ff527f-e409-47ce-ae32-59c555cdd653'
              }



'''搜索用户列表'''
def search_user(keyword,cursor):
    """
    搜索用户信息
    keyword: 关键词
    :return: response->json
    """
    url ='https://search-hl.amemv.com/aweme/v1/discover/search/?ts=1594792387&_rticket=1594187269781&os_api=23&device_platform=android&device_type=MI%205s&iid=3729134641503981&version_code=100400&app_name=aweme&openudid=c5c0babc0b33a19b&device_id=2743971277974349&os_version=6.0.1&aid=1128&channel=tengxun_new&ssmix=a&manifest_version_code=100401&dpi=270&cdid=a4ff527f-e409-47ce-ae32-59c555cdd653&version_name=10.4.0&resolution=810*1440&language=zh&device_brand=Xiaomi&app_type=normal&ac=wifi&update_version_code=10409900&uuid=866174600901389'
    url = change_params(url)
    headers = douyin_xgorgon(url=url,cookies=cookies,xtttoken=xtttoken)
    data = {
            'cursor': cursor,
            'keyword':keyword,
            'count': 10,
            'hot_search': 0,
            'is_pull_refresh': 1,
            'search_source': None,
            'search_id':None,
            'type':1,
            'query_correct_type': 1
            }
    requests.packages.urllib3.disable_warnings()
    doc = requests.post(url, headers=headers,data=data, verify=False).text
    print(doc)
    # sec_uid = re.compile('"sec_uid":"(.*?)"',re.I | re.S)
    # sec_uids = sec_uid.findall(doc)
    # has_more = re.compile('"has_more":(.*?),', re.I | re.S)
    # result = has_more.findall(doc)
    # for i in sec_uids:
    #     with open('shuju6.text','a+')as f:
    #         f.write(i)
    #         f.write('\n')
    #         print('保存完毕')
    #     print(i)
    # print(result)


if __name__ == '__main__':
    # for i in range(0,1000,30):
    search_user('美妆',30)



