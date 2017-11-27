# -*- coding: utf-8 -*-

__author__ = 'kiterunner_t'


import os


class InvalidMessageException(Exception):
    pass


# 二进制消息迭代器的策略
# 每次返回一整条完整的二进制消息内容
# 每次根据配置参数，先从文件中读取 maxSize 的二进制消息内容到内存，然后每次返回一条完整的消息
# 当消息文件很大，迭代完当前内存的消息之后，会再次从文件中读取消息到内存，然后再返回一条消息
class MessageFileIter():
    def __init__(self, fileName, maxSize):
        assert maxSize >= 4, "maxSize should be greater than 4"

        self.fileName = fileName
        self.maxSize = maxSize

        self.file = None
        self.filePosition = 0
        self.fileSize = 0
        self.isRead = False

        self.fileHeader = ""
        self.fileHeaderSize = 7
        
        self.lastBin = "" # 避免对上次的bin和当前从文件读取的内容进行字符串连接
        self.bin = ""
        self.binSize = 0
        self.binIndex = 0

        self.recordIndex = 0
        self.readCount = 0


    def __iter__(self):
        return self


    def next(self):
        if self._fileContentIsEmpty():
            raise StopIteration

        if self.recordIndex == 0:
            self.fileHeader = self._getBuf(self.fileHeaderSize)
            print self.fileHeader

        try:
            recordLen = int(self._getBuf(4))
        except:
            raise InvalidMessageException

        assert recordLen <= 10 * 1024 * 1024, "one message should be less than 10M"

        record = self._getBuf(recordLen)
        if len(record) != recordLen:
            raise InvalidMessageException
            
        self.recordIndex += 1
        return self.recordIndex, record

        
    def _fileContentIsEmpty(self):
        return self.binIndex >= self.binSize and self.isRead is True
        
        
    def _getBuf(self, size):
        if self.binIndex + size <= self.binSize:
            retStr = self.bin[self.binIndex:self.binIndex+size]
            self.binIndex += size
            return retStr
 
        self._readFile(size)
        
        needReadSize = size
        retStr = ""
        lastBinLen = len(self.lastBin)
        if lastBinLen != 0:
            assert lastBinLen < size, "lastBinLen should be size in this case"
            needReadSize -= lastBinLen
            retStr = self.lastBin
            self.lastBin = ""
            
        self.binIndex += needReadSize
        return retStr + self.bin[:needReadSize]
        

    def _readFile(self, atLeastSize):
        if self.isRead is True:
            return

        if self.file is None:
            self.fileSize = os.path.getsize(self.fileName)
            self.file = open(self.fileName, "rb")

        if self.binIndex < self.binSize:
            self.lastBin = self.bin[self.binIndex:]

        tmpList = []
        readSize = 0
        while readSize < atLeastSize:
            self.readCount += 1
            tmpStr = self.file.read(self.maxSize)
            tmpStrLen = len(tmpStr)

            readSize += tmpStrLen
            tmpList.append(tmpStr)
            
            self.filePosition += tmpStrLen
            if self.file.tell() == self.fileSize:
                self._closeFile()
                break

        self.bin = "".join(tmpList)
        self.binSize = len(self.bin)
        self.binIndex = 0


    def _closeFile(self):
        if self.file is None:
            return

        self.isRead = True
        self.file.close()
        self.file = None
        self.filePosition = 0
        self.fileSize = 0


if __name__ == "__main__":
    #fileName = '..\\test\\test.txt'
    
    maxSize = 50 * 1024 * 1024
    #fileName = '..\\test\\test100_0000.txt'
    fileName = '..\\test\\test1000_0000.txt'

    import time

    wfile = open(fileName + "-wfile.txt", "wb")

    startTime = time.time()
    mFile = MessageFileIter(fileName, maxSize)
    i = 0
    for (index, text) in iter(mFile):
        wfile.write(str(index) + ": " + text + "\n")
        i += 1
    wfile.close()

    endTime = time.time()
    print "records: ", i
    print startTime, endTime, endTime - startTime

