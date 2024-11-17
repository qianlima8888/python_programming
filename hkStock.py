import requests
import re
import csv

from texttable import Texttable

url = "https://17.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112406549656408281239_1730630411582&pn=1&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&dect=1&wbp2u=|0|0|0|web&fid=f3&fs=b:DLMK0146&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f19,f20,f21,f23,f24,f25,f26,f22,f33,f11,f62,f128,f136,f115,f152&_=1730630411586"
data = requests.get(url)

stockDatas = []

total = int(eval(re.findall(r'\((.*?)\)', data.text)[0])['data']['total'])
pz = 20
fields = "f2,f12,f14" #股价，股票代码，股票名称
loopCount = int(total / pz) + 1
for pn in range(1, loopCount + 1):
    url = "https://17.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112406549656408281239_1730630411582&pn={}&pz={}&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&dect=1&wbp2u=|0|0|0|web&fid=f3&fs=b:DLMK0146&fields={}&_=1730630411586".format(pn, pz, fields)
    data = requests.get(url).content.decode("utf-8")
    data = eval(data[data.find('(')+1:data.rfind(')')])['data']['diff']
    stockDatas += data

header = ["股票代码", "股票名称", "股价", "一手股票数", "一手股票价格"]
with open('hkStock.csv', 'w', newline='', encoding='gb2312') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    for stackData in stockDatas:
        price = stackData['f2']
        stockCode = stackData['f12']
        stockName = stackData['f14']
        url = "https://datacenter.eastmoney.com/securities/api/data/v1/get?reportName=RPT_HKF10_INFO_SECURITYINFO%3BRPT_HKF10_INFO_ORGPROFILE&columns=SECUCODE%2CSECURITY_CODE%2CSECURITY_NAME_ABBR%2CSECURITY_TYPE%2CLISTING_DATE%2CBOARD%2CTRADE_UNIT%2CTRADE_MARKET%2C%40SECUCODE%3B%40SECUCODE%2CORG_NAME%2CREG_PLACE%2CBELONG_INDUSTRY%2CFOUND_DATE%2CORG_WEB%2CCHAIRMAN&quoteColumns=&filter=(SECUCODE%3D%22{}.HK%22)&pageNumber=1&pageSize=200&sortTypes=&sortColumns=&source=F10&client=PC&v=027911191783349953".format(stockCode)
        data = requests.get(url)
        tradeUnit = data.json()['result']['data'][0]['TRADE_UNIT']
        data = [stockCode, stockName, price, tradeUnit, int(price*tradeUnit) if price != '-' else '-' ]
        writer.writerow(data)


