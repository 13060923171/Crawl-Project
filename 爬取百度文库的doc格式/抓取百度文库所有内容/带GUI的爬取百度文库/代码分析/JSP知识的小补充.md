# JSP知识的小补充
## 网页组成

网页是由 HTML 、 CSS 、JavaScript 组成的。

HTML 是用来搭建整个网页的骨架，而 CSS 是为了让整个页面更好看，包括我们看到的颜色，每个模块的大小、位置等都是由 CSS 来控制的， JavaScript 是用来让整个网页“动起来”，这个动起来有两层意思，一层是网页的数据动态交互，还有一层是真正的动，比如我们都见过一些网页上的动画，一般都是由 JavaScript 配合 CSS 来完成的。

不同类型的文字通过不同类型的标签来表示，如图片用 <img> 标签表示，视频用 <video> 标签表示，段落用 <p> 标签表示，它们之间的布局又常通过布局标签 <div> 嵌套组合而成，各种标签通过不同的排列和嵌套才形成了网页的框架。

在右边 Style 标签页中，显示的就是当前选中的 HTML 代码标签的 CSS 层叠样式，“层叠”是指当在HTML中引用了数个样式文件，并且样式发生冲突时，浏览器能依据层叠顺序处理。“样式”指网页中文字大小、颜色、元素间距、排列等格式。

而 JavaScript 就厉害了，它在 HTML 代码中通常使用 <script> 进行包裹，可以直接书写在 HTML 页面中，也可以以文件的形式引入。

## JSP

JavaScript的名字使得很多人会将其与Java语言联系起来，认为它是Java的某种派生语言，但实际上JavaScript在设计原则上更多受到了Scheme（一种函数式编程语言）和C语言的影响，除了变量类型和命名规范等细节，JavaScript与Java关系并不大。

Netscape公司最初为之命名“LiveScript”，但当时正与Sun公司合作，加上Java语言所获得的巨大成功，为了“蹭热点”，遂将其名字改为“JavaScript”。JavaScript推出后受到了业界的一致肯定，对JavaScript的支持也成为在21世纪出现的现代浏览器的基本要求。

浏览器端的脚本语言还包括用于Flash动画的ActionScript等。

为了在网页中使用JavaScript，开发者一般会把JavaScript脚本程序写在HTML的<script>标签中。在HTML语法里，<script>标签用于定义客户端脚本，如果需要引用外部脚本文件，可以在src属性中设置其地址，如下图所示。

![image-20200427235704505](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20200427235704505.png)

## 常用操作
- 隐藏百度图片

```python
from selenium import webdriver

driver = webdriver.PhantomJS()
driver.get("https://www.baidu.com/")

# 给搜索输入框标红的javascript脚本
js = "var q=document.getElementById(\"kw\");q.style.border=\"2px solid red\";"

# 调用给搜索输入框标红js脚本
driver.execute_script(js)

#查看页面快照
driver.save_screenshot("redbaidu.png")

#js隐藏元素，将获取的图片元素隐藏
img = driver.find_element_by_xpath("//*[@id='lg']/img")
driver.execute_script('$(arguments[0]).fadeOut()',img)

# 向下滚动到页面底部
driver.execute_script("$('.scroll_top').click(function(){$('html,body').animate({scrollTop: '0px'}, 800);});")

#查看页面快照
driver.save_screenshot("nullbaidu.png")

driver.quit()
```

- 模拟滚动条滚动到底部

```python
# 
from selenium import webdriver
import time

driver = webdriver.PhantomJS()
driver.get("https://movie.douban.com/typerank?type_name=剧情&type=11&interval_id=100:90&action=")

# 向下滚动10000像素
js = "document.body.scrollTop=10000"
#js="var q=document.documentElement.scrollTop=10000"
time.sleep(3)

#查看页面快照
driver.save_screenshot("douban.png")

# 执行JS语句
driver.execute_script(js)
time.sleep(10)

#查看页面快照
driver.save_screenshot("newdouban.png")

driver.quit()
```

