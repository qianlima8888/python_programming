#-*-coding:utf-8-*-
import requests, time, os, sys, io, random
from bs4 import BeautifulSoup

name = ['李博林','骆鑫','郭凯','李恩赐','周疆豪','袁鑫']
class jwxt:
    url1 = 'http://bbs.wust.edu.cn/vote/vote/member/index.php'
    url2 = 'http://bbs.wust.edu.cn/vote/vote/member/index.php?current=login'#登陆页面
    urlverifycode = 'http://bbs.wust.edu.cn/vote/vote/includes/rand_func.php'#获得验证码
    urllogon = 'http://bbs.wust.edu.cn/vote/vote/ajax.php'          #post提交用户名和密码等表单的网址
    vid = ''
    chongshi_num = 0#记录重试的次数 避免死循环
 
    def __init__(self, user, pwd):
        self.user = user
        self.pwd = pwd
        self.requests = requests.Session()    #自动管理cookie
        self.getvcode()

    def getvcode(self):#获得验证码
        r=self.requests.get(self.url1)
        r=self.requests.get(self.url2)
        r=self.requests.get(self.urlverifycode)
        with open('d:\\code.png','wb') as f:
            f.write(r.content)
        print('input login vcode:1234')
        #os.remove('d:\\code.png')
        self.postform()

    def postform(self):                      #提交用户名 密码 验证码等
        date = {
            'password'    : self.pwd,
            'user'    : self.user,
            'code'  : '1234',
            'login'           : '登录',
            }                          
        r=self.requests.post(self.url1,data = date)
        #print(r.text)
        x = r.text.find('window.location.href="../index.php"')
        if x:
            self.toupiao()

    def toupiao(self):#投票
        r = self.requests.get('http://bbs.wust.edu.cn/vote/vote/index.php')
        soup = BeautifulSoup(r.text, "html.parser")
        for tag in soup.find_all('div',class_='listbox'):
            if tag.find('font').string in name:
                self.vid+=('|'+tag.find('input').get('value'))
        #print(self.vid)
        r=self.requests.get(self.urlverifycode)
        with open('d:\\code.png','wb') as f:
            f.write(r.content)
        self.vcode = input('input vote vcode:')
        date = {
            'nt'    : 12996417320,
            'user'    : self.user,
            'vid'  :self.vid,
            'randcode'  : self.vcode,
            'time'           : int(time.time()),
            '_'           : '',
            }
        r=self.requests.post(self.urllogon,data = date)
        if r.text=='1':
            print('投票成功')
            print('------前十名票数为--------')
            r=requests.get('http://bbs.wust.edu.cn/vote/vote/top.php')
            soup = BeautifulSoup(r.text,'html5lib')
            div=soup.find('div',id='phangb')
            for div1 in div.find_all('a',limit=10):
                print(div1.find('font',style="color:#000000").get_text(),end='  ')
                print(div1.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element)
            div = soup.find_all('div',style="width:930px;float:left;height:30px;margin:5px 0;width:100%;")
            name[3]=div[random.randint(27,29)].find('font').string
            name[4]=div[random.randint(24,26)].find('font').string
            name[5]=div[random.randint(20,23)].find('font').string
        elif r.text=='6':
            print('验证码错误') 
            self.chongshi_num+=1
            if self.chongshi_num>6:
                print('已经输错验证码多次 即将登入下一个用户')
                return 10
            else:
                self.toupiao()
        elif r.text in ['0','2','8']:
            print('此用户已经投过，即将登入下一个用户')
        else:
            print('未知错误 即将登入下一用户')  
        
if __name__ == '__main__':
##    user = input('inptu user name:')
##    pwd = input('input password:')
    f = open('d:\\xuehao.txt')
    users = f.readlines()
    for user in users:
        user = user.strip('\n')
        pwd = user
        if user=='':
            continue
        print('\n\n此次投票给：',name)
        print('投票的用户为：',user,'   ')
        denglu = jwxt(user,pwd)
    print('所有用户已经已经登入 请重新增加用户')
    f.close()
