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
##    pyautogui.press('q')
##    pyautogui.keyDown('shift')
##    pyautogui.press('2')
##    pyautogui.press('d')
##    pyautogui.keyUp('shift')
##    pyautogui.press('n')
##    pyautogui.press('m')
##    pyautogui.press('1')
##    pyautogui.keyDown('shift')
##    pyautogui.press('1')
##    pyautogui.keyUp('shift')
##    pyautogui.press('7')
##    pyautogui.press('3')
##    pyautogui.press('2')
##    pyautogui.keyDown('shift')
##    pyautogui.press('7')
##    pyautogui.keyUp('shift')
##    pyautogui.press('1')
##    pyautogui.press('4')
##    pyautogui.press('1')
##    pyautogui.press('4')
##    pyautogui.moveTo(786,576)#786,506
##    pyautogui.click()    