#!/usr/bin/python
# -*- coding: UTF-8 -*-
import threading
import paramiko
import time
import threadpool
import glob 
import os
import re


TEST_LINE_INFO = {}
TEST_LINE_IP_LIST = []

def _get_host_ip(file_name):
    with open(file_name) as p_file:
        line_number = 0
        tag = False
        while 1:
            lines = p_file.readlines(5000)
            if not lines:
                break
            for line in lines:
                line_number = line_number + 1
                pattern = r"=.*FsmControlPc.*\("
                ret = re.findall(pattern, line)
                if ret != []:
                    tag = True
                    line_temp = line_number
                    continue
                if tag and line_number == line_temp + 1:
                    pattern = r"host='(\S+)'"
                    ret = re.findall(pattern, line)
                    return ret[0]

def _fill_testline_info(config_dir):
    file_list = glob.glob("%s/*/enb.py" % config_dir)
    for each_file in file_list:
        testline_ip = _get_host_ip(each_file)
        TEST_LINE_IP_LIST.append(testline_ip)
        TEST_LINE_INFO[os.path.basename(os.path.dirname(each_file))] = testline_ip

def mySsh(ip):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        username = 'test'
        password = 'test'
        cmd = ['java -version', 'wget http://10.*.*.*/kiss/tools/upgrade_java-8.sh', 'chmod +x upgrade_java-8.sh', 'nohup sh upgrade_java-8.sh >nohup.out &', 'cat nohup.out']
        ssh.connect(ip,22,username, password,timeout=5)
        for m in cmd:
            stdin, stdout, stderr = ssh.exec_command(m, get_pty=True)
#           stdin.write("Y")
            time.sleep(1)
            out = stdout.readlines()
            for o in out:
                #print o
                ret = re.search(r'java version "(1.\d).*"', o)
                if ret:
                    if str(ret.group(1)) == "1.8":
                           break
                with open("log_%s"%ip, 'a') as p_file:
                    p_file.write(o)
        print '%s\tOK\n'%(ip)
        ssh.close()
    except :
        print '%s\tError\n'%(ip)

 
# def mySsh(ip):
#     try:
#         username = 'test'
#         passwd = 'test'
#         cmd = "pwd"
#         ssh = paramiko.SSHClient()
#         ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#         ssh.connect(ip,22,username,passwd,timeout=5)
#         stdin, stdout, stderr = ssh.exec_command(cmd)
# #           stdin.write("Y")
#         time.sleep(1)
#         out = stdout.readlines()
#         for o in out:
#             print o,
#         print '%s\tOK\n'%(ip)
#         ssh.close()
#     except :
#         print '%s\tError\n'%(ip)


if __name__ == '__main__':
    _fill_testline_info(r"D:\i_source\trunk\TA\robot_repo\config")
    print TEST_LINE_IP_LIST
#     pool = threadpool.ThreadPool(len(TEST_LINE_IP_LIST))
#     requests = threadpool.makeRequests(mySsh, TEST_LINE_IP_LIST)  
#     [pool.putRequest(req) for req in requests]  
#     pool.wait()
    #output.close()

