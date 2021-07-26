# coding: utf-8
import numpy as np
import math as m


class calPlan():
    def __init__(self):
        pass

    def doubleS(self, vmax, amax, jmax, p0, p1, Ts):
        if (p1 - p0)<pow(10, -8):
            return
        D = p1 - p0
        Tj = amax / jmax
        vlimit = amax * Tj
        Dlimit = vlimit * Tj
        if (Dlimit>D / 2):  # 没有达到设置的最大加速度
            tj = pow(D / (2 * jmax), 1 / 3)
            vpeak = jmax * pow(tj, 2)
            if (vpeak>vmax):  # 判断是否达到最大速度
                tj = np.sqrt(vmax / jmax)
                Da = tj * vmax  # Da是计算出来的除匀速段外的距离
                tv = (D - 2 * Da) / vmax
            else:
                tv = 0
            ta = 2 * tj
        else:  # 能达到设计的最大加速
            if (vlimit>vmax):  # 判断是否有匀加速段
                tj = np.sqrt(vmax / jmax)
                Da = vmax * tj
                tv = (D - 2 * Da) / vmax
                ta = tj + tv
            else:  # 有匀加速段
                tj = Tj
                Tav = Tj + vmax / amax
                Da = vmax * Tav
                if (Da>D):
                    vpeak = amax * (np.sqrt(pow(Tj, 2) + 4 * D / amax) - Tj) / 2
                    ta = vpeak / amax + tj
                    tv = 0
                else:
                    ta = Tav
                    tv = (D - Da) / vmax
        if (tv != 0):
            vpeak = vmax
        Ttoal = 2 * ta + tv
        r = Ttoal / Ts
        scale = m.ceil(r) / r
        a21, a22, a23, a24 = jmax * pow(tj, 3) / 6, jmax * pow(tj, 3) / 2, jmax * tj, tj
        a31 = jmax * tj * (3 * pow(ta, 2) - 9 * ta * tj + 7 * pow(tj, 2)) / 6
        a32, a33, a34 = jmax * tj * (ta - tj * 3 / 2), jmax * tj, ta - tj
        a41, a42, a43, a44 = ta * vpeak / 2, vpeak, 0, ta
        praResult1 = np.array([np.ones(4), [a21, a22, a23, a24], [a31, a32, a33, a34], [a41, a42, a43, a44]])
        temp = np.array([D - praResult1[:, 0], praResult1[:, 1], -praResult1[:, 2], Ttoal - praResult1[:, 3]])
        praResult2 = np.flipud(np.transpose(temp))
        praResult = np.vstack(praResult1, praResult2)
        praResult[:,1]=praResult[:,1]/scale
        praResult[:,2]=praResult[:,2]/pow(scale,2)
        praResult[:,3]=praResult[:,3]/scale
        return praResult

    def calInterpolation(self, praResult, p1, p0, time):
        t=praResult[:,-1]
        T=np.diff(t)
        D=p1-p0
        p,v,a=praResult[:,0],praResult[:,1],praResult[:,2]
        b=np.zeros((7,4))
        b[:,0]=p[0:-1]
        b[:,1]=v[0:-1]
        b[:,2]=np.array([0,a[1]/2,a[2]/2,0,0,a[5]/2,a[6]/2])

        jmax=a[1]/t[1]
        b[:,3]=np.array([jmax/6,0,-jmax/6,0,-jmax/6,0,jmax/6])
        data=[]
        for i in range(len(t)-1):
            if(t[i]<=time<=t[i+1]):
                p=b[i,0]+b[i,1]*(time-t[i])+b[i,2]*pow(time-t[i],2)+b[i,3]*pow(time-t[i],3)
                v=b[i,1]+2*b[i,2]*(time-t[i])+3*b[i,3]*pow(time-t[i],2)
                a=2*b[i,2]+6*b[i,3]*pow(time-t[i],1)
                j=6*b[i,3]
                data=[t,p,v,a,j]
                break
            if time>=np.sum(T):
                p=p1
                v,a,j=0,0,0
                data=[time,p,v,a,j]
                break
        return data
