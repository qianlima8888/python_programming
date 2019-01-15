import os

def alter(file,old_str,new_str):
    """
    替换文件中的字符串
    :param file:文件名
    :param old_str:就字符串
    :param new_str:新字符串
    :return:
    """
    file_data = ""
    with open(file, "r") as f:
         for line in f:
             if old_str in line:
                 line = line.replace(old_str,new_str)
             file_data += line
    with open(file,"w") as f:
         f.write(file_data)
 
dir_name = "/home/wode/桌面/Annotations"
xml_name = os.listdir(dir_name)

i = 0
for temp in xml_name:
    alter(dir_name +'/' + temp, "indoorone", "indoortwo")
    print(temp + "修改成功")
    i = i + 1
print(i)