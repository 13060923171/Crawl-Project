import requests
import uuid
from urllib import parse
import math
import execjs
import os
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
    "accept-language": "zh-CN,zh;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "cache-control": "max-age=600",
    "Referer": "https://y.qq.com/portal/singer_list.html",
}
def get_singer_mid(index):
    #index=1---27
    data='{"comm":{"ct":24,"cv":0},"singerList":{"module":"Music.SingerListServer"' \
          ',"method":"get_singer_list","param":{"area":-100,"sex":-100,"genre":-100,' \
            '"index":%s,"sin":0,"cur_page":1}}}' % (str(index))
    url='https://u.y.qq.com/cgi-bin/musicu.fcg?-=getUCGI0432880619182503' \
          '&g_tk=571600846&loginUin=0&hostUin=0&format=json&inCharset=utf8&out' \
          'Charset=utf-8&notice=0&platform=yqq.json&needNewCode=0' \
          '&data={}'.format(parse.quote(data))
    html=requests.get(url).json()
    total=html["singerList"]["data"]["total"]
    pages=int(math.floor(int(total)/80))
    thread_number=pages
    Thread=ThreadPoolExecutor(max_workers=thread_number)
    sin = 0
    for page in range(1, pages):
        data = '{"comm":{"ct":24,"cv":0},"singerList":{"module":"Music.SingerListServer",' \
               '"method":"get_singer_list","param":{"area":-100,"sex":-100,"genre":-100,"' \
               'index":%s,"sin":%d,"cur_page":%s}}}' % (str(index), sin, str(page))

        url = 'https://u.y.qq.com/cgi-bin/musicu.fcg?-=getUCGI0432880619182503' \
              '&g_tk=571600846&loginUin=0&hostUin=0&format=json&inCharset=utf8&out' \
              'Charset=utf-8&notice=0&platform=yqq.json&needNewCode=0' \
              '&data={}'.format(parse.quote(data))
        html=requests.get(url,headers=headers).json()
        sings=html['singerList']['data']['singerlist']
        for sing in sings:
            singer_name = sing['singer_name']
            mid = sing['singer_mid']
            get_singer_data(mid,singer_name)
        sin += 80

def get_singer_data(mid,singer_name):
    params = '{"comm":{"ct":24,"cv":0},"singerSongList":{"method":"GetSingerSongList",' \
             '"param":{"order":1,"singerMid":"%s","begin":0,"num":10},' \
             '"module":"musichall.song_list_server"}}' % str(mid)

    url = 'https://u.y.qq.com/cgi-bin/musicu.fcg?-=getSingerSong9513357793133783&' \
          'g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8' \
          '&notice=0&platform=yqq.json&needNewCode=0*&data={}'.format(parse.quote(params))
    html=requests.session()
    content=html.get(url,headers=headers).json()
    songs_num=content['singerSongList']['data']['totalNum']

    if int(songs_num)<=80:
        params = '{"comm":{"ct":24,"cv":0},"singerSongList":{"method":"GetSingerSongList",' \
                 '"param":{"order":1,"singerMid":"%s","begin":0,"num":%s},' \
                 '"module":"musichall.song_list_server"}}' % (str(mid), str(songs_num))

        url = 'https://u.y.qq.com/cgi-bin/musicu.fcg?-=getSingerSong9513357793133783&' \
              'g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8' \
              '&notice=0&platform=yqq.json&needNewCode=0*&data={}'.format(parse.quote(params))
        html = requests.session()
        content =html.get(url,headers=headers).json()
        datas = content['singerSongList']['data']['songList']
        for song in datas:
            song_name = song['songInfo']['name']
            song_ablum = song['songInfo']['album']['name']
            singer_name = singer_name
            song_mid = song['songInfo']['mid']
            print(singer_name,song_name,song_ablum,song_mid)

    else:
        for a in range(0,songs_num,80):
            params = '{"comm":{"ct":24,"cv":0},"singerSongList":{"method":"GetSingerSongList",' \
                     '"param":{"order":1,"singerMid":"%s","begin":%s,"num":%s},' \
                     '"module":"musichall.song_list_server"}}' % (str(mid), int(a), int(songs_num))

            url = 'https://u.y.qq.com/cgi-bin/musicu.fcg?-=getSingerSong9513357793133783&' \
                  'g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8' \
                  '&notice=0&platform=yqq.json&needNewCode=0*&data={}'.format(parse.quote(params))
            html = requests.session()
            content = html.get(url, headers=headers).json()
            datas = content['singerSongList']['data']['songList']
            for song in datas:
                song_name = song['songInfo']['name']
                song_ablum = song['songInfo']['album']['name']
                singer_name = singer_name
                song_mid = song['songInfo']['mid']
                print(singer_name,song_name,song_ablum,song_mid)
                download(song_mid,singer_name)
def download(song_mid,sing_name):
    headers = {
        'cookie': 'pgv_pvid=2128245208; pac_uid=0_6b1c785781d54; pgv_pvi=772980736; RK=8x5lwvVnY1;'
                  ' ptcz=baca3422f148c8897bd71cb3765e7c08bf0dddc2aac46b34eb2f6b669e38d215;'
                  ' ptui_loginuin=1766228968@qq.com; ts_refer=www.baidu.com/link; ts_uid=2958609676; '
                  'pgv_si=s6667516928; pgv_info=ssid=s1048782460; player_exist=1; qqmusic_fromtag=66;'
                  ' userAction=1; yqq_stat=0; _qpsvr_localtk=0.5664181233633159;'
                  'psrf_qqunionid=E7D5E8B282E958B5ED555246677BCD41; psrf_qqrefresh_'
                  'token=DC32336F11952FA5867192F46CF15FD5; tmeLoginType=2; qqmusic_'
                  'key=Q_H_L_2Sqn2y50eyOV1i5dcbk613wim45KnxmEK5ofj1RsBgxgHN-xLkK25EjEAQ2jvs1;'
                  ' psrf_qqopenid=33B542A190FCA799A663FDDCB25EA8F0; qm_'
                  'keyst=Q_H_L_2Sqn2y50eyOV1i5dcbk613wim45KnxmEK5ofj1RsBgxgHN-xLkK25EjEAQ2jvs1; '
                  'euin=oK4qNe-l7KvPoz**; psrf_access_token_expiresAt=1601793607; '
                  'psrf_musickey_createtime=1594017607; psrf_qqaccess_token=8838D613ABE40CD4A345D8E550EBB967; '
                  'uin=1598275443; ts_last=y.qq.com/portal/player.html; yplayer_open=1; yq_index=3',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
        'referer': 'https://y.qq.com/portal/player.html'
    }

    data = '{"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":' \
           '{"guid":"2128245208","songmid":["%s"],"songtype":[0],"uin":"1598275443","loginflag"' \
           ':1,"platform":"20"}},"comm":{"uin":1598275443,"format":"json","ct":24,"cv":0}}' % str(
        song_mid)
    url = 'https://u.y.qq.com/cgi-bin/musicu.fcg?-=getplaysongvkey17693804549459324' \
          '&g_tk=5381&loginUin=3262637034&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8' \
          '&notice=0&platform=yqq.json&needNewCode=0&data={}'.format(parse.quote(data))
    vkey = requests.get(url, headers=headers)
    purl = vkey.json()['req_0']['data']['midurlinfo'][0]['purl']
    url = 'https://ws.stream.qqmusic.qq.com/' + purl
    html = requests.get(url)
    filename = 'qq音乐'
    if not os.path.exists(filename):
        os.makedirs(filename)
    with open('./{}/{}.m4a'.format(filename, sing_name), 'wb') as f:
        print('\n正在下载{}歌曲.....\n'.format(sing_name))
        f.write(html.content)




if __name__ == '__main__':
    get_singer_mid(2)