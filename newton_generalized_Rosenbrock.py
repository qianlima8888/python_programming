from sympy import *
import numpy as np

#计算具体值
def calculateValue(Jac_or_Hess, x, isJacMac):
    result = []
    x_dic = {}

    for data in range(1, len(x)+1):
        x_dic['x{}'.format(data)] = x[data-1]
    
    if(isJacMac):
        for fun in Jac_or_Hess:
            result.append(float(fun.evalf(subs = x_dic)))
    else:
        for fun in Jac_or_Hess:
            tmp = []
            for f in fun:
                tmp.append(float(f.evalf(subs = x_dic)))
            result.append(tmp)
    
    return np.matrix(result).T

#返回雅可比矩阵
def jacobian(Y, paraSymbos):
    grad = []

    for para in paraSymbos:
        fun = diff(Y, para)
        grad.append(fun)

    return grad

#返回海森矩阵
def hessianM(Y, paraSymbos):
    hess = []
    
    for i in jacobian(Y, paraSymbos):
        hess.append(jacobian(i, paraSymbos))
        
    return hess

def coutSolve(x):
    print('[ ', end='')
    for i in x:
        print(i, end=' ')
    print(']')

#n代表参数n的个数
n = int(input("输入n值(即参数x的个数)："))

name = "x1"
for index in range(2, n+1):
    name += " x{}".format(index) 

paraSymbos = symbols(name)

Y = 100*(paraSymbos[1]-paraSymbos[0]**2)**2 + (1-paraSymbos[0])**2
x0 = [-1.2, 1]
for index in range(2, n):
     Y += 100*(paraSymbos[index]-paraSymbos[index-1]**2)**2 + (1-paraSymbos[index-1])**2
     if(index%2 == 0):
         x0.append(-1.2)
     else:
         x0.append(1)

print(type(Y))

time = 2000#最大迭代次数
err = 1e-8#误差小于此值时停止迭代

print("\n优化函数为:fx =", Y)
print("初值为： x = ", end='')
coutSolve(x0)
print("允许的最大迭代次数为:", time)
print("精度为:{}\n".format(err))

for i in range(1, time+1):
    print("开始第{}轮迭代....".format(i))
    grad = calculateValue( jacobian(Y, paraSymbos), x0, True) #一阶梯度即雅可比矩阵
    grad2 = calculateValue( hessianM(Y, paraSymbos), x0, False) #二阶梯度即海森矩阵
    try:
        delta = -(grad2.I) * grad
    except:
        print("二阶导矩阵不可逆，结束迭代。")
        print("优化失败。")
        break
    print("第{}次迭代结束。x = ".format(i),end='')
    for index in range(len(x0)):
        x0[index] += delta[index, 0]
    coutSolve(x0)

    if(delta.T * delta <err):
        print("达到定义精度，停止迭代。")
        break
    print("")