import requests

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
    url = "https://api3-core-c-hl.amemv.com/aweme/v1/aweme/post/?source=0&publish_video_strategy_type=0&max_cursor=1587528101000&sec_user_id=MS4wLjABAAAA4s3jerVDPUA_xvyoGhRypnn8ijAtUfrt9rCWL2aXxtU&count=10&ts=1587635299&host_abi=armeabi-v7a&_rticket=1587635299508&mcc_mnc=46007&"
    #构建我们的headers，这些对应的数据都是通过我们的fiddler获取的
    headers = {
        'Cookie': 'odin_tt=fab0188042f9c0722c90b1fbaf5233d30ddb78a41267bacbfc7c1fb216d37344df795f4e08e975d557d0c274b1c761da039574e4eceaae4a8441f72167d64afb',
        'X-SS-REQ-TICKET': '1587635299505',
        'sdk-version': '1',
        'X-SS-DP': '1128',
        'x-tt-trace-id': '00-a67026290de17aa15402ce8ee4a90468-a67026290de17aa1-01',
        'User-Agent': 'com.ss.android.ugc.aweme/100801 (Linux; U; Android 5.1.1; zh_CN; MI 9; Build/NMF26X; Cronet/TTNetVersion:8109b77c 2020-04-15 QuicVersion:0144d358 2020-03-24)',
        'X-Gorgon': '0404c0d100004fe124c18b36d03baf0768c181e105b1af5e8167',
        'X-Khronos': '1587635299',
        'x-common-params-v2': 'os_api=22&device_platform=android&device_type=MI%209&iid=78795828897640&version_code=100800&app_name=aweme&openudid=80c5f2708a3b6304&device_id=3966668942355688&os_version=5.1.1&aid=1128&channel=tengxun_new&ssmix=a&manifest_version_code=100801&dpi=320&cdid=e390170c-0cb5-42ad-8bf6-d25dc4c7e3a3&version_name=10.8.0&resolution=900*1600&language=zh&device_brand=Xiaomi&app_type=normal&ac=wifi&update_version_code=10809900&uuid=863254643501389'
    }
    #无视证书的请求
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