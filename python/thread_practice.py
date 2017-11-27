#!/usr/bin/python
# -*- coding: UTF-8 -*-
import threading
import MySQLdb as mdb
import os,sys,math,time
import Queue
reload(sys)   
sys.setdefaultencoding('utf-8')
appdir=os.getcwd()
logdir=appdir+'/log'
if not os.path.exists(logdir):
    os.mkdir(logdir)


def writelog(filename,message):
    file=logdir+'/'+filename
    f=open(file,"a")
    f.write(message)
    f.close

def maxdata():
    try:
        conn=mdb.connect(host='localhost',user='root',passwd='',db='roomfamily',charset='utf8',port=3306)
        cur=conn.cursor()
        cur.execute("select max(userid) as maxid from roomfamily")
        data=cur.fetchone()
    finally:
        conn.close()
        return data[0]

maxiddata=maxdata()
minid=0
maxid=0
que=Queue.Queue()


def serial(id):
    global minid,maxid
    if minid < id:
       maxid=minid+9999
    if maxid > id:
       maxid=id
    return minid,maxid 

class runsql(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
            global minid,maxid,mutex
            threadname = threading.currentThread().getName()
            mutex.acquire()
            #对数据加锁
            if maxid >= maxiddata:
               time.sleep(0.1)
            (minid,maxid)=serial(maxiddata)
            que.put((minid,maxid))
            if maxid < maxiddata :
                minid=maxid+1
            mutex.release()
            conn=mdb.connect(host='localhost',user='root',passwd='',db='roomfamily',charset='utf8',port=3306)
            if not que.empty():
                (mid,aid)=que.get()
                #conn=mdb.connect(host='localhost',user='root',passwd='',db='roomfamily',charset='utf8',port=3306)
                cur=conn.cursor()
                cur.execute("select UserID,concat_ws('|',UserID,FamilyUserID,UserName,FamilyUserName,RelationTypeID,SecrecyType,CreateDate,UserType,UserCode,BatchNum,ClassID) as UserID2 from roomfamily where UserID between %d and %d"%(mid,aid))
                print threadname+" affect rows:%d:%s~%s"%(cur.rowcount,mid,aid)
                data=cur.fetchall();
                for num in data:
                   tablename="t_roomfamily_"+str(num[0]%200)
                   prefixname=str(num[0]%200)
                   writelog(tablename,num[1]+"\n")
                conn.close()
def main():
    global minid,maxid,mutex
    #### 定义循环序列，就是一个线程池     
    threads = []
    #### 定义运行所使用的线程数 
    thread_lines =10 
    start_line=0
    mutex = threading.Lock()
    for t in range(0,thread_lines):
        t=runsql()
        threads.append(t)
        start_line+=1
    for t in threads:
        t.start() 
    while True:
      for num_line in xrange(0,thread_lines): 
    #### 初始化当前线程的状态
         thread_status = False
    #### 初始化检查循环线程的开始值 
         loop_line = 0
    #### 开始循环检查线程池中的线程状态
         while thread_status == False :
    #### 如果检查当前线程，如果线程停止，代表任务完成，则分配给此线程新任务，
    #### 如果检查当先线程正在运行，则开始检查下一个线程，直到分配完新任务。 
    #### 如果线程池中线程全部在运行，则开始从头检查                
            if threads[loop_line].isAlive() == False:
                   threads[loop_line] = runsql() 
                   threads[loop_line].start() 
                   thread_status = True
            else:
                if loop_line >= thread_lines-1 :
                   loop_line=0
                else:
                   loop_line+=1
      if maxid >= maxiddata:
          break
    for number_line in xrange(start_line,thread_lines): 
        thread[number_line].exit() 

if __name__ == '__main__':
   main()

