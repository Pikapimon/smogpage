# k-means 需要聚类中心个数k和极小整数μ，最多支持二维数据聚类图返回
import pandas as pd
from .cmap import *
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


class k_means:
    def __init__(self, k, itr, df):
        self.data = df
        self.iteration = itr
        self.k = k

    def getOutPut(self):  # 返回DF
        self.data_zs = 1.0*(self.data - self.data.mean())/self.data.std()
        model = KMeans(n_clusters=self.k, max_iter=self.iteration)  # 分为k类
        model.fit(self.data_zs)  # 开始聚类
        r1 = pd.Series(model.labels_).value_counts()  # 统计各个类别的数目
        r2 = pd.DataFrame(model.cluster_centers_)  # 找出聚类中心
        self.r = pd.concat([r2, r1], axis=1)  # 横向连接（0是纵向），得到聚类中心对应的类别下的数目
        self.r.columns = list(self.data.columns) + [u'类别数目']  # 重命名表头
        self.r = pd.concat([self.data, pd.Series(
            model.labels_, index=self.data.index)], axis=1)  # 详细输出每个样本对应的类别
        self.r.columns = list(self.data.columns) + [u'聚类类别']  # 重命名表头
        return self.r

    def getImg(self):  # 得到聚类图片
        tsne = TSNE()
        tsne.fit_transform(self.data_zs)  # 进行数据降维,并返回结果
        tsne = pd.DataFrame(
            tsne.embedding_, index=self.data_zs.index)  # 转换数据格式
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        keys = list(cnames.keys())
        pk = 'o'
        for i in range(self.k):
            d = tsne[self.r[u'聚类类别'] == i]  # 找出聚类类别为0的数据对应的降维结果
            plt.scatter(d[0], d[1], marker=pk,
                        color=keys[i], s=40, label=str(i))
        plt.legend(loc='best')    # 设置 图例所在的位置 使用推荐位置
        return plt
