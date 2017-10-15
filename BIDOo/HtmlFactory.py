from bs4 import BeautifulSoup
import re
import sys, uuid
import urllib.request, json
class HtmlFactory():
    def getUrls(self, html):
        urls = []
        sp = BeautifulSoup(html,'html.parser')
        content = sp.find_all('h3', {'class':'r'})
        for t in content:
            hrefs = t.find('a')
            href = hrefs.get('href')
            index = href.find('http://tieba.baidu.com/p/')
            if index > -1:
                urls.append(href)
        print('url')
        return urls
    def getContent(self, html):
        sp = BeautifulSoup(html,'html.parser')
        content = sp.find('div', {'class':'p_content'})
        print('content')
        return content.get_text().replace(',','，').replace('\n','').replace('\r','').replace(' ','')
    def getAuthor(self, html):
        sp = BeautifulSoup(html,'html.parser')
        content = sp.find('a', {'alog-group':'p_author'})
        #print(str(content))
        if content is None:
            return ''
        print('author')
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
        print('date')
        return match.group(0)
    def getTitle(self, html):
        sp = BeautifulSoup(html,'html.parser')
        content = sp.find('title')
        print('title')
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
        print('comment')
        return comments.replace(',','，').replace('\n','').replace('\r','')
'''hFt = HtmlFactory()
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
i = 0
while i <= 1000:
    request = urllib.request.Request("https://www.google.com.tw/search?q=" + '%E9%9B%B7%E6%B4%8B' + "+site%3Ahttps%3A%2F%2Ftieba.baidu.com%2F" + "&start=" + str(i) ,headers=headers)
    #start: 第幾筆
    html = urllib.request.urlopen(request)
    txtHtml = html.read().decode('utf8', errors='ignore').translate(non_bmp_map)
    sp = BeautifulSoup(txtHtml,'html.parser')
    txtHtml = sp.find_all('h3', {'class':'r'})
    for t in txtHtml:
        hrefs = t.find('a')
        href = hrefs.get('href')
        index = href.find('http://tieba.baidu.com/p/')
        if index > -1:
            print(t.get_text() + '\t' + href, file=open("1111111.txt","a+",encoding='UTF-8'))
    #hFt.downloadImg(txtHtml)
    html.close()'''
    
'''hFt = HtmlFactory()
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
i = 0

request = urllib.request.Request('http://tieba.baidu.com/p/4538080535' ,headers=headers)
#start: 第幾筆
html = urllib.request.urlopen(request)
txtHtml = html.read().decode('utf8', errors='ignore').translate(non_bmp_map)
html.close()
print(txtHtml)'''