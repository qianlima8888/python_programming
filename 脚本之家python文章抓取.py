#-*-coding:utf-8-*-
import requests, sys
from bs4 import BeautifulSoup

def zhuaqu(htm,filename):
   head = {
      'Accept-Charset' : 'utf-8',
      'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
      }
   r=requests.get(htm,headers=head)
   r.encoding='gb2312'
   r.text.encode('gb2312','ignore')
   soup = BeautifulSoup(r.text, "html.parser")
   tag = soup.find('div',id="content")
   print(filename)
   try:
      with open(filename,'w') as f:
          for string in tag.strings:
             try:
                f.write(string)
             except:
                   continue
   except:
      print('抓取失败')
         
for num in range(1,130):
    url = 'http://www.jb51.net/list/list_97_'+str(num)+'.htm'
    r = requests.get(url)
    r.encoding='gb2312'
    soup = BeautifulSoup(r.text, "html.parser")
    for tag in soup.find('div',class_='artlist clearfix').find_all('dt'):
       htm = tag.a.get('href')
       title = tag.a.get('title')
       filename = 'd:\\1\\'+title+'.txt'
       html = 'http://www.jb51.net'+htm
       zhuaqu(html,filename)
