import os
from PIL import Image
dir_name = "D:\\new"  #文件位置
movie_name = os.listdir(dir_name)

total =1
for temp in movie_name:
    img = Image.open(dir_name + "\\\\" + temp)
    if(img.size[0] != 640 and img.size[1] != 480):
        print(temp + "尺寸不对")
    total = total + 1
print(total)