#coding=utf8
import pickle
from collections import defaultdict #可以直接使用下标访问二维字典不存在的元素
def cal_corated_users():
    for u, items in train.items():
        for i in items:
            if i not in N.keys(): #如果一维字典中没有该键，初始化值为0
                N[i] = 0
            N[i] += 1
            for j in items:
                if i == j:
                   continue
                if j not in C[i].keys(): #如果二维字典中没有该键，初始化值为0
                    C[i][j] = 0
                C[i][j] += 1
def cal_matrix_W():
        for i, related_items in C.items():
            for j, cij in related_items.items():
                W[i][j] = cij /((N[i] * N[j])**0.5)

def recommend(train, user_id, W, K):
    rank = dict()
    ru = train[user_id] #用户数据，表示某物品及其兴趣度
    for i, pi in ru.items(): #i表示用户已拥有的物品id，pi表示其兴趣度
        #j表示相似度为前K个物品的id，wj表示物品i和物品j的相似度
        for j, wj in sorted(W[i].items(), key=itemgetter(1), reverse=True)[0:K]:
		    if j in ru: #如果用户已经有了物品j，则不再推荐
		        continue
		    if j not in rank.keys():
		    	rank[j]=0
		    rank[j] += pi * wj
    return rank
    
C = defaultdict(defaultdict) #用户与用户共同喜欢物品的个数
N = defaultdict(defaultdict) #用户个数
W = defaultdict(defaultdict)
train_file=open('train.pkl','rb')
train=pickle.load(train_file)
train_file.close()

cal_corated_users()
cal_matrix_W()
print W
W_file=open('W.pkl','wb')
pickle.dump(W,W_file)
W_file.close()
