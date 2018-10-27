# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import random
import os

os.environ['http_proxy'] = 'http://10.144.1.10:8080'
os.environ['https_proxy'] = 'https://10.144.1.10:8080'


base_url = "https://baike.baidu.com"
his = ["/item/%E7%BD%91%E7%BB%9C%E7%88%AC%E8%99%AB/5162711"]  #a = "网络爬虫"

for i in range(1):
    # dealing with Chinese symbols
    url = base_url + his[-1]
    html = urlopen(url).read().decode('utf-8')
    print('html:' + html)
    soup = BeautifulSoup(html, features='lxml')
    print(i, soup.find('h1').get_text(), '    url: ', his[-1])

    # find valid urls
    sub_urls = soup.find_all("a", {"target": "_blank", "href": re.compile("/item/(%.{2})+$")})

    if len(sub_urls) != 0:
        his.append(random.sample(sub_urls, 1)[0]['href'])
    else:
        # no valid sub link found
        his.pop()