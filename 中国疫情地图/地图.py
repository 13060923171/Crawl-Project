import requests
import json
import re
from pyecharts.charts import Map
from pyecharts import options
#先请求到数据的页面
result = requests.get(
    'https://interface.sina.cn/news/wap/fymap2020_data.d.json?1580097300739&&callback=sinajp_1580097300873005379567841634181')
#用正则去获取具体的数字
json_str = re.search("\(+([^)]*)\)+", result.text).group(1)
html = f"{json_str}"
#然后用json把json转化为python
table = json.loads(f"{html}")
province_data = []
for province in table['data']['list']:
    province_data.append((province['name'], province['value']))
city_data = []
# 循环获取城市名称和对应的确诊数据
for city in province['city']:
    # 这里要注意对应上地图的名字需要使用mapName这个字段
    city_data.append((city['mapName'], city['conNum']))
# 使用Map，创建省份地图
map_province = Map()
# 设置地图上的标题和数据标记，添加省份和确诊人数
map_province.set_global_opts(title_opts=options.TitleOpts(
    title=province['name'] + "全国疫情的总数：" + province['value']),
    visualmap_opts=options.VisualMapOpts(is_piecewise=True,  # 设置是否为分段显示
                                         # 自定义数据范围和对应的颜色，这里我是取色工具获取的颜色值，不容易呀。
                                         pieces=[
                                             {"min": 1000, "label": '>1000',
                                              "color": "#6F171F"},
                                             {"min": 500, "max": 1000,
                                              "label": '500-1000', "color": "#C92C34"},
                                             {"min": 100, "max": 499,
                                              "label": '100-499', "color": "#E35B52"},
                                             {"min": 10, "max": 99,
                                              "label": '10-99', "color": "#F39E86"},
                                             {"min": 1, "max": 9, "label": '1-9', "color": "#FDEBD0"}]))
# 将 数据添加进去，生成省份地图，所以maptype要对应省份。
map_province.add("确诊人数：", city_data, maptype=province['name'])
# 一切完成，那么生成一个省份的html网页文件，取上对应省份的名字。

# 创建国家地图
map_country = Map()
# 设置地图上的标题和数据标记，添加确诊人数
map_country.set_global_opts(title_opts=options.TitleOpts(
    title="全国确诊人数：" + str(table['data']["gntotal"])),
    visualmap_opts=options.VisualMapOpts(is_piecewise=True,  # 设置是否为分段显示
                                         # 自定义数据范围和对应的颜色，这里我是取色工具获取的颜色值，不容易呀。
                                         pieces=[
                                             # 不指定 max，表示 max 为无限大（Infinity）。
                                             {"min": 1000, "label": '>1000',
                                              "color": "#6F171F"},
                                             {"min": 500, "max": 1000,
                                              "label": '500-1000', "color": "#C92C34"},
                                             {"min": 100, "max": 499,
                                              "label": '100-499', "color": "#E35B52"},
                                             {"min": 10, "max": 99,
                                              "label": '10-99', "color": "#F39E86"},
                                             {"min": 1, "max": 9, "label": '1-9', "color": "#FDEBD0"}]))
# 将数据添加进去，生成中国地图，所以maptype要对应china。
map_country.add("确诊人数：", province_data, maptype="china")
# 一切完成，那么生成一个html网页文件。
map_country.render("country.html")
print("生成完成！！！")