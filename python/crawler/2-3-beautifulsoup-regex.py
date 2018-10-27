# -*- coding: utf-8 -*-
import os
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re

os.environ['http_proxy'] = 'http://10.144.1.10:8080'
os.environ['https_proxy'] = 'https://10.144.1.10:8080'

# if has Chinese, apply decode()
html = urlopen("https://morvanzhou.github.io/static/scraping/table.html").read().decode('utf-8')

soup = BeautifulSoup(html, features='lxml')

img_links = soup.find_all("img", {"src": re.compile('.*?\.jpg')})
for link in img_links:
    print(link['src'])

print('\n')

course_links = soup.find_all('a', {'href': re.compile('https://morvan.*')})
for link in course_links:
    print(link['href'])