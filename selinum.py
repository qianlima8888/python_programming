from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait  #设置等待时间
from selenium.webdriver.support import expected_conditions as EC #设置等待条件
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select #处理下拉框
from selenium.webdriver import ActionChains #鼠标操作

import random
import time

select_options = ['优秀', '良好']
text_options = ['严谨认真','工作负责', '负责认真', '教学严谨 工作认真负责']

driver= webdriver.Chrome()
#driver.maximize_window()
 
#driver.implicitly_wait(60)#等待30秒
 
driver.get("评教网站")

#code = input("input yzm: ")

WebDriverWait(driver,60,2).until(EC.presence_of_element_located((By.ID, '_ctl0_txtusername')))
driver.find_element_by_id('_ctl0_txtusername').send_keys('学号')
driver.find_element_by_id('_ctl0_txtpassword').send_keys('密码')
#driver.find_element_by_id('_ctl0_txtyzm').send_keys(code)
#driver.find_element_by_id('_ctl0_ImageButton1').click() # 点击
time.sleep(30)


#进入评价页面
driver.switch_to.frame("PageFrame")
driver.find_element_by_xpath('//a[@href="dcpg/jxpjlist.aspx"]').click() # 点击

#time.sleep(30)
WebDriverWait(driver,120,2).until(EC.presence_of_element_located((By.XPATH, '//td[contains(text(),"未参加")]/following-sibling::td[1]/a')))
name = driver.find_element_by_xpath('//td[contains(text(),"未参加")]/following-sibling::td[1]/a')

while name:
    name.click()
    WebDriverWait(driver,120,2).until(EC.presence_of_element_located((By.ID, 'cmdAdd')))

    #输入评教内容
    driver.find_element_by_id('txtpjyj').send_keys(random.choice(text_options))
    selects = driver.find_elements_by_xpath('//select[starts-with(@id,"dgData__")]')
    for select in selects:
        Select(select).select_by_visible_text(random.choice(select_options))
        time.sleep(0.3)

    #保存评教内容
    driver.find_element_by_id('cmdAdd').click()
    dig_confirm = driver.switch_to.alert
    time.sleep(1)
    dig_confirm.accept()
    print("完成{0}老师评教".format(driver.find_element_by_id('lbljsxm').text))

    #返回上级页面
    driver.find_element_by_id('lnkExit').click()
    try:
        WebDriverWait(driver,60,2).until(EC.presence_of_element_located((By.XPATH, '//td[contains(text(),"未参加")]')))
        name = driver.find_element_by_xpath('//td[contains(text(),"未参加")]/following-sibling::td[1]/a')
    except:
        break
    

print("完成所有评教")

driver.quit()