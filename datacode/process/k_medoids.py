from pyclust import KMedoids
# KMedoids
import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from .DFTools import *
from .cmap import cnames


class k_medoids:

    def __init__(self, df, centers):
        self.centers = centers
        self.data = np.array(tranDF2list(df))

    def start(self):
        self.k = KMedoids(n_clusters=self.centers, distance='euclidean',
                          max_iter=1000).fit_predict(self.data)
        self.ret = np.hstack((self.data, self.k.reshape((-1, 1))))

    def getOutPut(self):
        return self.ret

    def getImg(self):
        keys = list(cnames.keys())
        data_TSNE = TSNE(learning_rate=100).fit_transform(self.data)
        plt.figure()
        for i in range(self.centers):
            d = data_TSNE[self.k == i]
            colors = cnames[keys[i]]
            plt.scatter(d[:, 0], d[:, 1], c=colors, s=10, label=str(i))
        plt.title('K-medoids Resul of {}'.format(str(self.centers)))
        plt.legend(loc='best')
        from io import BytesIO
        import base64
        sio = BytesIO()
        plt.savefig(sio, format='png')
        data = base64.encodebytes(sio.getvalue()).decode()
        html = 'data:image/png;base64,{} '
        return html.format(data)
