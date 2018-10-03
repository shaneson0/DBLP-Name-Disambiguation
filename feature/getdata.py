# coding=utf-8

import bibtexparser


# 数据预处理
# 去掉Jun Zhang

def FixAuthor(author):
    author = author.replace("\n", "")
    author = author.replace(" ", "")
    authors = author.split("and")
    # print(authors)
    authors.remove('JunZhang')
    return authors


def getAuthorsPaper(filename):
    with open(filename) as bibtex_file:
        bibtex_str = bibtex_file.read()

    bib_database = bibtexparser.loads(bibtex_str)
    authors_paper = []
    for item in bib_database.entries:
        if 'author' in item:
            author = item['author']
        elif 'editor' in item:
            author = item['editor']
        else:
            continue
        if 'Jun Zhang' in author:
            # print(item)
            authors = FixAuthor(author)
            item['authors'] = authors
            authors_paper.append(item)
    return authors_paper

def getdata():
    AllPapers = []

    for i in range(1, 11, 1):
        if i < 10:
            filename = './data/Zhang_000%d_Jun.bib' % i
        else:
            filename = './data/Zhang_0010_Jun.bib'
        papers = getAuthorsPaper(filename)
        AllPapers = AllPapers + papers

    return AllPapers











