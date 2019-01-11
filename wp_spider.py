import requests
from bs4 import BeautifulSoup

class weipu_spider:
    def __init__(self, keyword, url):
        self.keyword = keyword
        self.url = url
        self.StartSearch(self.keyword, self.url)
    
    def StartSearch(self, keyword, url):
        postData = {
            "key" : "U%3D" + keyword,
            "isNoteHistory" : "1",
            "isLog" : "1",
            "indexKey" : keyword,
            "indexIdentifier" : "U"
        }

        self.GetHtml("get", self.url, "0", False)

        searchUrl = self.url + "/Qikan/Search/Index?from=index"
        self.GetHtml("post", searchUrl, postData, False)
    
    def GetHtml(self,httpMethod, targetUrl, postData, isPdf):
        request = requests.Session()
        if httpMethod == "get":
            page = request.get(targetUrl)
        else:
            page = request.post(targetUrl, data = postData)

        if isPdf: 
            return page.content
        else:
            page.encoding = "utf8"
            print(page.text)
            return page.text

    def DownloadPdf(self):
        pass


if __name__ == '__main__':
    #keyword = input("input search keyword:")
    url = "http://qikan.cqvip.com"
    weipu_spider("slam", url)