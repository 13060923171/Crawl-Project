import requests
from selenium import webdriver
from lxml import etree
import re
from selenium.webdriver.common.keys import Keys
import time
from PIL import Image
import os
from bs4 import BeautifulSoup
from docx import Document
import sys

#首先先去获取这个函数
def get_html(url):
    try:
        #这里用到防错机制先获取这个页面用get方法
        r = requests.get(url,headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.62 Safari/537.36"})
        #这句话的意思就是这个HTTP回应内容的编码方式 =这个内容的备用编码方式，
        # 这样写的意义就是不用指定某种编码，而是直接调用这个内容的编码
        r.encoding = r.apparent_encoding
        #放回这个内容以text的形式
        return r.text
    except:
        print("URL request error")

