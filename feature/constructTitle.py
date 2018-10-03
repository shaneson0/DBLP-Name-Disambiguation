
# coding=utf-8

import pandas as pd
from feature.text_feature_dbscan import CountDBSCAN

# 尝试用dbscan提取文本特征

path = './data/extractVocabularyFeature.csv'
X = pd.read_csv(path)

# X may be a sparse matrix, in which case only "nonzero"
#         elements may be considered neighbors for DBSCAN
# https://github.com/scikit-learn/scikit-learn/commit/494b8e574337e510bcb6fd0c941e390371ef1879
# if len(self.core_sample_indices_):
#     # fix for scipy sparse indexing issue
#     self.components_ = X[self.core_sample_indices_].copy()
# else:
#     # no core samples
#     self.components_ = np.empty((0, X.shape[1]))
clusternum = CountDBSCAN(0.35, 5, X)
print(clusternum)


