from sklearn import svm
from DFTools import *
import numpy as np
import cv2 as cv
from sklearn.externals import joblib
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
def getClassifer(C,kernal,gamma='auto'):
	trainData=[]
	path="imgs/digits/train/"
	trainTarget=[x[0] for x in tranDF2list(getDF("imgs/digits/train.xls")[0])]
	target=[]
	for i in range(501):
		img_gray = cv.imread(path+str(i)+'.png', 0)
		trainData.append(img_gray.reshape(1,-1))
		target.append(trainTarget[i])
	print(target)
	trainData=np.array(trainData)
	nsamples,nx,ny=np.array(trainData).shape
	trainData=trainData.reshape((nsamples,nx*ny))
	svm_cnf=svm.SVC(kernel=kernal, C=C,gamma=gamma,probability=True)
	svm_cnf.fit(trainData.tolist(),target)
	joblib.dump(svm_cnf, "models/model.m")
def batch_img_predict(path,imgs):
	result=[]
	raw=[]
	targets=tranDF2list(getDF('imgs/digits/test.xls')[0])

	clf = joblib.load("models/model.m")
	for img in imgs:
		tmp=img
		raw.append(targets[int(tmp.split('.')[0])][0])
		img_gray = cv.imread(path+img, 0)
		ret = clf.predict(img_gray.reshape(1,-1))
		result.append(ret[0])
	precious=0
	for i in range(len(raw)):
		if raw[i]==result[i]:
			precious+=1
	return raw,result,"{0}%".format(round(precious/len(raw)*100,2)),cm_plot(raw,result)

def cm_plot(original_label, predict_label, pic=None):
    cm = confusion_matrix(original_label, predict_label)   # 由原标签和预测标签生成混淆矩阵
    # plt.figure(figsize=(6,6))
    plt.matshow(cm, cmap=plt.cm.Blues)     # 画混淆矩阵，配色风格使用cm.Blues
    plt.colorbar()    # 颜色标签
    for x in range(len(cm)):
        for y in range(len(cm)):
            plt.annotate(cm[x, y], xy=(x, y), horizontalalignment='center', verticalalignment='center')
            # annotate主要在图形中添加注释
            # 第一个参数添加注释
            # 第二个参数是注释的内容
            # xy设置箭头尖的坐标
            # horizontalalignment水平对齐
            # verticalalignment垂直对齐
            # 其余常用参数如下：
            # xytext设置注释内容显示的起始位置
            # arrowprops 用来设置箭头
            # facecolor 设置箭头的颜色
            # headlength 箭头的头的长度
            # headwidth 箭头的宽度
            # width 箭身的宽度
    plt.ylabel('True label')  # 坐标轴标签
    plt.xlabel('Predicted label')  # 坐标轴标签
    plt.title('confusion matrix')
    # if pic is not None:
    #     plt.savefig(str(pic) + '.jpg')
    return plt


	