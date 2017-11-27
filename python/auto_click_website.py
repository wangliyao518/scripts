# -*- coding: utf-8 -*-
# import urllib2, base64
# # 
# if __name__ == '__main__':
#     # IP for the router
#     ip = '192.168.1.1'
#     # 登录的用户名和密码
#     login_user = 'admin'
#     login_pw = 'admin'
#  
#     # 请求地址
#     url = 'http://' + ip + '/userRpm/SysRebootRpm.htm?Reboot=%D6%D8%C6%F4%C2%B7%D3%C9%C6%F7'
#     auth = 'Basic ' + base64.b64encode(login_user+':'+login_pw)
#     print auth  #Authorization=Basic%20YWRtaW46bWw1MDMwMjU5OTg%3D
#     heads = { 'Referer' : 'http://' + ip + '/userRpm/SysRebootRpm.htm',
#              'Authorization' : auth
#     }
#      
#     # 发送请求
#     request = urllib2.Request(url, None, heads)
#     response = urllib2.urlopen(request)
#     print response.read()

# login_user = 'admin'
# login_pw = 'admin'
# auth = 'Basic ' + base64.b64encode(login_user+':'+login_pw)
# 
# url = "http://192.168.1.1"
# req = urllib2.Request(url) 
# print '---', req, auth
# req.add_header("Authorization", auth)  #basic64 编码的admin admin
# resp = urllib2.urlopen(req)
# html = resp.read()
# print html
# resp.close()

import urllib
import time
import os
os.environ['http_proxy'] = ""
os.environ['https_proxy'] = ""

http_address = ["http://www.17k.com/chapter/1412334/21671446.html",
                "http://www.17k.com/chapter/1412334/21671464.html",
                "http://www.17k.com/chapter/1412334/21671482.html",
                "http://www.17k.com/chapter/1412334/21671489.html",
                "http://www.17k.com/chapter/1412334/21679700.html",
                "http://www.17k.com/chapter/1412334/21671496.html",
                ]
# for t, address in enumerate(http_address):
#     print "time:", t
#     print urllib.urlopen(address).read()
#     time.sleep(30)
print urllib.urlopen("http://test-community.china.net/2015/tta/mtl/2015-10-30/208.html").info()


