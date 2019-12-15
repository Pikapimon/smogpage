from .Node import *
import copy as cp


class FP_Growth:
    def __init__(self, t, ms, mc):
        self.transac = self.getInitSet(t)
        self.min_sup = ms
        self.min_conf = mc
        self.f = []  # 生成最终频繁集

    def getInitSet(self, t):
        ret = {}
        for trans in t:
            ret[frozenset(trans)] = ret.get(frozenset(trans), 0)+1
        return ret

    def createTree(self, dataSet):
        headerTable = {}
        retTree = Node("NULL", 1, None)
        # 获得每一个事务个体的频繁度
        for trans in dataSet:
            for item in trans:
                headerTable[item] = headerTable.get(item, 0)+dataSet[trans]
        # 删去不满足频繁度大于等于min_sup的个体
        for k in list(headerTable.keys()):
            if headerTable[k] < self.min_sup:
                del(headerTable[k])
        freqItemSet = set(headerTable)  # 将满足条件的个体转存为集合
        if len(freqItemSet) != 0:
            for k in headerTable:
                headerTable[k] = [headerTable[k], None]
        for trans, count in dataSet.items():  # 遍历键值元组
            localD = {}
            for item in trans:
                if item in freqItemSet:
                    localD[item] = headerTable[item][0]
            if len(localD) > 0:
                orderedItems = [v[0] for v in sorted(
                    localD.items(), key=lambda p:p[1], reverse=True)]
                self.updateTree(orderedItems, retTree, headerTable, count)
        return retTree, headerTable

    def updateTree(self, items, inTree, headerTable, count):
        if items[0] in inTree.children:
            inTree.children[items[0]].addWeight(count)
        else:
            inTree.children[items[0]] = Node(items[0], count, inTree)
            if headerTable[items[0]][1] == None:
                headerTable[items[0]][1] = inTree.children[items[0]]
            else:
                self.updateHeader(
                    headerTable[items[0]][1], inTree.children[items[0]])
            if len(items) > 1:
                self.updateTree(
                    items[1::], inTree.children[items[0]], headerTable, count)

    def updateHeader(self, nodeToTest, targetNode):
        while nodeToTest.next != None:
            nodeToTest = nodeToTest.next
        nodeToTest.next = targetNode

    def ascendTree(self, leafNode, prefixPath):
        if leafNode.parent != None:
            prefixPath.append(leafNode.name)
            self.ascendTree(leafNode.parent, prefixPath)

    def findPrefixPath(self, basePat, treeNode):
        condPats = {}
        while treeNode != None:
            # print(1)
            prefixPath = []
            self.ascendTree(treeNode, prefixPath)
            if len(prefixPath) > 1:
                condPats[frozenset(prefixPath[1:])] = treeNode.weight
            treeNode = treeNode.next
        return condPats

    def mineTree(self, inTree, headerTable, prefix, freqItemList):
        bigL = [v[0]
                for v in sorted(headerTable.items(), key=lambda p: p[1][0])]
        for basePat in bigL:
            newFreqSet = prefix.copy()
            newFreqSet.add(basePat)
            freqItemList.append(newFreqSet)
            conpattBases = self.findPrefixPath(
                basePat, headerTable[basePat][1])
            myCondTree, myHead = self.createTree(conpattBases)
            if myHead != None:
                self.mineTree(myCondTree, myHead, newFreqSet, freqItemList)

    def get_freq_sets(self):
        # print(self.transac)
        tree, header = self.createTree(self.transac)
        # print(tree.get_tree_dict())
        # print(header)
        self.mineTree(tree, header, set([]), self.f)
        return self.f, tree.get_tree_dict()
        # return self.f
