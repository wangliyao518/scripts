# -*- coding: utf-8 -*-
# 重启路由器脚本
#
import urllib2, base64,cookielib
#


# -*- coding: utf-8 -*-   
from PyQt4.QtGui import *  
from PyQt4.QtCore import *  
import sys 
#   

  
QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))  

class EmittingStream(QObject):
 
    textWritten = pyqtSignal(str)
 
    def write(self, text):
        self.textWritten.emit(str(text))
 
  
class StandardDialog(QDialog):  
  
    def __init__(self,parent=None, app=None):  
        super(StandardDialog,self).__init__(parent)  
        
        self.setWindowTitle(self.tr("重启路由器"))  
         
        self.stdout_back = sys.stdout 
        sys.stdout = EmittingStream(textWritten=self.normalOutputWritten) 
        
        Labe0_ip=QLabel(self.tr("路由器ip："))
        Label_username=QLabel(self.tr("用户名："))
        Labe2_password=QLabel(self.tr("密码："))  
        self.usernameLineEdit=QLineEdit("admin")  
        self.passwordLineEdit=QLineEdit("ml503025998")
        self.ipLineEdit=QLineEdit("192.168.1.1")
        self.consloeTxt=QTextEdit()
        self.consloeTxt.resize(2,1)  
        restartButton=QPushButton(self.tr("重启路由器"))  
        quiteButton=QPushButton(self.tr("退出"))
        Labe3_output=QLabel(self.tr("终端输出窗口："))
        detailinfoButton=QPushButton(self.tr("显示输出窗口"))
  
        self.detailWidget=QWidget()
        detailLayout=QGridLayout(self.detailWidget)
        self.consloeTxt=QTextEdit()
        #detailLayout.addWidget(quiteButton,0,0)
        detailLayout.addWidget(Labe3_output,0,0)
        detailLayout.addWidget(self.consloeTxt,1,0)
        self.detailWidget.hide()    
        
        layout=QGridLayout()
        layout.addWidget(Labe0_ip,0,0)
        layout.addWidget(self.ipLineEdit,0,1)
        layout.addWidget(Label_username,1,0) 
        layout.addWidget(self.usernameLineEdit,1,1)
        layout.addWidget(Labe2_password,2,0)  
        layout.addWidget(self.passwordLineEdit,2,1) 
        layout.addWidget(restartButton,3,0)
        layout.addWidget(detailinfoButton,3,1)
        #layout.addWidget(quiteButton,4,0)
        #layout.addWidget(self.consloeTxt,3,1,4,1)
        #self.setLayout(layout)
        
        mainLayout=QVBoxLayout()
        mainLayout.addLayout(layout)
        mainLayout.addWidget(self.detailWidget)
        #mainLayout.setSizeConstraint(QLayout.SetFixedSize)
        #mainLayout.setSpacing(10)

        self.setLayout(mainLayout)
        
        self.connect(restartButton,SIGNAL("clicked()"),self.restart_router)  
        self.connect(quiteButton,SIGNAL("clicked()"),app,SLOT("quit()"))
        self.connect(detailinfoButton,SIGNAL("clicked()"),self.slotExtension)

    def __del__(self):
        # Restore sys.stdout
        sys.stdout = self.stdout_back
        
    def slotExtension(self):
        if self.detailWidget.isHidden():
            self.detailWidget.show()
        else:
            self.detailWidget.hide()
    
    def normalOutputWritten(self, text):
        """Append text to the QTextEdit."""
        # Maybe QTextEdit.append() works as well, but this is how I do it:
        cursor = self.consloeTxt.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(str(text))
        self.consloeTxt.setTextCursor(cursor)
        self.consloeTxt.ensureCursorVisible()

    def restart_router(self):
        # IP for the router
        
        ip = unicode(self.ipLineEdit.text())
        # 登录的用户名和密码
        login_user = unicode(self.usernameLineEdit.text()) #'admin'
        login_pw = unicode(self.passwordLineEdit.text()) #'ml503025998'
     
        # 请求地址
        url = 'http://' + ip + '/userRpm/SysRebootRpm.htm?Reboot=%D6%D8%C6%F4%C2%B7%D3%C9%C6%F7'
        auth = 'Basic ' + base64.b64encode(login_user+':'+login_pw)
        print auth  #Authorization=Basic%20YWRtaW46bWw1MDMwMjU5OTg%3D
        #opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
        #urllib2.install_opener(opener)
        #opener.addheaders = [('Host', "192.168.1.1"),
    #                          ('User-agent',"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0"),
    #                          ('Accpet',"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"),
    #                          ("Accept-Language", "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3"),
    #                          ('Accept-Encoding','gzip, deflate'),
    #                          ('Referer',"http://192.168.1.1/userRpm/SysRebootRpm.htm?Reboot=%D6%D8%C6%F4%C2%B7%D3%C9%C6%F7"),
    #                          ('Cookie',auth),
    #                          ('Connection',"keep-alive"),
    #                          ] 
        #{ 'Referer' : 'http://' + ip + '/userRpm/SysRebootRpm.htm',
        #         'Authorization' : auth
        #}
        heads = { 'Host':ip, 
                 'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
                 'Accpet': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                 "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
                 "Accept-Encoding": "gzip, deflate",
                 'Referer' : "http://{}/userRpm/SysRebootRpm.htm?Reboot=%D6%D8%C6%F4%C2%B7%D3%C9%C6%F7".format(ip),
                 'Cookie' : "Authorization="+auth,
                 'Connection':"keep-alive"
        }     
         
        # 发送请求
        print url
        print heads
        try:
            request = urllib2.Request(url,None, heads)
            response = urllib2.urlopen(request)
            response.read()
        except Exception, e:
            print e
            QMessageBox.critical(self,self.tr("告警窗口"),self.tr(unicode(e)))
        else:
            QMessageBox.about(self,self.tr("成功提示窗口"),self.tr("重启路由器成功！")) 

 
if __name__ == '__main__':
    
    app=QApplication(sys.argv)  
    form=StandardDialog(None,app)  
    form.show()  
    app.exec_()  
    


# login_user = 'admin'
# login_pw = 'ml503025998'
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


# import urllib
# print urllib.urlopen("http://admin:ml503025998@192.168.1.1/userRpm/MenuRpm.htm?MainID=0&SubID=0").read()

