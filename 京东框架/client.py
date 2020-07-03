import redis
import json
def write_csv(row):
    with open('shop.txt','a+',encoding='utf8')as f:
        f.write(str(row)+'\n')
r = redis.Redis(host='127.0.0.1',port=6379,db=2)
keys = r.keys()
for key in keys():
    res = r.get(key)
    res = json.loads(res.decode('utf-8'))
    results = res.get('result')
    write_csv(results)