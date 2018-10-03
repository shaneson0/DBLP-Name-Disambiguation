# coding=utf-8

import numpy as np

from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

# #############################################################################
# Generate sample data

Data = [
    [1,1,1,1],
    [2,2,2,2],
    [3,3,3,3],
    [4,4,4,4]
 ]

X = StandardScaler().fit_transform(Data)

print('---- X ----')
print(X)

# #############################################################################
# Compute DBSCAN


db = DBSCAN(eps=0.3, min_samples=1).fit(X)
labels = db.labels_
# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)


print('Estimated number of clusters: %d' % n_clusters_)










