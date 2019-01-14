import os
dir_name = "C:\\Users\\bob\\Desktop\\图标注\\卧室\\卧室\\1"  #文件位置
movie_name = os.listdir(dir_name)
i = 0
for temp in movie_name:
    fileName = input("输入图片名称：")
    while(len(str(fileName)) != 4):
        print("输入格式错误，重新输入！")
        fileName = input("输入图片名称：")
    new_name = "00" + fileName +".jpg"  #新的文件名称
    while(os.path.exists(dir_name+'\\'+new_name)):
        print("该名称已使用，请重新输入！")
        fileName = input("输入图片名称：")
        new_name = "00" + fileName +".jpg"  #新的文件名称
    os.rename(dir_name+'\\'+temp, dir_name+'\\'+new_name)
    print(new_name + "修改成功！")