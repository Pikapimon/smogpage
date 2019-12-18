from .FP_Growth import *
from .k_means import *
from .apriori import *
from .SVM import *
from .k_medoids import *
import pandas as pd
import xlrd
import numpy as np
from .DFTools import *
# 本console文件也将被写成函数形式
# book = xlrd.open_workbook("data1.xlsx")
# sheet=book.sheets()[0]


class process:
    def __init__(self, fileName, method, paras):
        self.method = method
        self.paras = paras
        self.DF = getDF(fileName)
        self.preTreat()

    def start(self):
        paras = self.paras
        if self.method == 1:
            # freqSet,relatedSet
            return self.apriori(self.dataList, paras[0], paras[1])
        if self.method == 2:
            # freqSet,FPtree
            return self.FP_Growth(self.dataList, paras[0], paras[1])
        if self.method == 3:
            # classInfo,plt
            return self.k_means(self.dataList, paras[0], paras[1])
        if self.method == 4:  # SVM
            return self.SVM(self.dataList, paras)  # 惩罚系数、核函数、需要绘制ROC
        # if self.method==5:
        if self.method == 5:  # k_medoids
            return self.k_medoids(self.dataList, paras[0])

    def apriori(self, dataList, min_sup, min_conf):
        ap = apriori(dataList, min_sup, min_conf)
        ap.start()
        result = ap.getOutCome()  # 频繁集集
        ap.rule_gen()
        l, r = ap.getRule()
        retDic = {}
        for key in l:
            retDic[l[key]] = r[key]
        return result, retDic  # 返回频繁项集、关联信息

    def k_means(self, dataList,  k, iteration):
        km = k_means(k, iteration, dataList)
        classInfo = tranDF2list(km.getOutPut())
        plt = km.getImg()
        return classInfo, plt

    def FP_Growth(self, dataList, min_sup, min_conf):
        freqSet, tree = FP_Growth(dataList, min_sup)
        rules = rule_gen(freqSet, len(dataList), min_conf)
        # print(freqSet)
        return freqSet, rules, tree

    def SVM(self, dataList, paras):  # 使用SVM进行二分类
        length = len(dataList)
        penalty_coefficient = paras[0]  # 惩罚系数
        kernal = paras[1]  # 核函数
        need_ROC = paras[2]  # 是否需要绘制ROC
        test_target = None
        if need_ROC == 1:
            test_target = dataList[2]  # Sheet3中，如果有输出ROC曲线的意图
        svm = SVM(dataList[0], dataList[1], test_target,
                  penalty_coefficient, kernal)
        svm.train()
        plt_raw = svm.getPtsImg()
        result = svm.getOutCome()
        plt_Hyper = svm.getHyperImg()
        if need_ROC == 1:
            ROC = svm.getROC()
            return result, plt_raw, plt_Hyper, ROC
        else:
            return result, plt_raw, plt_Hyper

    def k_medoids(self, dataList, k):
        kct = k_medoids(dataList, k)
        kct.start()
        result = kct.getOutPut()
        plt = kct.getImg()
        return result, plt

    def preTreat(self):
        if self.method in [1, 2]:
            if len(self.DF) >= 2:
                self.dataList = tranDF2list(self.DF[0])
            else:
                self.dataList = tranDF2list(self.DF)
        elif self.method == 4:  # SVM分类
            sheets = len(self.DF)
            # print(sheets)
            if sheets == 2:
                self.dataList = [tranDF2list(
                    self.DF[0]), tranDF2list(self.DF[1])]
            elif sheets == 3:
                self.dataList = [tranDF2list(self.DF[0]), tranDF2list(
                    self.DF[1]), tranDF2list(self.DF[2])]
            elif sheets == 1:
                self.dataList = [tranDF2list(self.DF[0])]
        else:
            self.dataList = self.DF[1]


if __name__ == '__main__':
    pro = process('data.xlsx', 1, [0.4, 0.4])
    print(pro.start()[0])
