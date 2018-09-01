'''
本爬虫思路：
    1、首先爬取页面获得标题、url、时间等信息
    2、然后将每一条博客按照发布时间的先后顺序排序，记录爬取的最新时间
    3、以后每次爬虫则与上次爬虫的最新时间比较，时间大则为新发布的内容

比较时间的思路为：
    1、时间格式为:yyyy-mm-dd hh-mm。如2018-05-31 09-01
    2、去掉时间横杠和空格，讲字符串转换为int
    3、比较转换后两数字的大小
'''
import requests
from bs4 import BeautifulSoup

#比较时间
def isBigTime(oldTimrString, newTimeString):
    pass

#按照时间先后顺序排列
def sortList(bligList):
    pass

#获得每篇文章详细信息，返回一个列表
def getDetail(blogDetail):
    blogUrl = blogDetail.find_all(class_ = "post_item_body")
    for url in blogUrl:
        print(url.h3.get_text())
        print(url.h3.a.get("href"))
        print(url.find("p", class_  =  "post_item_summary").get_text())
        auth = url.find(class_ = "post_item_foot").a.string
        print(auth)

#获得页面
def getHtml(url):
    request = requests.Session()
    blogPage = request.get(url)
    blogPage.encoding = "utf-8"
    getDetail(BeautifulSoup(blogPage.text, "html5lib"))

url = "https://www.cnblogs.com/cate/cpp/"
getHtml(url)
