#!/usr/bin/python
#coding=utf-8
from xml.sax.handler import ContentHandler
from xml.sax import parse
import sys
import os


def clean_empty_folder(path):
    files = os.listdir(path)
    for file in files:
        print 'Traversal at', file
        if os.path.isdir(os.path.join(path, file)):
            if not os.listdir(os.path.join(path, file)):
                os.rmdir(os.path.join(path, file))
            else:
                clean_empty_folder(os.path.join(path, file))
        elif os.path.isfile(os.path.join(path, file)):
            if os.path.getsize(os.path.join(path, file)) == 0:
                os.remove(os.path.join(path, file))
    print path, 'Dispose over!'


if __name__=='__main__':
    clean_empty_folder(sys.argv[1])
    # for fpathe, dirs, fs in os.walk(sys.argv[1]):
    #     for f in fs:
    #         print os.path.join(fpathe, f)
