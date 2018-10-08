
# coding=utf-8

import pandas as pd
from feature.text_feature_dbscan import CountDBSCAN

# 尝试用dbscan提取文本特征

path = './data/extractVocabularyFeature.csv'
X = pd.read_csv(path)


clusternum = CountDBSCAN(0.35, 5, X)
print(clusternum)


