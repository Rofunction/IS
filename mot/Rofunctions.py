# coding utf-8
import tkinter
from tkinter import filedialog


def getfilePath():
    root = tkinter.Tk()  # 生成root主窗口
    root.withdraw()  # 隐匿button按钮
    filePath = filedialog.askopenfilename()
    return filePath


def dataSplit(filePath, Delimiter):
    strList = []
    with open(filePath, 'r') as file:
        for line in file:
            strList.append(line.replace('\n', '').split(Delimiter))
    return strList


def str2Num(strList):
    numList = []
    for xlist in strList:  # 外循环
        numList.append([float(x) for x in xlist])  # 内循环（每行中的每个数据都转换）
    return numList
