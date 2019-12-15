from console import *
p = process("dataSVM.xlsx", 4, [1, 'linear', 1])
ret, plt_raw, plt_Hyper, a = p.start()
print(ret)
plt_raw.show()
plt_Hyper.show()
a.show()
# for key in relatSet:
# 	print(key,"=>",relatSet[key])
# pd.set_option('display.max_rows', 1000)
# print(classInfo)

# plt.show()
