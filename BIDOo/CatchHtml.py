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
        self.cookie_FirstValue = 'ABTEST=0|1492871394|v1; IPLOC=CN7100; JSESSIONID=aaaBU-sq2ZsyrcalwCFSv; SUV=00525A9F3B7C9F1E58FB68E2CD3EB633; weixinIndexVisited=1; ppinf=5|1492872274|1494081874|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZTo2OlRNV1BJV3xjcnQ6MTA6MTQ5Mjg3MjI3NHxyZWZuaWNrOjY6VE1XUElXfHVzZXJpZDo0NDpvOXQybHVCa2w3SWVKOFZhanhKdWVqektyR0kwQHdlaXhpbi5zb2h1LmNvbXw; pprdig=XJB5g4grX3GifTVzf4XQkG9cSesbr_hUvsTsntFI48oHQ_4T8MGIAjSCR5Q8ujYxcth3l64ZmvPIUsZcC4KejAM-2eZHDqjzUp5HvrAlqjQwRi43DlNCGV9opjrJlLj5bAP5Dx1Z46lw93EMf7z5UQOE-72DT8iypADSyTY0_8I; sgid=; sct=1'
        
        self.cookie_Storage = []
        #self.updateCookie()
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
    def makeOpener(self, head = {  
        'Connection': 'Keep-Alive',  
        'Accept-Language': 'zh-TW,zh;en-US;q=0.6,en;q=0.4',  
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36',
        'Host' : 'weixin.sogou.com',
        'Content-Type': 'charset=utf-8',
        'Upgrade-Insecure-Requests': '1'
        }):
        
        self.cookie = http.cookiejar.CookieJar()
        ##cookie_filename = 'cookie_jar.txt'
        ##self.cookie = http.cookiejar.MozillaCookieJar(cookie_filename)
        ##self.cookie.load(cookie_filename, ignore_discard=True, ignore_expires=True)
        
        pro = urllib.request.HTTPCookieProcessor(self.cookie)
        proxies = urllib.request.ProxyHandler({'http': '184.168.131.233:80'})
        opener = urllib.request.build_opener(pro)#, proxies)  
        header = []  
        for key, value in head.items():  
            elem = (key, value)  
            header.append(elem)  
        opener.addheaders = header  
        return opener
    
    def updateCookie(self):
        try:
            url = 'http://tieba.baidu.com/f/search/res?only_thread=1&pn=%d&qw=' % random.choice('abcdefghijklmnopqrstuvwxyz')
            oper = self.makeOpener()
            response = oper.open(url)
            #print( self.cookie )
            tmpCookie = ''
            for item in self.cookie:
                if item.name.find( 'SNUID' ) != -1:
                    tmpCookie = tmpCookie + 'SNUID=%s; '  % item.value
                    print( 'SNUID=' + item.value )
                if item.name.find( 'SUID' ) != -1:
                    tmpCookie = tmpCookie + 'SUID=%s; '  % item.value
                    print( 'SUID=' + item.value )
            response.close()
            print( 'tmpCookie=' + tmpCookie )
            #self.cookie_Value = self.cookie_FirstValue + tmpCookie
            #self.cookie_Storage.append(self.cookie_FirstValue + tmpCookie)
            if 'SNUID' not in tmpCookie:
                print('Error: SNUID not found')
                print('Error: SNUID not found', file=self.logFile)
                self.GUI.textEdit.append('Error: SNUID not found')
                return False
            self.cookie_Storage.append( tmpCookie)
        except:
            print('Error: Update Cookie')
            print('Error: Update Cookie', file=self.logFile)
            self.GUI.textEdit.append('Error: Update Cookie')
            return False
        return True
    
    def getCookie(self):
        self.GUI.showStatus.setText('取得cookie中' )
        print('取得cookie中' )
        if len(self.cookie_Storage) <= 1:
            while len(self.cookie_Storage) < 5:
                if self.updateCookie() == False:
                    break
                time.sleep(5)
        if len(self.cookie_Storage) <= 0:
            self.GUI.textEdit.append('Error: Cookie 使用完畢' )
            print('Error: Cookie 使用完畢' )
            print('Error: Cookie 使用完畢', file=self.logFile)
            return False
        
        self.cookie_Value = self.cookie_FirstValue + self.cookie_Storage[0]
        del self.cookie_Storage[0]
        print('change cookie success')
        self.GUI.textEdit.append('Cookie change to %s\n\n' % self.cookie_Value )
        return True
    def catchContent(self, url):
        print (url)
        date = datetime.datetime.now()
        
        txtFile=open('%s_%s_%s_%s.csv' % (date.year, date.month, date.day, self.keyword),"a+",encoding='UTF-8')
        html = urllib.request.urlopen(url)
        txtHtml = html.read().decode('utf8', errors='ignore').translate(self.non_bmp_map)
        if self.numOfCatch == 0:
            print( '\uFEFF', file=txtFile, end='' )
            print( 'Date,Title,Author,Content,Comments', file=txtFile )
            print( '開始save to csv' )
        Date = self.htmlFactory.getDate(txtHtml) 
        if Date == '':
            html.close()
            return False
        result = self.htmlFactory.getDate(txtHtml) + ',' + self.htmlFactory.getTitle(txtHtml) + ',' + self.htmlFactory.getAuthor(txtHtml) + ',' + self.htmlFactory.getContent(txtHtml) + ',' + self.htmlFactory.getComment(txtHtml)
        print( 'result = content' )
        if self.GUI.downloadImg.isChecked():
            self.htmlFactory.downloadImg(txtHtml)
        html.close()
        #html = urllib.request.urlopen(url.replace('http://mp.weixin.qq.com/s', 'http://mp.weixin.qq.com/mp/getcomment'))
        #txtHtml = html.read().decode('utf8', errors='ignore').translate(self.non_bmp_map)
        #print( 'result + comment' )
        #result = result + self.htmlFactory.getComment(txtHtml)
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
            self.catchContent('https://tieba.baidu.com' + url)
            #time.sleep (5)
            #thd = threading.Thread(target = self.catchContent, name='Catch%s' % self.numthd, args=(url,))
            #self.thdList.append( thd )
            #thd.start()
            #self.numthd = self.numthd + 1
            
    def catch(self, keyword, index, times = 0):
        try:
            self.GUI.showStatus.setText('正在抓取第%d頁' % index )
            print('正在抓取第%d頁' % index )
           
            #if index % 5 == 0 and index % 10 != 0:
            #    self.updateCookie()  
            #elif index % 15 == 0:
            #    if not self.getCookie():
            #        return False
            #print('-----------------> ' + self.cookie_Value )
            headers = {  
                'Connection': 'Keep-Alive',  
                'Accept-Language': 'zh-TW,zh;en-US;q=0.6,en;q=0.4',  
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36',
                'Host' : 'tieba.baidu.com',
                'Content-Type': 'text/html; charset=GBK',
                'Upgrade-Insecure-Requests': '1',
   
            }
            
            url = 'http://tieba.baidu.com/f/search/res?only_thread=1&pn=%d&qw='%index
            ############# find last page
            

            #######################
            print('begin open' )
            url = url +  urllib.parse.quote(keyword.encode('gbk'))
            print( url )

            request = urllib.request.Request(url, headers=headers)
            response = urllib.request.urlopen(request)
            print('end open' )        
            content = response.read().decode('GBK', errors='ignore').translate(self.non_bmp_map)
            #print(content)
            #print( '---->getUrls' )
            urls = self.htmlFactory.getUrls(content)
            if index == self.lastPage:
                self.lastPage = self.htmlFactory.getLastPage(content)
            #print( urls[0] )
            print( '---->end getUrls num: %d' % len(urls) )
            
            response.close()
            
            #print(content, file=open('111.html',"a+",encoding='GBK'))
            # 抓取內容
            #print( '---->catchContent' )
            if ( len(urls) <= 0 ):
                return True
            self.catchAllContents(urls)
            #print( '---->end catchContent' )
        except Exception as e:
            print('catch 發生Error: ' + str(e))
            print('catch 發生Error', file=self.logFile)
            self.GUI.textEdit.append('catch發生Error')
            return False
        print('輸出成功至')
        return True
    def forCatching(self, keyword, beginI, endI ):
        stopIndex = endI
        sum_index = 1;
        self.lastPage = beginI
        for i in range( beginI, endI+1 ):
            if i > beginI and i > self.lastPage:
                break;
            if not self.catch(keyword, i):
                stopIndex = i
                break;
            sum_index = sum_index + 1;
            if self.lastPage == -1:
               break 
            print('99999')
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
        thd = threading.Thread(target = self.forCatching, name='Catching', args=(keyword,beginI,endI))
        thd.start()
        #self.catch(keyword, beginI)
