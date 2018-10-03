

import pandas as pd


from sklearn.feature_extraction.text import TfidfVectorizer

def getVocabularyFeature():
    cnt = 0
    map = {}
    with open('./data/vocabularyFeature.txt', 'r') as f:
        list1 = f.readlines()
        list1 = list1[1:]
        for line in list1:
            [term, _] = (line[:-2]).split(',')
            map[term] = cnt
            cnt = cnt + 1
    return map



def findFeatureArrayBytfidf(texts):
    FeaturesDict = getVocabularyFeature()
    tfidf = TfidfVectorizer(min_df=0.0, max_df=1.0, vocabulary=FeaturesDict)
    features = tfidf.fit_transform(texts)
    res = pd.DataFrame(features.todense(), columns=tfidf.get_feature_names())
    res.to_csv('./data/extractVocabularyFeature.csv', index=False)
























