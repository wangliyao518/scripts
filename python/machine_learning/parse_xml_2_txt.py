#!/usr/bin/python
#coding=utf-8
#Python Version Python 2.6.5
from xml.sax.handler import ContentHandler
from xml.sax import parse
import sys
import os

class HeadlineHandler(ContentHandler):

    in_headline=False

    def __init__ (self, file_name):
        ContentHandler.__init__(self)
        self.data=[]
        self.file_name = file_name.replace('.xml', '.txt')
        #self.file.writelines('id'+'\t'+'head\n')

    def startElement(self, name, attrs):
        pass
        # if name == 'list':
        #     self.data.append(attrs['id'])
        # if name == 'head':
        #     self.in_headline=True

    def endElement(self, name):
        pass
        # if name == 'list':
        #     self.file=open('info.txt','a')
        #     self.file.writelines(self.data[0]+'\t'+self.data[1]+'\n')
        #     self.file.close()
        #     self.data=[]
        # if name == 'head':
        #     self.in_headline=False

    def characters(self, string):
        #if self.in_headline:
        #    self.data.append(string)
        if string:
            self.file = open(self.file_name, 'a')
            self.file.writelines(string.strip() + "\n")
            self.file.close()


if __name__=='__main__':
    for fpathe, dirs, fs in os.walk(sys.argv[1]):
        for f in fs:
            if os.path.splitext(f)[-1] == '.txt':
                continue
            try:
                parse(os.path.join(fpathe, f), HeadlineHandler(os.path.join(fpathe, f)))
                #os.remove(os.path.join(fpathe, f))
            except Exception, e:
                try:
                    os.remove(os.path.join(fpathe, f))
                except:
                    print 'remove except'
                print '+++', e
