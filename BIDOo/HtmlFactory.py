from bs4 import BeautifulSoup
import re
from datetime import datetime
import sys, uuid
import urllib.request, json
class HtmlFactory():
    def getUrls(self, html):
        urls = []
        sp = BeautifulSoup(html,'html.parser')
        contents = sp.find_all('span', {'class':'p_title'})
        
        for content in contents:
            all_links = content.find_all('a', {'target':'_blank'})
            for link in all_links:
                href = link.get('href')
                #linkClass = link.get('class')
                if href != None and href not in urls:
                    urls.append(href)
                    #print(href)
        return urls
    def getContent(self, html):
        sp = BeautifulSoup(html,'html.parser')
        content = sp.find('div', {'class':'p_content'})
        return content.get_text().replace(',','，').replace('\n','').replace('\r','').replace(' ','')
    def getAuthor(self, html):
        sp = BeautifulSoup(html,'html.parser')
        content = sp.find('a', {'alog-group':'p_author'})
        print(str(content))
        if content is None:
            return ''
        return content.get_text().replace(',','，').replace('\n','').replace('\r','')
    def getDate(self, html):
        #print(html)
        sp = BeautifulSoup(html,'html.parser')
        #print(html[html.find('1楼'):])
        content = sp.find('div', {'id':'j_p_postlist'})
        #print( content.get_text() )
        match = re.search('\d{4}-\d{2}-\d{2}', str(content))
        if match is None:
            return ''
        return match.group(0)
    def getTitle(self, html):
        sp = BeautifulSoup(html,'html.parser')
        content = sp.find('title')
        return content.get_text().replace(',','，').replace('\n','').replace('\r','')
    def getComment(self, html):
        
        sp = BeautifulSoup(html,'html.parser')
        contents = sp.findAll('div', {'class':'p_content'})
        authors = sp.findAll('a', {'class':'p_author_name'})
        comments = ''
        if ( len(contents) <= 0 ):
            return''
            
        for i in range(1,len(contents)):
            if i >= len(authors):
                nickname = ''
            else:
                nickname = authors[i].get_text().replace(',','，').replace('\n','').replace('\r','')
            content = contents[i].get_text().replace(',','，').replace('\n','').replace('\r','').replace(' ','')
            #print( nickname + content )
            #print('\n')
            comments = comments + '[%s:%s]' % (nickname, content )
        
        return comments.replace(',','，').replace('\n','').replace('\r','')
    def downloadImg(self, html):
        sp = BeautifulSoup(html,'html.parser')
        content = sp.find('div', {'class':'rich_media_content'})
        imgs = content.find_all('img')
        if len(imgs) <= 0:
            return
        for img in imgs:
            href = img.get('data-src')
            imgFormat = img.get('data-type')
            if href == None or imgFormat == None:
                continue
            if imgFormat == 'jpeg':
                imgFormat = 'jpg'
            print( imgFormat )
           
            try:
                urllib.request.urlretrieve(href, './Images/' + str(uuid.uuid4()) + '.%s' % imgFormat)
            except:
                print ('download img error' )
       

    def getLastPage(self,html):
        
        sp = BeautifulSoup(html,'html.parser')
        content = sp.find('a', {'class':'last'})
        if content is None:
            return -1
        href = content.get('href')
        print( 'Last Page is ' + href[href.find('&pn')+4:] )
        return int(href[href.find('&pn')+4:])
#hFt = HtmlFactory()
#non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
#html = urllib.request.urlopen('http://tieba.baidu.com/f/search/res?only_thread=1&pn=76&qw=%C0%D7%D1%F3')

#txtHtml = html.read().decode('utf8', errors='ignore').translate(non_bmp_map)
#print(hFt.getLastPage(txtHtml))
#print(hFt.getContent(txtHtml))
#print(hFt.getAuthor(txtHtml))
#print(hFt.getDate(txtHtml))
#print(hFt.getTitle(txtHtml))
#print(hFt.getComment(txtHtml))
#hFt.downloadImg(txtHtml)
#html.close()
