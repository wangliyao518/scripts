#-*- coding:utf-8 -*-
import optparse
import re
import threading
import sys
import socket

def anlyze_host(target_host):
#from--host arguments get the host value and translate to xx.xxx.xxx.xxx format，其中主要是利用socket的gethostbyname函数将域名形式的值转换为四位点进制形式
    try:
        pattern = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}') #匹配标准点进制的IP
        match = pattern.match(target_host)
        if match:
            return(match.group())
        else:
            try:
                target_host = socket.gethostbyname(target_host) #如果不是，就把target_host的值作为域名进行解析
                return(target_host)
            except Exception as err:
                print('parser address error：',err)
                exit(0)
    except Exception as err:
        print('notes error 1：',sys.exc_info()[0],err)
        print(parser.usage)
        exit(0)
                    

def anlyze_port(target_port):
#解析--port参数传入的值，返回端口列表
    try:
        pattern = re.compile(r'(\d+)-(\d+)')    #解析连接符-模式
        match = pattern.match(target_port)
        if match:
            start_port = int(match.group(1))
            end_port = int(match.group(2))
            return([x for x in range(start_port,end_port + 1)])
        else:
            return([int(x) for x in target_port.split(',')])
    except Exception as err:
        print('notes error 2:',sys.exc_info()[0],err)
        print(parser.usage)
        exit(0)

def scanner(target_host,target_port):
#创建一个socket对象
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.settimeout(5)
    try:
        s.connect((target_host,target_port))
        #s.sendall(b'hello\r\n\r\n')
        #message = s.recv(100)
        #if message:
        print('[+]%s %3s port: open' % (target_host,target_port)) #若可以建立连接，表示此端口是打开的
           # print(' %s' % message.decode('utf-8'))
    except socket.timeout:
        pass
        #print('[-]%s %3s port: close' % (target_host,target_port)) #如果连接超时，表示此端口关闭
    except Exception as err:
        pass
        #print('notes error 3:',sys.exc_info()[0],err)
        exit(0)


        
def main():
   usage = 'Usage:%prog -h <host> -p <port>'
   parser = optparse.OptionParser(usage,version='%prog v1.0')
   parser.add_option('--host',dest='target_host',type='string',
                     help='the host of scan, domain or IP')
   parser.add_option('--port',dest='target_port',type='string',
                    help='the port of the host，suport 1-100 or 21,53,80 format')
   (options,args) = parser.parse_args()
   if options.target_host == None or options.target_port == None:
      print(parser.usage)
      exit(0)
   else:
      target_host = options.target_host
      target_port = options.target_port

   target_host = anlyze_host(target_host)
   target_port = anlyze_port(target_port)

   for port in target_port:
      t = threading.Thread(target=scanner,args=(target_host,port)) #scan the port
      t.start()

if __name__ == '__main__':
    main()
