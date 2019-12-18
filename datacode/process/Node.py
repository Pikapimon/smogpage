class Node:
	def __init__(self,n,o,p):#name,频繁度,前驱
		self.name=n
		self.parent=p
		self.children={}
		self.weight=o#频繁度值
		self.tree={}#生成的fp tree
		self.next=None#相似元素连接
	def inc(self,w):
		self.weight+=w
	def get_tree_dict(self):
		ret={}
		# print(self.name)
		ret[self.name]=self.dict_gen(self.children)
		return ret
	def dict_gen(self,root):#使用根结点的children生成所有的
		ret={}
		for i in root:
			ret[i]=self.dict_gen(root[i].children)
		# print(ret)
		return ret



		