# apriori
import copy


class apriori:
    min_sup = 0
    min_conf = 0
    transac = []  # 事务集
    f = []  # 频繁集
    dic_left = {}  # 哈希频繁集
    dic_right = {}

    def __init__(self, tac, ms, mc):
        self.transac = copy.deepcopy(tac)
        self.min_conf = mc
        self.min_sup = ms

    def get_sup(self, t):
        k = 0
        for i in self.transac:
            if set(t) <= set(i):
                k += 1
        return k

    def apriori_gen(self, f):
        length = len(f)
        tret = []
        for i in range(length-1):
            j = i+1
            while j < len(f):
                if self.checkLegality(f[i], f[j]):
                    tmp = list(set(f[i]) | set(f[j]))
                    tmp.sort()
                    tret.append(tmp)
                j += 1
        # 剪枝
        ret = copy.deepcopy(tret)
        for i in range(len(tret)):
            tmp = list(tret[i])
            _tmp = list(tret[i])
            for j in range(len(tmp)):
                _tmp.remove(tmp[j])
                if _tmp in f:
                    _tmp = list(tmp)
                else:
                    ret.remove(tmp)
                    break
        return ret

    def checkLegality(self, a, b):
        length = len(a)
        if length == 1:
            return True
        for i in range(length-1):
            if a[i] != b[i]:
                return False
        return a[length-1] < b[length-1]

    def start(self):
        ci = []
        fi = []
        for i in self.transac:
            ci = list(set(ci) | set(i))
        ci.sort()
        for i in ci:
            sup = self.get_sup([i])
            if sup >= self.min_sup:
                tmp = []
                tmp.append(i)
                fi.append([tmp, sup])
        self.f.append(fi)
        j = 1
        while len(self.f[j-1]) != 0:
            ci = self.apriori_gen([i[0] for i in self.f[j-1]])
            fi = []
            for i in ci:
                sup = self.get_sup(i)
                if sup >= self.min_sup:
                    fi.append([i, sup])
            self.f.append(fi)
            j += 1

    def rule_gen(self):  # 使用频繁集去得到关联规则
        length = len(self.f)
        hashk = 0
        for i in range(1, length-2):  # 最后一个是空集
            lenrow = len(self.f[i])
            for j in range(lenrow):
                # 得到一个小集合的所有子集，均满足min_sup条件
                tmp_subs = self.getAllSubSets(self.f[i][j][0])
                lencol = len(tmp_subs)
                k = 0
                while k < lencol:
                    set1 = set(tmp_subs[k])
                    set2 = set(self.f[i][j][0]) ^ set1
                    # print(self.f[i][j][0],"set1:",set1,"set2:",set2)
                    conf, lift = self.getconf(list(set1), list(set2))
                    if conf >= self.min_conf:  # 存在强关联
                        hashk += 1
                        tmp = []
                        tmp.append(frozenset(set1))
                        tmp.append(frozenset(set2))
                        # print(tmp)
                        self.dic_left[hashk] = frozenset(tmp)
                        self.dic_right[hashk] = {
                            "confidence：": conf, "support:": self.f[i][j][1], "lift:": lift}
                    else:
                        r = 0
                        while r < lencol:
                            if set(tmp_subs[r]).issubset(set1):
                                tmp_subs.remove(tmp_subs[r])
                                r -= 1
                                lencol -= 1
                            r += 1
                    k += 1

    def getconf(self, a, b):
        both = list(set(a) | set(b))
        alen = len(a)
        all_sup = self.get_sup(both)
        lenf = len(self.f[alen-1])
        a_sup = 0
        b_sup = 0
        for i in range(lenf):
            if set(a).issubset(set(self.f[alen-1][i][0])):
                a_sup = self.f[alen-1][i][1]
                break
        for i in range(lenf):
            if set(b).issubset(set(self.f[alen-1][i][0])):
                b_sup = self.f[alen-1][i][1]
                break
        if a_sup != 0 and b_sup != 0:
            # conf lift
            return all_sup/a_sup, all_sup/a_sup/b_sup*len(self.transac)
        else:
            return -1, -1

    def getOutCome(self):
        return self.f

    def getAllSubSets(self, t):
        length = len(t)
        ret = []
        for i in range(length-1, 0, -1):  # 集合长度
            tmp = [0]*i
            vis = [False]*length
            self.dfs(tmp, i, ret, t, 0, 0)
        return ret

    def dfs(self, tmp, length, ret, raw, depth, s):
        if depth == length:
            ret.append(list(tmp))
        else:
            i = s
            while i < len(raw):
                tmp[depth] = raw[i]
                self.dfs(tmp, length, ret, raw, depth+1, i+1)
                i += 1

    def getRule(self):
        return self.dic_left, self.dic_right

    # def getOutComeImg():#返回一张图（描述关联性关系的可是化图）

    # def getOutComeImg(self):
