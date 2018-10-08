


def getValidFy(papers):
    nc = 0
    ni = 0
    paperlen = len(papers)
    for i in range(paperlen):
        for j in range(i+1, paperlen):
            PaperI = papers[i]
            PaperJ = papers[j]
            if PaperI['authorId'] == PaperJ['authorId'] and PaperI['patitionRes'] == PaperJ['patitionRes']:
                nc = nc + 1
            elif PaperI['authorId'] != PaperJ['authorId'] and PaperI['patitionRes'] != PaperJ['patitionRes']:
                nc = nc + 1
            else:
                ni = ni + 1

    return float(nc) / float(nc + ni)


