import numpy as np
import math
class TgPy():
    def __init__(self):
        pass
    def doubleSVel(self,p1,p2,vmax,amax,jmax,Ts):
        D=p2-p1
        TOLERANCE=10**-10
        pvatResult=np.zeros((8,4))
        if(D<TOLERANCE):
            return
        Tj=amax/jmax
        Vlimit=amax*Tj
        Dlimit=Tj*Vlimit
        if(Dlimit>D/2): ## no acceleration cruis
            tj=(D/(2*jmax))**(1/3)
            Vpeak=jmax*tj**2
            if(Vpeak>vmax):
                tj=np.sqrt(vmax/jmax)
                Da=tj*vmax
                tv=(D-2*Da)/vmax
            else:
                tv=0
            ta=2*tj
        else:
            if(Vlimit>vmax):
                tj=np.sqrt(vmax/jmax)
                Da=tj*vmax
                tv=(D-2*Da)/vmax
                ta=2*tj
            else: ## there are two acceleration cruises
                tj=Tj
                Tav=Tj+vmax/amax
                Da=vmax*Tav ## total distance include deceleration part
                if(Da>D): ## vmax can not be reached v*(v/amax+Tj)-D=0
                    Vpeak=amax*(np.sqrt(Tj**2+4*D/amax)-Tj)/2
                    ta=Vpeak/amax+tj
                    tv=0
                else: ## vmax can be reached
                    ta=Tav
                    tv=(D-Da)/vmax
        if(tv!=0):
            Vpeak=vmax
        Ttotal=2*ta+tv
        r=Ttotal/Ts
        scale=math.ceil(r)/r
        a21=jmax*tj**3/6
        a22=jmax*tj**2/2
        a23=jmax*tj
        a24=tj
        a31=(jmax*tj*(3*ta**2-9*ta*tj+7*tj**2))/6
        a32=jmax*tj*(ta-tj*3/2)
        a33=jmax*tj
        a34=ta-tj
        a41=ta*Vpeak/2
        a42=Vpeak
        a43=0
        a44=ta
        pvatResult1=np.array([[0,0,0,0],[a21,a22,a23,a24],[a31,a32,a33,a34],[a41,a42,a43,a44]])
        temp=np.array([D-pvatResult1[:,0],pvatResult1[:,1],-pvatResult1[:,2],Ttotal-pvatResult1[:,3]])
        #a=[D-n for n in pvatResult1(:,1)]
        pvatResult2=np.flipud(np.transpose(temp))
        pvatResult=np.vstack((pvatResult1,pvatResult2))
        # scale total trajectory time to int Ts
        pvatResult[:,1]=pvatResult[:,1]/scale
        pvatResult[:,2]=pvatResult[:,2]/scale**2
        pvatResult[:,3]=pvatResult[:,3]*scale
        return pvatResult

    def generateTG(self,pvatResult,Ts,p1,p2,Jmax):
        t=pvatResult[:,-1]
        T=np.diff(t)
        D=p2-p1
        p=pvatResult[:,0]
        v=pvatResult[:,1]
        a=pvatResult[:,2]
        b=np.zeros((7,4))
        b[:,0]=p[0:-1]
        b[:,1]=v[0:-1]
        b[:,2]=np.array([0,a[1]/2,a[2]/2,0,0,a[5]/2,a[6]/2])
        b[:,3]=np.array([Jmax/6,0,-Jmax/6,0,-Jmax/6,0,Jmax/6])
        data=[]
        for time in np.arange(0,np.sum(T)+Ts,Ts):
            for i in range(len(t)-1):
                if((t[i]<=time)and(t[i+1]>=time)):
                    p=b[i,0]+b[i,1]*(time-t[i])+b[i,2]*(time-t[i])**2+b[i,3]*(time-t[i])**3
                    v=b[i,1]+2*b[i,2]*(time-t[i])+3*b[i,3]*(time-t[i])**2
                    aa=2*b[i,2]+6*b[i,3]*(time-t[i])
                    j=6*b[i,3]
                    data.append([time,p,v,aa,j])
                    break
                if time>=np.sum(T):
                    p=p2
                    v=0
                    a=0
                    j=0
                    data.append([time,p,v,aa,j])
                    break
        return data

    def calculateInterpolation(self,pvatResult,Ts,p1,p2,Jmax,ti):
        t=pvatResult[:,-1]
        T=np.diff(t)
        D=p2-p1
        p=pvatResult[:,0]
        v=pvatResult[:,1]
        a=pvatResult[:,2]
        b=np.zeros((7,4))
        b[:,0]=p[0:-1]
        b[:,1]=v[0:-1]
        b[:,2]=np.array([0,a[1]/2,a[2]/2,0,0,a[5]/2,a[6]/2])

        Jmax2=a[1]/t[1]

        b[:,3]=np.array([Jmax2/6,0,-Jmax2/6,0,-Jmax2/6,0,Jmax2/6])
        data=[]
        time=ti
        for i in range(len(t)-1):
            if((t[i]<=time)and(t[i+1]>=time)):
                p=b[i,0]+b[i,1]*(time-t[i])+b[i,2]*(time-t[i])**2+b[i,3]*(time-t[i])**3
                v=b[i,1]+2*b[i,2]*(time-t[i])+3*b[i,3]*(time-t[i])**2
                aa=2*b[i,2]+6*b[i,3]*(time-t[i])
                j=6*b[i,3]
                data=[time,p,v,aa,j]
                break
            if time>=np.sum(T):
                p=p2
                v=0
                aa=0
                j=0
                data=[time,p,v,aa,j]
                break
        return data

    def unittest(self):
        s1=0
        s2=100
        vm=50
        am=300
        jm=5000
        q=self.doubleSVel(s1,s2,vm,am,jm,0.004)
        p=self.generateTG(q,0.008,s1,s2,jm)
        p=np.array(p)
        print("q={}".format(q))
        import matplotlib.pyplot as plt
        plt.ion()
        plt.figure(1)
        t=p[:,0]
        pos=p[:,1]
        vel=p[:,2]
        acc=p[:,3]
        jerk=p[:,4]
        plt.plot(t,pos,label='pos')
        plt.plot(t,vel,label='vel')
        plt.plot(t,acc,label='acc')
        plt.plot(t,jerk,label='jerk')
        plt.legend()
        plt.ioff()
        plt.show()
        return t,pos,vel,acc
        # print("p={}".format(p))

    def unittest1(self):
        s1=0
        s2=100
        vm=50
        am=300
        jm=500
        Ts=0.008
        q=self.doubleSVel(s1,s2,vm,am,jm,Ts)
        sumT=t=q[-1,-1]
        p=[]
        for t in np.arange(0,sumT+Ts,Ts):
            data=self.calculateInterpolation(q,Ts,s1,s2,jm,t)
            p.append(data)
        #p=generateTG(q,Ts,s1,s2,jm)
        p=np.array(p)
        print("q={}".format(q))
        import matplotlib.pyplot as plt
        plt.ion()
        plt.figure(1)
        t=p[:,0]
        pos=p[:,1]
        vel=p[:,2]
        acc=p[:,3]
        jerk=p[:,4]
        plt.plot(t,pos,label='pos')
        plt.plot(t,vel,label='vel')
        plt.plot(t,acc,label='acc')
        plt.plot(t,jerk,label='jerk')
        plt.legend()
        plt.ioff()
        plt.show()


################ Main Unit Test ###########


if __name__ == "__main__":
   # t,u1,u2,u3 =unittest1()
   tg1=TgPy()
   tg1.unittest1()