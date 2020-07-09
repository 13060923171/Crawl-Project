# 项目和个人笔记
一些有趣的小项目，实现一些小功能，需要的可以下载来玩玩

一些注意事项：

# 1、关于怎么爬取抖音，这里我们得先用夜神模拟器去模拟手机的登录环境，然后再通过fiddler去抓包，然后就和我们怎么去爬取网页那就怎么去爬取APP



# 2、关于百度文库和千图，房天下，京东，都有涉及到反爬虫机制，这里你必须得会一点JavaScript才可以知道怎么去破解



# 3、这里大多数知识，你要看得懂还是建议先学好爬虫基础，再来实现这些项目



# 4、关于京东的，还有一些小缺陷没有完善，因为这里涉及到分布式的知识，说实话我分布式这块没有学好，所以不太完整，得自己去慢慢探索才行



# 5、关于未来的发展道路，可以的话可以去学习docker和k8s，这些大多数用go语言写的，对了如果学java的话，其实对于我们这些爬虫工程师来说还不如学习go语言，因为go语言大多数是基于C语言的，对于我们这些python工程师来说，比较友好



# 6、Redis内存数据库 MySQL关系数据库 mongobd文档数据库 不同的数据库对应不同的功能，大多数我们爬虫工程师都是用到Redis和MySQL，而且很多应聘都是必须要求熟练使用Redis内存数据库，善用于Redis可以大大提高我们的爬取速率



# 7、关于js破解这块，首先我们得先把破解好的js文件写一个接口去对接我们的python文件，因为毕竟这两门是不同的语言

```javascript
rsaPassword = function(t){
    var e= new D;
    return e.setPublic("xxx")
    e.encrypt(t)
}
function getPwd(pwd){
    return rsaPassword(pwd);
}
//通过这个接口把我们要破解的内容放回到getPwd这个函数里面
```



```python
#先导入我们的接口包
import execjs
#设置函数
def getpwd(password):
    #读取我们的js文件，格式为utf8
    with open("xxx.js",'r',encoding='utf8')as f:
        content = f.read()
        #然后去解析这个读取的内容
    jsdata = execjs.compile(content)
    #去看js那个函数，并且传入参数
    pw = jsdata.call('getPwd',password)
    print('pw:',pw)
    return pw


if __name__ == '__main__':
    getpwd('123456')

```

这个固定格式，基本上照着这样写就完事了，可以百分之99获取我们想要的内容

