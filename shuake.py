import time
from DrissionPage import Chromium, ChromiumOptions

def watchAllVideo(userKey, userPassword, start, end):
    co = ChromiumOptions().auto_port()
    browser = Chromium(co)
    tabLogin = browser.latest_tab
    time.sleep(10)

    tabLogin.get("https://www.eszedu.com/")
    tabLogin.ele('@text()=登 录', timeout = 60).click()

    tabLogin.wait.title_change("登录")
    tabLogin.ele('@id=userKey', timeout = 60).clear().input(userKey)
    tabLogin.ele('@id=userPassword', timeout = 60).clear().input(userPassword)
    tabLogin.ele("@id=btnAccountLogin", timeout = 60).click()
    print("finish login")

    tabLogin.ele('@text()=教师心育培训', timeout = 60).click()

    browser.wait.new_tab()
    time.sleep(8)
    tabKeCheng = browser.get_tab(title="心理健康培训课程") #获得课程页面

    allClassName = tabKeCheng.ele('@class=bac_03_01-01 bac_03_01', timeout = 60).children() #获取有几门课程，一共10门课程
    for className in allClassName[start-1: end]:
        name = className.text.split('\n')[1]
        print("进入课程：{}".format(name))
        className.ele('@text()={}'.format(className.text.split('\n')[0]), timeout = 60).click() #进入选择的课程

        browser.wait.new_tab()
        time.sleep(8)
        tabClass = browser.get_tab(title="课程列表") #进入课程详细页面，可以看到课程有几个章节

        cheaperCount = len(tabClass.ele('@text()=课程目录：', timeout = 60).nexts()) #获取课程的章节数目
        for i in range(1, cheaperCount + 1):
            tabClass = browser.get_tab(title="课程列表")
            cheapter = tabClass.ele('@text()=课程目录：', timeout = 60).next(index = i)

            titles = cheapter.text.split("\n") #获取章节中小节的数目
            for j in range(1, len(titles)):
                title = titles[j]
                if("（已完成）" in title):
                    print("\t  已完成：{}".format(title))
                elif("（文档）" in title):
                    print("\t    跳过：{}".format(title))
                else:
                    print("\t开始学习：{}".format(title))

                    #获取课程章节的具体内容，点击进入要学习的章节
                    tabClass = browser.get_tab(title="课程列表") #进入课程详细页面
                    cheapter = tabClass.ele('@text()=课程目录：', timeout = 60).next(index = i)
                    subCheapter = cheapter.child(j + 1).child().click()
                    #点击要学习的章节后，tab页面的title会从课程列表变为
                    tabClass.wait.title_change("学习列表")
                    time.sleep(8)

                    #获取点击要学习的章节后进入具体的要看的视频页面
                    tabVideos = browser.get_tab(title="学习列表")
                    videos = tabVideos.eles('t:a', timeout = 60)
                    for video in videos:
                        #查找要学习的视频
                        if((".mp4" in video.text) or (".flv" in video.text) or (".MP4" in video.text)):
                            print("\t\t  开始观看视频：{}".format(video.text), end="。 ", flush=True)
                            video.click(by_js=True)#点击学习的视频
                            time.sleep(20)

                            #获取视频的时长
                            timeStart = tabVideos.ele('@class=current_time j-current_time', timeout = 60).text
                            timeEnd = tabVideos.ele('@class=duration j-duration', timeout = 60).text
                            print("视频时长:", timeEnd, end=",", flush=True)
                            print("已播放视频时长:", timeStart, end="。", flush=True)
                            sleepSecond = (int(timeEnd.split(":")[0]) - int(timeStart.split(":")[0])) * 60 + int(timeEnd.split(":")[1]) + 10
                            print("等待视频{}秒后播放结束... ".format(sleepSecond), end="", flush=True)
                            time.sleep(sleepSecond)
                            print("视频学习结束。")

                    tabVideos.back()
                    time.sleep(8)

        tabClass.close()
        time.sleep(8)


userKey = "xxxx"
userPassword = "xxxx"

#watchAllVideo(userKey, userPassword, 3, 4)
#watchAllVideo(userKey, userPassword, 5, 6)
#watchAllVideo(userKey, userPassword, 7, 7)
#watchAllVideo(userKey, userPassword, 9, 9)
watchAllVideo(userKey, userPassword, 10, 10)