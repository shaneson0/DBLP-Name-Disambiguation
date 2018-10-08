
# coding=utf-8




import pandas as pd
from feature.text_feature_dbscan import CountDBSCAN
from communityFeature.constructCommunity import DFSAuthorSociety
import numpy as np
from feature.getdata import getdata
from communityFeature.constructCommunity import ConStructSocietyFeaturesByDFSAuthorSociety
from feature.getFeature import GetDomainFeature
from feature.getFeature import GetPapaersDomainFeatures
from feature.getFeature import TF_IDF_GetFeatures
from feature.constructFeature import findFeatureArrayBytfidf



# 融合特征，一起聚合


papers = getdata()
papers = papers[:-1]

papers = ConStructSocietyFeaturesByDFSAuthorSociety(papers)

# 求出每篇论文是什么类型的社交分类

# Final partition
FinalPartition = {}
FinalCnt = 0

# 尝试构造基于作者的社交网络
Social2Paper = {}
for paper in papers:
    if paper['SocialType'] in Social2Paper:
        Social2Paper[paper['SocialType']].append(paper)
    else:
        Social2Paper[paper['SocialType']] = [paper]



# 提取每组每篇的关键信息
temp = [] # 这个是用来存储等会要删掉的SocialType
labelIndex2SocialType = {}
SocialKeyInfoArray = []
Social2PaperKeys = Social2Paper.keys()
labelindex = 0
for SocialType in Social2PaperKeys:
    # -1的表示是独立的点，先不管。
    if SocialType == -1:
        continue

    # 根据尝试，211和143这两组其实不用进行再次，聚类，因为几乎是可以判断是同一个作者的文章的了，
    # 再次聚类会导致"黑洞效果"
    if len(Social2Paper[SocialType]) > 100:
        FinalPartition[FinalCnt] = Social2Paper[SocialType]
        FinalCnt = FinalCnt + 1
        temp.append(SocialType)
        continue
    SocialFeatures = GetPapaersDomainFeatures(Social2Paper[SocialType])
    SocialKeyInfoArray.append(SocialFeatures)
    labelIndex2SocialType[labelindex] = SocialType
    labelindex = labelindex + 1

# 删掉temp数组里面的socialType
for socialtype in temp:
    del Social2Paper[socialtype]

# to ./data/FeaturesRanking.csv
# to ./data/vocabularyFeature.txt
# to ./data/features.csv
TF_IDF_GetFeatures(SocialKeyInfoArray)
findFeatureArrayBytfidf(SocialKeyInfoArray)


# 尝试用dbscan提取文本特征

path = './data/extractVocabularyFeature.csv'
# path = './data/vocabularyFeature.txt'
X = pd.read_csv(path)



clusternum , labels = CountDBSCAN(1.254445, 1, X)

print('--- 分组情况是 ---')
print("X's len: ", len(X))
print('clusternum: ', clusternum)
print('labels: ', labels)
print('labelIndex2SocialType: ', labelIndex2SocialType)


for index,value in enumerate(labels):
    PartitionIndex = value + FinalCnt
    if PartitionIndex in FinalPartition:
        FinalPartition[PartitionIndex] = FinalPartition[PartitionIndex] + Social2Paper[labelIndex2SocialType[index]]
    else:
        FinalPartition[PartitionIndex] = Social2Paper[labelIndex2SocialType[index]]


for index, partition in enumerate(FinalPartition.keys()):
    print('index : ', index, len(FinalPartition[partition]))


print(len(papers))
# 成功划分了10类结果是
# index :  0 211
# index :  1 143
# index :  2 105
# index :  3 154
# index :  4 13
# index :  5 1
# index :  6 15
# index :  7 4
# index :  8 1
# index :  9 1

# 把index: 5，7,8,9，单独出来聚类，看能不能聚成4类

# 第三次聚合，处理噪声点
LeftClusterPapers = list(Social2Paper[-1]) + FinalPartition[5] + FinalPartition[7] + FinalPartition[8] + FinalPartition[9]
del FinalPartition[5]
del FinalPartition[7]
del FinalPartition[8]
del FinalPartition[9]

# features
print("------- left cluster -------")
print(LeftClusterPapers)
Finaltexts = []
for paper in LeftClusterPapers:
    if 'features' not in paper:
        GetPapaersDomainFeatures([paper])
    Finaltexts.append(' '.join(paper['features']))


TF_IDF_GetFeatures(Finaltexts, ranklimit=20)
findFeatureArrayBytfidf(Finaltexts)

path = './data/extractVocabularyFeature.csv'
X = pd.read_csv(path)
clusternum , labels = CountDBSCAN(0.9955204081632653, 0.0, X)

print('--- 第三次聚合的分组情况是 ---')
print("X's len: ", len(X))
print('clusternum: ', clusternum)
print('labels: ', labels)

ResultCnt = 10
for index, label in enumerate(labels):
    itemindex = label + ResultCnt
    if itemindex in FinalPartition:
        FinalPartition[itemindex] = FinalPartition[itemindex] + [LeftClusterPapers[index]]
    else:
        FinalPartition[itemindex] = [LeftClusterPapers[index]]


TerminalPapers = []
for index, partitionId in enumerate(FinalPartition.keys()):
    print('index : ', index, len(FinalPartition[partitionId]))
    # 对于每个partition添加partitionid进行标注
    for paper in FinalPartition[partitionId]:
        paper['patitionRes'] = index
    TerminalPapers = TerminalPapers + FinalPartition[partitionId]

from judge import judge

Result = judge.getValidFy(TerminalPapers)

print('Algorithm result is : ', Result)


# Final结果
# index :  0 211
# index :  1 143
# index :  2 105
# index :  3 154
# index :  4 13
# index :  5 15
# index :  6 21
# index :  7 1
# index :  8 9
# index :  9 1










# ==================================================================================================
#
#                                          求最小的噪声比
#
# ==================================================================================================


# 枚举一下什么参数可以求最小的噪声比
# 寻找最小的噪声比，得到(11, 0, 1.2346938775510206, 1.0)这个较为优的结果
# EpsArray = np.linspace(0.1, 14).tolist()
# MinNumArray = np.linspace(0 ,7).tolist()
#
# def CountNoisyRate(labels):
#     NoisyLen = len(list(filter(lambda labelType: labelType == -1, labels)))
#     return NoisyLen
#
#
# path = './data/extractVocabularyFeature.csv'
# X = pd.read_csv(path)
#
# ResArray = []
# for Eps in EpsArray:
#     for MinNum in MinNumArray:
#         tempClusternum, templabels = CountDBSCAN(Eps, MinNum, X)
#         NoisyLen = CountNoisyRate(templabels)
#         ResArray.append((tempClusternum, NoisyLen, Eps, MinNum))
#
# ResArray = sorted(ResArray, key=lambda item: item[1])
# # print(ResArray)
#
# for item in ResArray:
#     if item[1] == 0:
#         print(item)





# ==================================================================================================
#
#                                          求中欧式距离的最大最小值
#
# ==================================================================================================


# 求extractVocabularyFeature.csv 中欧式距离的最大最小值

# 这是测试A - B的距离测试值
# print((X.iloc[0]).shape)
# print((X.iloc[1]).shape)
# print( np.linalg.norm( np.transpose(X.iloc[0]) - np.transpose(X.iloc[1]) ) )

# path = './data/extractVocabularyFeature.csv'
# X = pd.read_csv(path)
# Sum = 0.0
# Min = 999999999
# Max = -1
# Threshold = 0.35
# ThresholdCnt = 0
# [rows, cols] = X.shape
# # print('rows : %d, cols: %d'%(rows, cols))
# for i in range(rows):
#     for j in range(i+1,rows):
#         try:
#             dist = np.linalg.norm( np.transpose(X.iloc[i]) - np.transpose(X.iloc[j]) )
#             if dist <= Threshold:
#                 print(dist)
#                 ThresholdCnt = ThresholdCnt + 1
#             Sum = Sum + dist
#             if dist > Max:
#                 Max = dist
#             if dist < Min:
#                 Min = dist
#         except:
#             print('error i :%d, j: %d'%(i,j))
#             break
#
#
# print('--- 欧式距离，距离矩阵的Max and Min ---')
# print('Max : ', Max)
# print('Min : ', Min)
# print('Sum : ', Sum)
# print('Rows: ', float(rows))
# print('averge: ', Sum / float(rows))
# print("Below Threshold's number: ", ThresholdCnt)



# --- 欧式距离，距离矩阵的Max and Min ---
# Max :  1.4142135623730951
# Min :  0.7112342791150912
# Sum :  506.44621323777375
# Rows:  28.0
# averge:  18.08736475849192
# Below Threshold's number:  0



















