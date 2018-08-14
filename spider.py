import socket
import socks
import requests
from bs4 import BeautifulSoup

def getSyncKey(tagUrl):
    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 1080)
    socket.socket = socks.socksocket
    request = requests.Session()
    page = request.get(tagUrl)
    page.encoding = "utf8"
    soup = BeautifulSoup(page.text, "html5lib")
    allTd = soup.find_all("td", class_ = "text-title")
    for td in allTd:
        try:
            key = td.a.get("href").split("/")[-1]
            name =td.a.text
            file = open("d:\\1.txt", "a")
            file.write(name.strip() + " : " + key.strip() + "\n")
            file.close()
        except:
            pass

if __name__=='__main__':
    url = "https://www.btsynckeys.com/"
    for i in range(0,131):#(1, 131)
        tagUrl = url + str(i*10)
        getSyncKey(tagUrl)
    print("end")