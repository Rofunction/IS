# coding utf-8
import Rofunctions as Rofun
import numpy as np

filePath = Rofun.getfilePath()
strdata = Rofun.dataSplit(filePath, ';')
del [strdata[0]]
dataNum = np.array(Rofun.str2Num(strdata))

needData = dataNum[:, 1::]
intervel = 6
IP = needData[:, :intervel]
Descartes = needData[:, intervel::]
# J_cfg是选解配置
#J_cfg = Descartes[:, intervel]

with open('../Output.csv', 'w') as inputFile:
    inputFile.write('dt;x;y;z;a;b;c;j_cfg' + '\n')
    for str in Descartes:
        inputFile.write("{dt};{x};{y};{z};{a};{b};{c};{j_cfg}".format(dt=0.008, x=str[0], y=str[1],
        z=str[2], a=str[3], b=str[4], c=str[5], j_cfg= str[6]) + '\n')

    # inputFile.write('dt;j1;j2;j3;j4;j5;j6;flags;aux1;aux2;out1;,out2;out3;out4' + '\n')
    # for str in IP:
    #     inputFile.write("{dt};{j1};{j2};{j3};{j4};{j5};{j6};1;0;0;0,-24;,-25,0;0;,".format(dt=0.008, j1=str[0],
    #     j2=str[1], j3=str[2], j4=str[3], j5=str[4],j6=str[5]) + '\n')

inputFile.close()
