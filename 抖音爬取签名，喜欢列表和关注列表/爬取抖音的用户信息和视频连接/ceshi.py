from urllib import parse
from xgorgon import douyin_xgorgon
import requests
import re
import time
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
    doc = requests.get(url, headers=headers,proxies=proxies).json()
    return doc

def user_name(keyword):
    url = 'https://search-hl.amemv.com/aweme/v1/discover/search/?ts=1596089594&_rticket=1596089584130&os_api=23&device_platform=android&device_type=MI%205s&iid=3535618201363773&version_code=100400&app_name=aweme&openudid=68d42b816654c06d&device_id=2638416712040606&os_version=6.0.1&aid=1128&channel=tengxun_new&ssmix=a&manifest_version_code=100401&dpi=270&cdid=6beadddd-ede3-4fc1-99f0-d351d4c76445&version_name=10.4.0&resolution=810*1440&language=zh&device_brand=Xiaomi&app_type=normal&ac=wifi&update_version_code=10409900&uuid=350000000060778'
    url = change_params(url, device_dict)
    headers = douyin_xgorgon(url=url, cookies=cookies, xtttoken=xtttoken)
    data = {
        'cursor':0,
        'keyword':keyword,
        'count': 1,
        'hot_search': 0,
        'is_pull_refresh': 1,
        'search_source': None,
        'search_id': None,
        'type': 1,
        'query_correct_type': 1
    }
    requests.packages.urllib3.disable_warnings()
    doc = requests.post(url, headers=headers,data=data,verify=False).text
    sec_uids = re.compile('"sec_uid":"(.*?)"',re.I|re.S)
    sec_uid = sec_uids.findall(doc)
    user_ids = re.compile('"uid":"(.*?)"', re.I | re.S)
    user_id= user_ids.findall(doc)
    try:
        for i in range(len(sec_uid)):
            uid = sec_uid[i]
            id = user_id[i]
            time.sleep(1)
            user_list(id,uid)
            count_list(uid)
    except:
        pass


def user_list(id,uid):
    url = 'https://api3-normal-c-lf.amemv.com/aweme/v1/user/following/list/?user_id={}&sec_user_id={}' \
          '&max_time=1595739196&count=20&offset=0' \
          '&source_type=1&address_book_access=2&gps_access=1&vcd_count=0&vcd_auth_first_time=0&ts=1595737080&cpu_support64=false&storage_type=2' \
          '&host_abi=armeabi-v7a&_rticket=1595737080341&mac_address=F4%3A09%3AD8%3A33%3AEE%3A9A&mcc_mnc=46001&os_api=23' \
          '&device_platform=android&device_type=SM-G9008V&iid=2339350999993501&version_code=110800&app_name=aweme&openudid=c5c0babc0b33a19b' \
          '&device_id=2743971277974349&os_version=6.0.1&aid=1128&channel=douyin-huidu-guanwang-control1&ssmix=a&manifest_version_code=110801&dpi=480&cdid=92d6111d-fa05-4987-a2bf-13b22d7caec2' \
          '&version_name=11.8.0&resolution=1080*1920&language=zh&device_brand=samsung&app_type=normal&ac=wifi&update_version_code=11809900&uuid=866174600901389'.format(id,uid)
    url = change_params(url, device_dict)
    headers = douyin_xgorgon(url=url, cookies=cookies, xtttoken=xtttoken)
    requests.packages.urllib3.disable_warnings()
    doc = requests.post(url, headers=headers,verify=False).json()
    try:
        total = doc["total"]
        for i in range(total):
            uid = doc["followings"][i]["uid"]
            print(uid)
            guangzhu_uid(uid)
    except:
        pass

def count_list(uid):
    url_base = 'https://api3-normal-c-lf.amemv.com/aweme/v1/aweme/favorite/?invalid_item_count=0&' \
          'is_hiding_invalid_item=0&max_cursor=0&' \
          'sec_user_id={}&count=20&os_api=22&device_type=MI%209&ssmix=a&manifest_version_code=110801&' \
          'dpi=320&uuid=866174600901389&app_name=aweme&version_name=11.8.0&ts=1596114855&cpu_support64=false&' \
          'storage_type=0&app_type=normal&ac=wifi&host_abi=armeabi-v7a&update_version_code=11809900&channel=tengxun_new&' \
          '_rticket=1596114842311&device_platform=android&iid=2339350999993501&version_code=110800&' \
          'mac_address=80%3AC5%3AF2%3A70%3A8A%3A3B&cdid=92d6111d-fa05-4987-a2bf-13b22d7caec2&' \
          'openudid=c5c0babc0b33a19b&device_id=2743971277974349&resolution=1600*900&os_version=5.1.1&language=zh&' \
          'device_brand=Xiaomi&aid=1128&mcc_mnc=46007&os_api=23' \
          '&device_platform=android&device_type=SM-G9008V&iid=2339350999993501&version_code=110800&app_name=aweme&' \
          'openudid=c5c0babc0b33a19b' \
          '&device_id=2743971277974349&os_version=6.0.1&aid=1128&channel=douyin-huidu-guanwang-control1&' \
          'ssmix=a&manifest_version_code=110801&dpi=480&cdid=92d6111d-fa05-4987-a2bf-13b22d7caec2' \
          '&version_name=11.8.0&resolution=1080*1920&language=zh&device_brand=samsung&app_type=normal&ac=wifi&' \
          'update_version_code=11809900&uuid=866174600901389'.format(uid)

    page = 0
    while 1:
        url = change_params(url_base.replace('max_cursor=0','max_cursor={}'.format(page)), device_dict)
        headers = douyin_xgorgon(url=url, cookies=cookies, xtttoken=xtttoken)
        requests.packages.urllib3.disable_warnings()
        doc = requests.post(url, headers=headers, verify=False).json()

        if doc['has_more'] !=1:
            print("没有下一页了")
            break
        if len(doc['aweme_list']) == 0:
            raise ("aweme_list Error")

        page = doc['max_cursor']
        time.sleep(1)
        try:
            for i in range(20):
                uid = doc['aweme_list'][i]['author']['uid']
                print(uid)
                xihuan_uid(uid)
        except:
            pass
        continue

def xihuan_uid(uid):
    with open("喜欢列表.txt","a+")as f:
        f.write(uid+"\n")
        print("写入成功")

def guangzhu_uid(uid):
    with open("关注列表.txt","a+")as f:
        f.write(uid+"\n")
        print("写入成功")

if __name__ == '__main__':
    while True:
        user_name("dy6i3fk5dhj4")


