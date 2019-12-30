import os

old_str = ".png"
new_str = ".jpg"
path = "E:\\1"
fileList = os.listdir(path)
for file in fileList:
    with open(path+"\\"+file, "r", encoding="utf-8") as f1, open("%s.bak" % (path+"\\"+file), "w", encoding="utf-8") as f2:
        for line in f1:
            if old_str in line:
                line = line.replace(old_str, new_str)
            f2.write(line)
    os.remove(path+"\\"+file)
    os.rename("%s.bak" % (path+"\\"+file), (path+"\\"+file))
    print("change file %s" % file)
