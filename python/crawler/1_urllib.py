# -*- coding: utf-8 -*-
import os
from urllib.request import urlopen
import re

os.environ['http_proxy'] = 'http://10.144.1.10:8080'
os.environ['https_proxy'] = 'https://10.144.1.10:8080'
# if has Chinese, apply decode()
html = urlopen("https://wangliyao518.github.io/about/").read().decode('utf-8')
print(html)


res = re.findall(r"<title>(.+?)</title>", html)
print("\nPage title is: ", res[0])


res = re.findall(r"<p>(.*?)</p>", html, flags=re.DOTALL)    # re.DOTALL if multi line
for line, content in enumerate(res):
    print("\nPage {} paragraph is: {} ".format(line, content))


res = re.findall(r'href="(.*?)"', html)
print("\nAll links: ", res)
