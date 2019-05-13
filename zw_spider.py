import requests
from bs4 import BeautifulSoup
import time

class zw_spider:
    def __init__(self, keyword, url):
        self.keyword = keyword
        self.url = url
        self.headers = {}
        self.cookies = {}

    def GetHtml(self, httpMethod, htmlUrl, postData, headers, cookies):
        pass
    
    def GetSearchResult(self, htmlPage):
        pass

    def DownloadPdf(self, articalDownloadInfo, downloadList):
        pass