from .Node import *
from . import treePlotter


def createTree(dataSet, minSup=1):
    '''
    创建FP树
    '''
    headerTable = {}
    # 第一次扫描数据集
    for trans in dataSet:  # 计算item出现频数
        for item in trans:
            headerTable[item] = headerTable.get(item, 0) + dataSet[trans]
    headerTable = {k: v for k, v in headerTable.items() if v >= minSup}
    freqItemSet = set(headerTable.keys())
    #print ('freqItemSet: ',freqItemSet)
    if len(freqItemSet) == 0:
        return None, None  # 如果没有元素项满足要求，则退出
    for k in headerTable:
        headerTable[k] = [headerTable[k], None]  # 初始化headerTable
    #print ('headerTable: ',headerTable)
    # 第二次扫描数据集
    retTree = Node('NULL', 1, None)  # 创建树
    for tranSet, count in dataSet.items():
        localD = {}
        for item in tranSet:  # put transaction items in order
            if item in freqItemSet:
                localD[item] = headerTable[item][0]
        if len(localD) > 0:
            orderedItems = [v[0] for v in sorted(
                localD.items(), key=lambda p: p[1], reverse=True)]
            updateTree(orderedItems, retTree, headerTable,
                       count)  # 将排序后的item集合填充的树中
    return retTree, headerTable  # 返回树型结构和头指针表


def updateTree(items, inTree, headerTable, count):
    if items[0] in inTree.children:  # 检查第一个元素项是否作为子节点存在
        inTree.children[items[0]].inc(count)  # 存在，更新计数
    else:  # 不存在，创建一个新的treeNode,将其作为一个新的子节点加入其中
        inTree.children[items[0]] = Node(items[0], count, inTree)
        if headerTable[items[0]][1] == None:  # 更新头指针表
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])
    if len(items) > 1:  # 不断迭代调用自身，每次调用都会删掉列表中的第一个元素
        updateTree(items[1::], inTree.children[items[0]], headerTable, count)


def updateHeader(nodeToTest, targetNode):
    '''
    this version does not use recursion
    Do not use recursion to traverse a linked list!
    更新头指针表，确保节点链接指向树中该元素项的每一个实例
    '''
    while (nodeToTest.next != None):
        nodeToTest = nodeToTest.next
    nodeToTest.next = targetNode


def ascendTree(leafNode, prefixPath):  # 迭代上溯整棵树
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)


def findPrefixPath(basePat, treeNode):  # treeNode comes from header table
    condPats = {}
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode, prefixPath)
        if len(prefixPath) > 1:
            condPats[frozenset(prefixPath[1:])] = treeNode.weight
        treeNode = treeNode.next
    return condPats


def mineTree(inTree, headerTable, minSup, preFix, freqItemList):
    bigL = [v[0] for v in sorted(
        headerTable.items(), key=lambda p: p[1][0])]  # 1.排序头指针表
    for basePat in bigL:  # 从头指针表的底端开始
        newFreqSet = preFix.copy()
        newFreqSet.append([basePat, headerTable[basePat][0]])
        freq = min([t[1] for t in newFreqSet])
        adder = ([v[0] for v in newFreqSet])
        # print ('finalFrequent Item: ',newFreqSet)    #添加的频繁项列表
        freqItemList.append([adder, freq])
        condPattBases = findPrefixPath(basePat, headerTable[basePat][1])
        # print ('condPattBases :',basePat, condPattBases)
        # 2.从条件模式基创建条件FP树
        myCondTree, myHead = createTree(condPattBases, minSup)
#         print ('head from conditional tree: ', myHead)
        if myHead != None:  # 3.挖掘条件FP树
            # print ('conditional tree for: ',newFreqSet)
            # myCondTree.disp(1)
            mineTree(myCondTree, myHead, minSup, newFreqSet, freqItemList)


def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        retDict[frozenset(trans)] = retDict.get(
            frozenset(trans), 0) + 1  # 若没有相同事项，则为1；若有相同事项，则加1
    return retDict


def FP_Growth(dataList, min_sup):
    dataSet = createInitSet(dataList)
    ret = []
    tree, header = createTree(dataSet, min_sup)
    mineTree(tree, header, min_sup, [], ret)
    return ret, tree.get_tree_dict()


def getTreePlt(tree):
    plt = treePlotter.createPlot(tree)
    from io import BytesIO
    import base64
    sio = BytesIO()
    plt.savefig(sio, format='png')
    data = base64.encodebytes(sio.getvalue()).decode()
    html = 'data:image/png;base64,{} '
    return html.format(data)
