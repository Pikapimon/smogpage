result=[]
def rule_gen(freq,taclen,min_conf):#返回字典
	ret={}
	for freqSet in freq:
		allsubsets=getAllSubSets(freqSet[0])
		length=len(allsubsets)
		i=0
		# print(allsubsets)
		while i < length:
			set1=set(allsubsets[i])
			set2=set(freqSet[0])^set1
			# print("set1",set1,"set2",set2)
			conf,lift=getConf(freq,set1,set2,freqSet[1],taclen)
			if conf >= min_conf:
				tmp=frozenset([frozenset(set1),frozenset(set2)])
				ret[tmp]={"confidence":conf,"support":freqSet[1],"lift":lift}
			else:
				it=0
				while it < len(allsubsets):
					if set(allsubsets[it]).issubset(set1):
						allsubsets.remove(allsubsets[it])
						it-=1
						i-=1
						length-=1
					it+=1
			i+=1
	return ret

def getAllSubSets(a):#求全子集list
	result.clear()
	for i in range(1,len(a)):
		tmp=[0]*i
		dfs(0,0,a,len(a),i,tmp)
	return result

def getConf(freq,set1,set2,both,taclen):
	sup1=0
	sup2=0
	# print("set1",set1,"set2",set2)
	for i in freq:
		# print("i[0]",i[0],"set1",set1)
		if not (set(i[0])^set1):
			sup1=i[1]
			break
	for i in freq:
		if not (set(i[0])^set2):
			sup2=i[1]
			break
	return both/sup1,both/sup1/sup2*taclen

def dfs(k,f,arr,lenarr,n,tmp):
	if k==n:
		result.append(list(tmp))
		return;
	for i in range(f,lenarr):
		tmp[k]=arr[i]
		dfs(k+1,i+1,arr,lenarr,n,tmp)
