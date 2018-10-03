
# coding=utf-8

from feature.constructFeature import findFeatureArrayBytfidf
from feature.getFeature import GetAllDomainFeatures


import pandas as pd
from feature.text_feature_dbscan import CountDBSCAN
import numpy as np

# 提起文本特征

# NewFeaturesArray = GetAllDomainFeatures()
# findFeatureArrayBytfidf(NewFeaturesArray)

# 尝试用dbscan提取文本特征

path = './data/extractVocabularyFeature.csv'
X = pd.read_csv(path)

def CountNoisyRate(labels):
    NoisyLen = len(list(filter(lambda labelType: labelType == -1, labels)))
    return NoisyLen

# 0.965, 1.0 is the best

clusternum , labels = CountDBSCAN(0.81, 1, X)
print(labels)
print('clusternum: ', clusternum)
print('CountNoisyRate: ', CountNoisyRate(labels))

# 枚举一下什么参数可以求最小的噪声比
# 寻找最小的噪声比，得到(15, 0, 0.9510204081632653, 1.0)这个较为优的结果
# EpsArray = np.linspace(0.1, 14).tolist()
# MinNumArray = np.linspace(1 , 15).tolist()
#
#
#
# ResArray = []
# for Eps in EpsArray:
#     for MinNum in MinNumArray:
#         tempClusternum, templabels = CountDBSCAN(Eps, MinNum, X)
#         NoisyLen = CountNoisyRate(templabels)
#         ResArray.append((tempClusternum, NoisyLen, Eps, MinNum))
#
# ResArray = sorted(ResArray, key=lambda item: item[1])
# print(ResArray)




# 求extractVocabularyFeature.csv 中欧式距离的最大最小值

# 这是测试A - B的距离测试值
# print((X.iloc[0]).shape)
# print((X.iloc[1]).shape)
# print( np.linalg.norm( np.transpose(X.iloc[0]) - np.transpose(X.iloc[1]) ) )


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




#
# 1.4142135623730954
# 0.0
# 303616.5900256383
# 673.0
# 451.1390639311119



















