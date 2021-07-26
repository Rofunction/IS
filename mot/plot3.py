# coding: utf-8
import matplotlib as mpl
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import Rofunctions as Rofuc


filePath = Rofuc.getfilePath()
strdata = Rofuc.dataSplit(filePath,';')
del [strdata[0]]
dataNum = np.array(Rofuc.str2Num(strdata))

plt.figure()
# 设置三维图形模式
ax = plt.figure().gca(projection='3d')

# data
xData=dataNum[:,7]
yData=dataNum[:,8]
zData=dataNum[:,9]

ax.plot(xData,yData,zData)
plt.show()