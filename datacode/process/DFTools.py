import pandas as pd
import numpy as np
def tranDF2list(dataList):
	tmpdata=np.array(dataList)#np.ndarray()
	retlist=tmpdata.tolist()#list
	# print(retlist)
	removeNAN(retlist)
	# print(retlist)
	return retlist

def getDF(inputfile):#前端传来的excel文件全部都是data.xlsx
	all_sheets=pd.read_excel(inputfile,index_col=0,sheet_name=None)#读取所有数据表
	sheet1=all_sheets['Sheet1']
	sheet1=pd.DataFrame(sheet1).fillna('')
	sheet2=all_sheets.get('Sheet2',pd.DataFrame())
	sheet3=all_sheets.get('Sheet3',pd.DataFrame())
	if not sheet2.empty:
		if not sheet3.empty:
			return sheet1,sheet2,sheet3
		else:
			return sheet1,sheet2
	else:
		return sheet1
def removeNAN(dataList):#直接对一个list进行处理 删除NAN
	for i in dataList:
		length=len(i)
		j=0
		while j<length:
			if i[j]=='':
				i.remove(i[j])
				j-=1
				length-=1
			j+=1 

