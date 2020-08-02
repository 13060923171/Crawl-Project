import requests
import pandas as pd
from pprint import pprint
from lxml import etree
import time
import warnings
warnings.filterwarnings("ignore")

for i in range(1,1501):
    print("正在爬取第" + str(i) + "页的数据")
    url_pre = "https://search.51job.com/list/000000,000000,0000,00,9,99,%25E6%2595%25B0%25E6%258D%25AE,2,"
    url_end = ".html?"
    url = url_pre + str(i) + url_end
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }
    web = requests.get(url, headers=headers)
    web.encoding = "gbk"
    dom = etree.HTML(web.text)
    # 1、岗位名称
    job_name = dom.xpath('//div[@class="dw_table"]/div[@class="el"]//p/span/a[@target="_blank"]/@title')
    # 2、公司名称
    company_name = dom.xpath('//div[@class="dw_table"]/div[@class="el"]/span[@class="t2"]/a[@target="_blank"]/@title')
    # 3、工作地点
    address = dom.xpath('//div[@class="dw_table"]/div[@class="el"]/span[@class="t3"]/text()')
    # 4、工资
    salary_mid = dom.xpath('//div[@class="dw_table"]/div[@class="el"]/span[@class="t4"]')
    salary = [i.text for i in salary_mid]
    # 5、发布日期
    release_time = dom.xpath('//div[@class="dw_table"]/div[@class="el"]/span[@class="t5"]/text()')
    # 6、获取二级网址url
    deep_url = dom.xpath('//div[@class="dw_table"]/div[@class="el"]//p/span/a[@target="_blank"]/@href')
    RandomAll = []
    JobDescribe = []
    CompanyType = []
    CompanySize = []
    Industry = []
    for i in range(len(deep_url)):
        web_test = requests.get(deep_url[i], headers=headers)
        web_test.encoding = "gbk"
        dom_test = etree.HTML(web_test.text)
        # 7、爬取经验、学历信息，先合在一个字段里面，以后再做数据清洗。命名为random_all
        random_all = dom_test.xpath('//div[@class="tHeader tHjob"]//div[@class="cn"]/p[@class="msg ltype"]/text()')
        # 8、岗位描述性息
        job_describe = dom_test.xpath('//div[@class="tBorderTop_box"]//div[@class="bmsg job_msg inbox"]/p/text()')
        # 9、公司类型
        company_type = dom_test.xpath('//div[@class="tCompany_sidebar"]//div[@class="com_tag"]/p[1]/@title')
        # 10、公司规模(人数)
        company_size = dom_test.xpath('//div[@class="tCompany_sidebar"]//div[@class="com_tag"]/p[2]/@title')
        # 11、所属行业(公司)
        industry = dom_test.xpath('//div[@class="tCompany_sidebar"]//div[@class="com_tag"]/p[3]/@title')
        # 将上述信息保存到各自的列表中
        RandomAll.append(random_all)
        JobDescribe.append(job_describe)
        CompanyType.append(company_type)
        CompanySize.append(company_size)
        Industry.append(industry)
        # 为了反爬，设置睡眠时间
        time.sleep(1)
    # 由于我们需要爬取很多页，为了防止最后一次性保存所有数据出现的错误，因此，我们每获取一夜的数据，就进行一次数据存取。
    df = pd.DataFrame()
    df["岗位名称"] = job_name
    df["公司名称"] = company_name
    df["工作地点"] = address
    df["工资"] = salary
    df["发布日期"] = release_time
    df["经验、学历"] = RandomAll
    df["公司类型"] = CompanyType
    df["公司规模"] = CompanySize
    df["所属行业"] = Industry
    df["岗位描述"] = JobDescribe
    # 这里在写出过程中，有可能会写入失败，为了解决这个问题，我们使用异常处理。
    try:
        df.to_csv("job_info.csv", mode="a+", header=None, index=None, encoding="gbk")
    except:
        print("当页数据写入失败")
    time.sleep(1)

