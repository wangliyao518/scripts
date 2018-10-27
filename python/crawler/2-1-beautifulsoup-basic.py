# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from urllib.request import urlopen
import os

os.environ['http_proxy'] = 'http://10.144.1.10:8080'
os.environ['https_proxy'] = 'https://10.144.1.10:8080'
# if has Chinese, apply decode()
html = urlopen("https://wangliyao518.github.io/about/").read().decode('utf-8')

soup = BeautifulSoup(html, features='lxml')
print(soup.h1)
print('\n', soup.p)

all_href = soup.find_all('a')
print('=='*10)
for line in all_href:
    if hasattr(line, 'href'):
    	print(line.get('href'))
