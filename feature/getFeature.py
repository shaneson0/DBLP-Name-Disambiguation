# coding=utf-8



import re

import nltk
import pandas as pd
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

from feature.getdata import getdata

SelfFilter = ['11i', '802.11i', '15-point', '16-18', '18', '2004']

STOPWORDS = stopwords.words('english') + ['algorithm', 'based', 'content-based' , 'ieee', 'ieee trans', 'trans', 'using', 'problem', 'approach', 'method']




#  2018/09/30
# 先把stop-words去掉吧，这个有点碍位置
def test():
    texts = ["good movie", "not a good movie", "did not like","i like it", "good one"]
    tfidf = TfidfVectorizer(min_df=0, max_df=1, ngram_range=(2,2) )
    features = tfidf.fit_transform(texts)
    res = pd.DataFrame(features.todense(),columns=tfidf.get_feature_names())
    return res

def TF_IDF_GetFeatures(texts):
    tfidf = TfidfVectorizer(min_df=0.0, max_df=1.0, ngram_range=(1, 2))
    features = tfidf.fit_transform(texts)

    terms = tfidf.get_feature_names()
    sums = features.sum(axis=0)

    # connecting term to its sums frequency
    data = []
    for col, term in enumerate(terms):
        data.append((term, sums[0, col]))

    ranking = pd.DataFrame(data, columns=['term', 'rank'])
    ranking.sort_values('rank', inplace=True, ascending=False)
    ranking.to_csv("./data/FeaturesRanking.csv", index=False)

    # 提取前100个特征，用于关键字特征用

    MainFeatures = ranking[:100]
    MainFeatures.to_csv("./data/vocabularyFeature.txt", index=False)


    res = pd.DataFrame(features.todense(), columns=tfidf.get_feature_names())
    res.to_csv("./data/features.csv", index=False)










def GetDomainFeature(text):

    # 统一小写
    text = text.lower()

    # 去除{}和换行
    text = text.replace("\n", " ")
    text = text.replace("{", "")
    text = text.replace("}", "")
    text = text.replace("-", " ")


    # tokenizer
    tokenizer = nltk.tokenize.WhitespaceTokenizer()
    tokens = tokenizer.tokenize(text)

    # Stemming

    # stemmer = nltk.stem.PorterStemmer()
    stemmer = nltk.stem.WordNetLemmatizer()
    text = [stemmer.lemmatize(token) for token in tokens]
    newtext = []

    # 去除数字
    for word in text:
        if re.search(r'^-?[1-9]\d*$', word) is None:
            newtext.append(word)

    # print('------ STOPWORDS --------')
    # print(STOPWORDS)

    # for word in newtext:
    #     print(word)

    # 去除STOPWORDS
    FinalArray = []
    for word in newtext:
        flag = True
        for stopword in STOPWORDS:
            if stopword == word:
                flag = False
                break
        if flag:
            for filterword in SelfFilter:
                if filterword in word:
                    flag = False
                    break
        if flag:
            FinalArray.append(word)


    for word in FinalArray:
        print(word)

    return FinalArray


def GetAllDomainFeatures():
    papers = getdata()
    NewFeaturesArray = []
    for paper in papers:
        paper['features'] = []
        if 'journal' in paper:
            JournalFeatures = GetDomainFeature(paper['journal'])
            paper['features'] = paper['features'] + JournalFeatures
        if 'title'in paper:
            TitleFeatures = GetDomainFeature(paper['title'])
            paper['features'] = paper['features'] + TitleFeatures
        NewFeaturesArray.append(' '.join(paper['features']))
    return NewFeaturesArray




if __name__ == "__main__":
    # text = 'Computers {\\&} Mathematics with Applications'
    # print(GetDomainFeature(text))
    NewFeaturesArray = GetAllDomainFeatures()
    TF_IDF_GetFeatures(NewFeaturesArray)
    # for paper in papers:
    #     if len(paper['features']) > 0:
    #         print(paper['features'])

























