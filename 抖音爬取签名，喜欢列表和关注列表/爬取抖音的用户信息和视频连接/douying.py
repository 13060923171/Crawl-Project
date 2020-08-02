import requests
import urllib3
'''
GET https://api3-core-c-hl.amemv.com/aweme/v1/aweme/post/?source=0&publish_video_strategy_type=0&max_cursor=1587528101000&sec_user_id=MS4wLjABAAAA4s3jerVDPUA_xvyoGhRypnn8ijAtUfrt9rCWL2aXxtU&count=10&ts=1587635299&host_abi=armeabi-v7a&_rticket=1587635299508&mcc_mnc=46007& HTTP/1.1
Host: api3-core-c-hl.amemv.com
Connection: keep-alive
Cookie: odin_tt=fab0188042f9c0722c90b1fbaf5233d30ddb78a41267bacbfc7c1fb216d37344df795f4e08e975d557d0c274b1c761da039574e4eceaae4a8441f72167d64afb
X-SS-REQ-TICKET: 1587635299505
sdk-version: 1
X-SS-DP: 1128
x-tt-trace-id: 00-a67026290de17aa15402ce8ee4a90468-a67026290de17aa1-01
User-Agent: com.ss.android.ugc.aweme/100801 (Linux; U; Android 5.1.1; zh_CN; MI 9; Build/NMF26X; Cronet/TTNetVersion:8109b77c 2020-04-15 QuicVersion:0144d358 2020-03-24)
X-Gorgon: 0404c0d100004fe124c18b36d03baf0768c181e105b1af5e8167
X-Khronos: 1587635299
x-common-params-v2: os_api=22&device_platform=android&device_type=MI%209&iid=78795828897640&version_code=100800&app_name=aweme&openudid=80c5f2708a3b6304&device_id=3966668942355688&os_version=5.1.1&aid=1128&channel=tengxun_new&ssmix=a&manifest_version_code=100801&dpi=320&cdid=e390170c-0cb5-42ad-8bf6-d25dc4c7e3a3&version_name=10.8.0&resolution=900*1600&language=zh&device_brand=Xiaomi&app_type=normal&ac=wifi&update_version_code=10809900&uuid=863254643501389


'''


# 下载视频代码，创建一个文件夹来存放抖音的视频
def download_video(url, title):
    with open("{}.mp4".format(title), "wb") as f:
        f.write(requests.get(url).content)
    print("下载视频{}完毕".format(title))

#怎么去爬取APP里面的视频
def get_video():
    #通过我们的fiddler这个抓包工具来获取我们想要爬取某个账户里面全部视频的URL
    url = "GET https://api3-core-c-lf.amemv.com/aweme/v1/aweme/post/?source=0&publish_video_strategy_type=0&max_cursor=1590752981000&sec_user_id=MS4wLjABAAAAcXW9VYbv07hczERdiLoQil_TRW6GbwWc_BuRU1pczaCq9GQavlvKFhl_qIqE4yZ6&count=10&ts=1594477988&cpu_support64=false&storage_type=0&host_abi=armeabi-v7a&_rticket=1594477986155&mac_address=80%3AC5%3AF2%3A70%3A8A%3A3B&mcc_mnc=46007& HTTP/1.1"
    #构建我们的headers，这些对应的数据都是通过我们的fiddler获取的
    headers = {
        'Host': 'api3-core-c-lf.amemv.com',
        'Connection': 'keep-alive',
        'Cookie': 'install_id=2339350999993501; ttreq=1$7a4d72914f4cef66e2e2ff13b5dc74a9ab180c06; passport_csrf_token=a4f3fb89f64b4fa8c707293c951c0c17; d_ticket=19b0a970bd0b508bdde6a5128f580f540c2d6; odin_tt=c3c9b378984696b77432b71b951c0e34a773411cce385120c69196cc6529b214c7d5c8716d1fc6f4cc2cb701d61a48b4; sid_guard=fdbd63a338be8acb4a08a1621c41fea6%7C1594464835%7C5184000%7CWed%2C+09-Sep-2020+10%3A53%3A55+GMT; uid_tt=760bb76af4748dcf85a4a0c5a9c5b146; uid_tt_ss=760bb76af4748dcf85a4a0c5a9c5b146; sid_tt=fdbd63a338be8acb4a08a1621c41fea6; sessionid=fdbd63a338be8acb4a08a1621c41fea6; sessionid_ss=fdbd63a338be8acb4a08a1621c41fea6',
        'X-SS-REQ-TICKET': '1594464868804',
        'passport-sdk-version': '17',
        'X-Tt-Token': '00fdbd63a338be8acb4a08a1621c41fea6c5165e3a78a6e6e8bad4d8602a9fba4f29f111b5425b14f07ecf6df18c6b940518',
        'sdk-version': '2',
        'X-SS-DP': '1128',
        'x-tt-trace-id': '00-3d831b3e0d9bfa0994c2b4de0dc30468-3d831b3e0d9bfa09-01',
        'User-Agent': 'com.ss.android.ugc.aweme/110801 (Linux; U; Android 5.1.1; zh_CN; OPPO R11 Plus; Build/NMF26X; Cronet/TTNetVersion:71e8fd11 2020-06-10 QuicVersion:7aee791b 2020-06-05)',
        'Accept-Encoding': 'gzip, deflate',
        'X-Gorgon': '0404d8954001fffd06f451b46c120f09798b487f8c591c2f6bce',
        'X-Khronos': '1594464868',
        'x-common-params-v2': 'os_api=22&device_platform=android&device_type=OPPO%20R11%20Plus&iid=2339350999993501&version_code=110800&app_name=aweme&openudid=c5c0babc0b33a19b&device_id=2743971277974349&os_version=5.1.1&aid=1128&channel=tengxun_new&ssmix=a&manifest_version_code=110801&dpi=320&cdid=92d6111d-fa05-4987-a2bf-13b22d7caec2&version_name=11.8.0&resolution=900*1600&language=zh&device_brand=OPPO&app_type=normal&ac=wifi&update_version_code=11809900&uuid=866174600901389',
    }

    #无视证书的请求
    requests.packages.urllib3.disable_warnings()
    html = requests.get(url, headers=headers, verify=False)
    #把数据用json来全部获取下来
    json_data = html.json()["aweme_list"]
    #循环叠带我们的数据，把它们一一展示出来
    for j in json_data:
        title = j['desc']
        print(title)
        print(j['video']['play_addr']['url_list'][0])
        #把最后每个视频对应的URL打印出来，再根据我们的下载函数，把它们全部下载到自己的电脑里面
        download_video(j['video']['play_addr']['url_list'][0], title)


if __name__ == '__main__':
    get_video()