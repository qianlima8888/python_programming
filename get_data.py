import math

total_num = 1  #取得的第几个数据
now_index = 0  #向上取整的数据下标数
resolution = 1.18251 #间隔几个取数据
data_num = 0 #行数
targetNum = 2630 #需获取的数据个数

fileName = "/home/wode/桌面/误差分析/odom_raw.txt"
fileChangeName = "/home/wode/桌面/误差分析/odom_raw_change.txt"

f = open(fileName)             # 返回一个文件对象
line = f.readline()             # 调用文件的 readline()方法
while line and total_num <= targetNum:
    if math.ceil(now_index) == data_num:
        now_index = total_num * resolution
        total_num = total_num + 1
        with open(fileChangeName, "a") as cf:
            cf.write(line)
        print(line)
    data_num = data_num + 1
    line = f.readline()

print(total_num)

f.close()
