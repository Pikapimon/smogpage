import numpy as np
import pandas as pd
import matplotlib.pyplot as plt  # 可视化绘图
from sklearn import svm  # svm支持向量机
from sklearn.metrics import roc_curve, auc  # 计算roc和auc
from sklearn.datasets import make_blobs
from sklearn.manifold import TSNE
from sklearn.metrics import roc_curve, auc  # 计算roc和auc
from .cmap import *
# 前端使用下拉框提供核函数选择，必须是标准的核函数名
import matplotlib
matplotlib.use("TKAgg")


class SVM:  # 需要训练样本和预测样本
    # 预测数据可以是list,必须约定最后一列是类别信息
    def __init__(self, trainData, preData, test_target, penalty_coefficient, kernal):

        self.trainData = [x[0:-1] for x in trainData]  # 训练数据，简单二维list
        self.target = [x[-1] for x in trainData]  # 训练数据的类别

        self.classes = list(set(self.target))  # 类别种类

        self.kernal = kernal  # 核函数选择
        self.penalty_coefficient = penalty_coefficient

        self.svm_cnf = None  # 分类器

        self.preData = preData  # 预测样本

        self.test_target = test_target  # 需要绘制ROC曲线时使用

    def getPtsImg(self):  # 绘制trainData降维的散点图
        # print(self.target)
        from io import BytesIO
        import base64
        df = pd.DataFrame({'classes': self.target})
        tsne = TSNE(n_components=2, learning_rate=100).fit_transform(
            self.trainData)
        plt.figure(figsize=(6, 6))
        for i in self.classes:
            d = tsne[df['classes'] == i]
            print(d[0], d[1])
            plt.scatter(d[:, 0], d[:, 1], label=str(i))
        plt.legend(loc='best')
        sio = BytesIO()
        plt.savefig(sio, format='png')
        data = base64.encodebytes(sio.getvalue()).decode()
        html = 'data:image/png;base64,{} '
        return html.format(data)

    def train(self):  # 使用训练数据和target进行训练
        self.svm_cnf = svm.SVC(kernel=self.kernal, C=self.penalty_coefficient)
        self.svm_cnf.fit(self.trainData, self.target)
        self.result = self.svm_cnf.predict(self.preData)  # 使用模型预测值

    def getOutCome(self):
        return self.result

    def getHyperImg(self):
        df_target = pd.DataFrame({'classes': self.target})
        df_trainData = pd.DataFrame(self.trainData)
        from io import BytesIO
        import base64
        plt.figure(figsize=(6, 6))
        for i in range(len(self.classes)):
            d = df_trainData.values[df_target['classes'] == self.classes[i]]
            plt.scatter(d[:, 0], d[:, 1], label=str(self.classes[i]))
            # if self.target[i]==self.classes[0]:
            #   plt.scatter(self.trainData[i][0],self.trainData[i][1],label=str(self.classes[0]))
            # else:
            #   plt.scatter(self.trainData[i][0],self.trainData[i][1],label=str(self.classes[1]))
        for j in self.svm_cnf.support_:
            plt.scatter(self.trainData[j][0], self.trainData[j][1],
                        s=100, c='', alpha=0.5, linewidth=1.5, edgecolor='red')
        W = self.svm_cnf.coef_  # 方向向量W
        b = self.svm_cnf.intercept_  # 截距项b
        x = np.arange(0, 10, 0.01)
        y = (W[0][0]*x+b)/(-1*W[0][1])
        plt.scatter(x, y, s=5, marker='h')
        plt.legend(loc='best')
        sio = BytesIO()
        plt.savefig(sio, format='png')
        data = base64.encodebytes(sio.getvalue()).decode()
        html = 'data:image/png;base64,{} '
        return html.format(data)

    def getROC(self):
        fpr, tpr, threshold = roc_curve(
            self.test_target, self.result)  # 计算真正率和假正率
        roc_auc = auc(fpr, tpr)  # 计算auc的值
        lw = 2
        from io import BytesIO
        import base64
        plt.figure(figsize=(6, 6))
        plt.plot(fpr, tpr, color='darkorange',
                 lw=lw, label='ROC curve (area = %0.2f)' % roc_auc)  # 假正率为横坐标，真正率为纵坐标做曲线
        plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC')
        plt.legend(loc="lower right")
        sio = BytesIO()
        plt.savefig(sio, format='png')
        data = base64.encodebytes(sio.getvalue()).decode()
        html = 'data:image/png;base64,{} '
        return html.format(data)
