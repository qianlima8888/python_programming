import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.animation as animation

y1 = [[0 for _ in range(400)],[0 for _ in range(400)],[0 for _ in range(400)]]
x = [x for x in range(400)]

fig = plt.figure() 
axes1 = fig.add_subplot(111) 
 
line1 = plt.plot(x, y1[0], 'r')
line2 = plt.plot(x, y1[1], 'b')
line3 = plt.plot(x, y1[2], 'g')

axes1.set_ylim(-1, 1) #设置y轴范围
plt.xticks([]) #关闭x轴刻度

def update(data):
  global y1, x, line1, line2, line3
  y1[0] = y1[0][1:] + [float(data.split()[0])]
  y1[1] = y1[1][1:] + [float(data.split()[1])]
  y1[2] = y1[2][1:] + [float(data.split()[2])]

  #删除上次绘制的曲线
  axes1.lines.remove(line1[0])
  axes1.lines.remove(line2[0])
  axes1.lines.remove(line3[0])
  
  #重新绘制
  line1 = plt.plot(x, y1[0], 'r')
  line2 = plt.plot(x, y1[1], 'b')
  line3 = plt.plot(x, y1[2], 'g')

def getData():
    f = open("/home/wode/data.txt")
    line = f.readline()
    while(line):
        yield line
        line = f.readline()

ani = animation.FuncAnimation(fig, update, getData, interval=10, repeat=False)
plt.show()