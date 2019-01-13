import requests
from bs4 import BeautifulSoup
import time

class weipu_spider:
    def __init__(self, keyword, url):
        self.keyword = keyword
        self.url = url

        self.headers = {
            'User-agent'       :    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'Connection'       :    'keep-alive',
            'Accept'           :    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding'  :    'gzip, deflate',
            'Accept-Language'  :    'zh-CN,zh;q=0.8,zh-TW;q=0.8,en-US;q=0.7,en;q=0.6',
            'Host'             :    'qikan.cqvip.com',
            'Referer'          :    'http://www.lib.wust.edu.cn/resource/Purchased.aspx?name=&loginsubmit.x=43&loginsubmit.y=13'
        }

        self.cookie = {
            "_qddaz"                                  :   "QD.1cutkn.sy97lq.jorxle2p",
            "Hm_lvt_69fff6aaf37627a0e2ac81d849c2d313" :   "1542850905,1542851299", 
            "__utma"                                  :   "164835757.325484457.1542851307.1542851307.1542851307.1",
            "__utmz"                                  :   "164835757.1542851307.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)",
            "user_behavior_flag"                      :   "3d53d8a4-33a9-474f-9cd0-f5eeb51008a2", 
            "skybug"                                  :   "075acf59953577e481a10d15d668f262", 
            "LIBUSERSETARTICLEPAGESIZECOOKIE"         :   "20",
            "ASP.NET_SessionId"                       :   "u54rckrewznd1ehh4kn1zhlp", 
            "td_cookie"                               :   "1923783448", 
            "search_isEnable"                         :   "1"
        }

        self.StartSearch()
    
    def StartSearch(self):#开始搜索
        postData = {
            "key"             :   "U%3D" + self.keyword,
            "isNoteHistory"   :   "1",
            "isLog"           :   "1",
            "indexKey"        :   self.keyword,
            "indexIdentifier" :   "U"
        }

        self.GetHtml("get", self.url, "0", self.headers)#获得维普网站首页

        searchUrl = self.url + "/Qikan/Search/Index?from=Qikan_Search_Index"
        self.headers.pop('Referer')
        htmlPage = self.GetHtml("post", searchUrl, postData, self.headers)#获得搜索页面

        articalDownloadInfo = self.GetSearchResult(htmlPage)
        self.DownloadPdf(articalDownloadInfo, [0])
    
    def GetHtml(self, httpMethod, targetUrl, postData, header):#获得页面
        request = requests.Session()

        if httpMethod == "get":
            page = request.get(targetUrl, headers = header, cookies = self.cookie)
        else:
            page = request.post(targetUrl, data = postData, headers = header, cookies = self.cookie)
        
        return page
    
    def GetSearchResult(self, htmlPage):#获得搜索结果 利用beautifulSoup解析页面 获得文献标题 和下载所需的相关参数
        htmlPage.encoding = "utf8"#为正常显示汉字 将编码改为utf8
        soup = BeautifulSoup(htmlPage.text,"html5lib")
        #print(htmlPage.text)

        #获得当前页面、页面总数和文章总数
        current_page = soup.find("span", class_="layui-laypage-curr")
        total_page = soup.find("a", class_="layui-laypage-last")
        total_artical = soup.find("div", class_="layui-col-xs6 search-result")
        print(total_artical.get_text())#输出查询到多少文献
        print(" 当前为第" + current_page.get_text() + "页")
        print("总页面数为" + total_page.get_text() + "页")

        dl = soup.find_all("dl", class_="")
        dl = dl[0:int(len(dl)/2)]                #dl中会有一半的重复元素 因此取前一半就ok

        num = 1
        articalDownloadInfo = []
        for detail in dl:
            title =  detail.find("dt").find("a", target="_blank")
            abstract =  detail.find("span", class_="abstract").find_all("span")[-1]
            article_source =  detail.find("div", class_="article-source").find("a", href="javascript:void(0);")
            try:
                print("----------------" + str(num) + "-----------------------", end='\n\n')
                print("  title: " + title.get_text())               #获取文献标题
                print("abstrcat:" + abstract.get_text())            #获得文章摘要
                articalDownloadInfo.append(article_source["onclick"][9:-1])              #获取下载相关参数 '\'' + title.get_text() + '\',' + 
                pass
            except:
                print("           获取文献信息出现错误！")
            print("")
            num = num + 1
        return articalDownloadInfo

    def DownloadPdf(self, articalDownloadInfo, downloadList):#下载文献
        ts = str(int(time.time()))

        #检查是否登入
        checkUrl = "http://qikan.cqvip.com/RegistLogin/CheckUserIslogin?0.4823511649473653"
        checkResult = self.GetHtml("get", checkUrl, 0, self.headers)#获得搜索页面
        if "true" not in checkResult.text:
            print("    不能下载文献！")
            return 0

        for i in downloadList:
            downLoadInfo = {
                "id"   : articalDownloadInfo[i].split(",")[0][1:-1],
                "info" : articalDownloadInfo[i].split(",")[1][1:-1],
                "ts"   : ts
            }

            self.cookie = {
                "td_cookie"                                  :   "1805494208",
                " _qddaz"                                    :   "QD.1cutkn.sy97lq.jorxle2p", 
                "Hm_lvt_69fff6aaf37627a0e2ac81d849c2d313"    :   "1542850905,1542851299", 
                " __utma"                                    :   "164835757.325484457.1542851307.1542851307.1542851307.1", 
                "__utmz"                                     :   "164835757.1542851307.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)", 
                "user_behavior_flag"                         :   "3d53d8a4-33a9-474f-9cd0-f5eeb51008a2", 
                "td_cookie"                                  :   "2060013100", 
                "skybug"                                     :   "ea4aa775b9af539f55ca5843428f034b", 
                "LIBUSERCOOKIE"                              :   "Oosn4ui+3LJraWhl2GKwZd4N3DziBMlIwDSCLIlUV7E8tnJct9u8Hs859iSbTYSjfHjVjeYZzQ7DlVXYGcnjs+Dueckl1EDOGkndfDb21I9WCnzLqgCoYuajUVp7Wi8NcCbQUyuSlqRo+AvSHa9oECsj8sCpe9+jLItbYfISvNZBxM7g4iCr7na0RJYSPWt6PpjBTviZhi8ai0Fv9Anc6QC9impeTiak1sTgG/464oMAAlLG5jQ8YfaiaYoADQ281T6r89c8JGY2Gd0rlqDbgSH86C3zgHSrFe+7cHKVlfSHncyaZ2OxxH9IXBWHI4xLqOMyhtVs4ZN7xQJJFhWL7V3e6toyD8efXeSNeJ2YBv/jL2VKGYSFxg==",
                "LIBUSERIDCOOKIE"                            :   "14346487", 
                "LIBUSERNAMECOOKIE"                          :   "武汉科技大学", 
                "ASP.NET_SessionId"                          :   "ogfl10digrqonbqd5sqiuvga",
                "search_isEnable"                            :   "1"
            }

            articleDownUrl = "http://qikan.cqvip.com/Qikan/Article/ArticleDown"
            htmlPage = self.GetHtml("post", articleDownUrl, downLoadInfo, self.headers)#获得真正下载链接
            #print(htmlPage.text)

            self.cookie = {
                "Hm_lvt_69fff6aaf37627a0e2ac81d849c2d313" :   "1542850905,1542851299", 
                "__utma"                                  :   "164835757.325484457.1542851307.1542851307.1542851307.1",
                "__utmz"                                  :   "164835757.1542851307.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)",
                "user_behavior_flag"                      :   "3d53d8a4-33a9-474f-9cd0-f5eeb51008a2", 
                "_qddaz"                                  :   "QD.1cutkn.sy97lq.jorxle2p",
                "td_cookie"                               :   "2083812556"
            }

            downloadUrl = htmlPage.text.split("\"")[3].replace("\\u0026", "&")
            headers = {
                "Accept"                              :     "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Encoding"                     :     "gzip, deflate",
                "Accept-Language"                     :     "zh-CN,zh;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.6",
                "Connection"                          :     "keep-alive",
                "DNT"                                 :     "1",
                "Host"                                :     downloadUrl.split("/")[2],
                "Upgrade-Insecure-Requests"           :     "1",
                "User-Agent"                          :     "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
            }
            pdfInfo = self.GetHtml("get", downloadUrl, 0, headers)
            if pdfInfo.status_code == 200:
                fileName = downloadUrl.split("&")[4].split("=")[1]
                with open("d:\\" + fileName, "wb") as f:
                    f.write(pdfInfo.content)
                print("成功下载" + fileName)

if __name__ == '__main__':
    #keyword = input("input search keyword:")
    url = "http://qikan.cqvip.com"
    weipu_spider("slam", url)