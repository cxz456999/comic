from urllib.parse import urlencode
from html.parser import HTMLParser
from bs4 import BeautifulSoup

from HtmlFactory import HtmlFactory
import urllib.request
import urllib.parse
import http.cookiejar, threading
import random, sys, datetime, time, os
import time
from PyQt5 import QtCore, QtGui, QtWidgets

class CatchHtml():
    def __init__(self, obj):
        self.GUI = obj
        self.lastPage = 0
        self.htmlFactory = HtmlFactory()
        self.non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
        self.numOfCatch = 0
        self.numthd = 0
        self.thdList = []
        self.tLock = threading.Lock()
        date = datetime.datetime.now()
        filename = '%s_%s_%s.log' % (date.year, date.month, date.day)
        if os.path.exists(filename):
            os.remove(filename)
        self.logFile = open('%s_%s_%s.log' % (date.year, date.month, date.day),"a+",encoding='UTF-8')
    
    def catchContent(self, url):
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
        date = datetime.datetime.now()
        txtFile=open('%s_%s_%s_%s.csv' % (date.year, date.month, date.day, self.keyword),"a+",encoding='UTF-8')
        if self.numOfCatch == 0:
            print( '\uFEFF', file=txtFile, end='' )
            print( 'Date,Title,Author,Content,Comments', file=txtFile )
            print( '開始save to csv' )

        request = urllib.request.Request(url ,headers=headers)
        print('sss1')
        html = urllib.request.urlopen(request)
        print('sss2')
        txtHtml = html.read().decode('utf8', errors='ignore').translate(self.non_bmp_map)
        html.close()
        print('sss3')
        Date = self.htmlFactory.getDate(txtHtml) 
        if Date == '':
            html.close()
            return False
        result = self.htmlFactory.getDate(txtHtml) + ',' + self.htmlFactory.getTitle(txtHtml) + ',' + self.htmlFactory.getAuthor(txtHtml) + ',' + self.htmlFactory.getContent(txtHtml) + ',' + self.htmlFactory.getComment(txtHtml)
        print( 'result = content' )
        
        print( 'output result' )
        print( result, file=txtFile )
        #print( '------------------------------------------------------------------------------', file=txtFile )
        
        #html.close()

        
        self.tLock.acquire()
        self.numOfCatch = self.numOfCatch + 1
        self.tLock.release()
        return True
    def catchAllContents(self, urls):
        
        for url in urls:
            print(url)
            self.catchContent(url)
            #time.sleep (5)
            #thd = threading.Thread(target = self.catchContent, name='Catch%s' % self.numthd, args=(url,))
            #self.thdList.append( thd )
            #thd.start()
            #self.numthd = self.numthd + 1
            
    def catch(self, keyword, index, times = 0):
        try:
            strI = index/10 if index > 0 else 1
            self.GUI.showStatus.setText('正在抓取第%d頁' %  strI)
            print('正在抓取第%d頁' % strI )
            headers = {  
                #'Connection': 'Keep-Alive',  
                #'Accept-Language': 'zh-TW,zh;en-US;q=0.6,en;q=0.4',  
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
                #'Host' : 'tieba.baidu.com',
                #'Content-Type': 'text/html; charset=GBK',
                #'Upgrade-Insecure-Requests': '1',
   
            }
            

            url = 'https://www.google.com.tw/search?start=' + str(index) + '&q=' + urllib.parse.quote(keyword.encode('utf8')) + '+site%3Ahttps%3A%2F%2Ftieba.baidu.com%2F'
            ############# find last page
            

            #######################
            print('begin open' )
            print( url )

            request = urllib.request.Request(url, headers=headers)
            response = urllib.request.urlopen(request)
            print('end open' )        
            content = response.read().decode('GBK', errors='ignore').translate(self.non_bmp_map)
            response.close()
            #print(content)
            #print( '---->getUrls' )
            urls = self.htmlFactory.getUrls(content)
            #print( urls[0] )
            print( '---->end getUrls num: %d' % len(urls) )
            
           
            
            #print(content, file=open('111.html',"a+",encoding='GBK'))
            # 抓取內容
            #print( '---->catchContent' )
            if len(urls) <= 0  or times > 5:
                return False
            self.catchAllContents(urls)
            #print( '---->end catchContent' )
        except Exception as e:
            print('catch 發生Error: ' + str(e))
            print('catch 發生Error', file=self.logFile)
            self.GUI.textEdit.append('catch發生Error')
            print('重新開始至抓取' + str(index))
            self.catch(keyword, index, times=times+1)
            return True
        print('輸出成功至')
        return True
    def forCatching(self, keyword, beginI, endI ):
        stopIndex = endI
        sum_index = 1;
        i = self.lastPage = beginI
        while i <= endI:
            if not self.catch(keyword, i):
                stopIndex = i
                break;
            sum_index = sum_index + 1;
            if self.lastPage == -1:
               break 
            print('Catch success')
            i = i + 10
        # Wait for all threads to terminate.  
        for t in self.thdList:
            t.join()
            #print( 'after sleep %d' % len(self.thdList) )
            
        self.GUI.showStatus.setText('結束 第%d頁, 共抓%d筆資料' % (stopIndex, self.numOfCatch))
        self.numOfCatch = 0
        self.numthd = 0
        self.GUI.GoButton.setEnabled(True)
        self.logFile.close()
    def start(self, keyword, beginI, endI):
        self.keyword = keyword
        thd = threading.Thread(target = self.forCatching, name='Catching', args=(keyword,beginI-1,endI*10))
        thd.start()
        #self.catch(keyword, beginI)
