# coding:utf-8
from planTra import TgPy
import math as m
import numpy as np

i=(2.16-1)/2.16
s1=0
s2=1000
vm=600/i
am=4000/i**2
jm=10000/i**3
# vm=1500
# am=3000
# jm=30000

Ts=0.008
W=2*m.pi
Dr=0.005
wd=W*m.sqrt(1 - Dr ** 2)
K=m.exp(-Dr * m.pi / m.sqrt(1 - pow(Dr,2)))
Td=2*m.pi/wd
A1=1/(1+K)**2
A2=2*K/(1+K)**2
A3=K**2/(1+K)**2
A=[A1,A2,A3]
T=[0,0.5*Td,Td]

# inti pos
#p_init=np.array([287.96,-220.74,472.02,166.48,0.46,-179.67])
# p_init=np.array([190.88,-544.20,472.02,166.48,0.46,-179.66])
p_init=np.array([3.65,-767.19,481.65,166.48,0.45,-179.68])
# shape command trajectory
q=TgPy().doubleSVel(s1,s2,vm,am,jm,Ts)
sumT=t=q[-1,-1]
datalist=[]
originlist=[]
tList=[]

print("total run time ={}".format(q[-1,-1]))
print("shaped total time ={}".format(Td+sumT))
for t in np.arange(0,sumT+Td+100*Ts,Ts):
    t1=t-T[0]
    t2=t-T[1]
    t3=t-T[2]
    if t1<0:
        t1=0
    if t2<0:
        t2=0
    if t3<0:
        t3=0
    data0=TgPy().calculateInterpolation(q,Ts,s1,s2,jm,t)
    data1=TgPy().calculateInterpolation(q,Ts,s1,s2,jm,t1)
    data2=TgPy().calculateInterpolation(q,Ts,s1,s2,jm,t2)
    data3=TgPy().calculateInterpolation(q,Ts,s1,s2,jm,t3)
    data1[1]=data1[1]*A[0]
    data2[1]=data2[1]*A[1]
    data3[1]=data3[1]*A[2]
    data=np.array(data1)+np.array(data2)+np.array(data3)
    tList.append(t)
    datalist.append(data)
    originlist.append(data0)

datalist = np.array(datalist)
originlist = np.array(originlist)
originPos = originlist[:,1]
originVel = originlist[:,2]
originAcc = originlist[:,3]
shapedPos = datalist[:,1]

# origin data
origin_xData = p_init[0] + originPos*m.sqrt(2)/2
origin_yData = p_init[1] + originPos*m.sqrt(2)/2
origin_zData = p_init[2] * np.ones(len(origin_xData))
origin_aData = p_init[3] * np.ones(len(origin_xData))
origin_bData = p_init[4] * np.ones(len(origin_xData))
origin_cData = p_init[5] * np.ones(len(origin_xData))
originData = np.array([origin_xData,origin_yData,origin_zData,origin_aData,
                     origin_bData,origin_cData])
originList = []
for i in range(len(origin_xData)):
    originList.append([origin_xData[i],origin_yData[i],origin_zData[i],origin_aData[i],
                       origin_bData[i],origin_cData[i]])
originData = np.array(originList)

# shaped data
shaped_xData = p_init[0] + shapedPos*m.sqrt(2)/2
shaped_yData = p_init[1] + shapedPos*m.sqrt(2)/2
shaped_zData = origin_zData
shaped_aData = origin_aData
shaped_bData = origin_bData
shaped_cData = origin_cData

shapedList = []
for i in range(len(shaped_xData)):
    shapedList.append([shaped_xData[i],shaped_yData[i],shaped_zData[i],shaped_aData[i],
                       shaped_bData[i],shaped_cData[i]])
shapedData = np.array(shapedList)


with open('../shaped683005.csv', 'w') as inputFile:
    inputFile.write('dt;x;y;z;a;b;c;j_cfg' + '\n')
    for str in shapedData:
        inputFile.write("{dt};{x};{y};{z};{a};{b};{c};{j_cfg}".format(dt=0.008, x=str[0], y=str[1],
                z=str[2], a=str[3], b=str[4], c=str[5], j_cfg=1028) + '\n')
inputFile.close()

with open('../origin683005.csv', 'w') as inputFile:
    inputFile.write('dt;x;y;z;a;b;c;j_cfg' + '\n')
    for str in originData:
        inputFile.write("{dt};{x};{y};{z};{a};{b};{c};{j_cfg}".format(dt=0.008, x=str[0], y=str[1],
                z=str[2], a=str[3], b=str[4], c=str[5], j_cfg=1028) + '\n')
inputFile.close()




import matplotlib.pyplot as plt

velList=np.diff(shapedPos)/Ts
accList=np.diff(velList)/Ts
tList=np.array(tList)

plt.figure()
plt.plot(tList,shapedPos,label='shaped pos')
plt.plot(tList,originPos,label='origin pos')
plt.xlabel('time(s)')
plt.ylabel('deg')
plt.legend()
plt.show()

plt.figure()
plt.plot(tList,originVel,label='origin vel')
plt.plot(tList[0:-1],velList,label='shaped vel')
plt.xlabel('time(s)')
plt.ylabel('deg/s')
plt.legend()
plt.show()

plt.figure()
plt.plot(tList,originAcc,label='origin acc')
plt.plot(tList[0:-2],accList,label='shaped acc')
plt.xlabel('time(s)')
plt.ylabel('deg/s^2')
plt.legend()
plt.show()

## build system and calculate response
from scipy.signal import lsim
Ws=W
Crs=Dr
Num=np.array([Ws**2])
Den=np.array([1,2*Ws*Crs,Ws*Ws])
tout1, yout1,xout1 =lsim((Num,Den),originPos,tList)
tout2, yout2,xout2 =lsim((Num,Den),shapedPos,tList)
plt.figure(2)
plt.title('system response')
plt.plot(tout1,yout1,label='origin response')
plt.plot(tout2,yout2,label='shaped response')
plt.xlabel('time(s)')
plt.ylabel('deg')
plt.legend()
plt.show()