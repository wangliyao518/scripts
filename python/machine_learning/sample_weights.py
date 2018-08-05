# -*- coding:utf-8 -*-
import os


def weights(filePath):
    countList = []
    fileList =  os.listdir(filePath)  # 遍历train目录，显示所有类别标签
    numFileList = len(fileList)
    for i in range(numFileList):
        subFileList = os.listdir('%s\\%s' % (filePath, fileList[i]))
        numSubFileList = len(subFileList)
        if numSubFileList > 0:
            numSubFileList = 1/numSubFileList
        countList.append(numSubFileList) # 倒数的列表
        sumCount = sum(countList)
    for i in range(numFileList):
        countList[i] = countList[i]/sumCount
    return countList
