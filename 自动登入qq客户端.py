import pyautogui, win32gui, time, os
##while(True):
##    currentMouseX=pyautogui.position()
##    print(currentMouseX)
##    time.sleep(3)
os.startfile("D:\program file\qq\Bin\QQ.exe")
time.sleep(3)
dlg=win32gui.FindWindow(None,'QQ')#获得qq的句柄
if dlg:
    pyautogui.moveTo(786,496)#786,506
    pyautogui.click()
    pyautogui.click()
    pwd='***************'#qq密码
    time.sleep(2)
    pyautogui.typewrite(pwd,interval=0.3)
