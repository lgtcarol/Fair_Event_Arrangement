#from gensim.corpora

# -*- coding: utf-8 -*-
import pandas as pd
import codecs
import json
import re
import sys
import string
import nltk
import os
import string
from gensim import corpora


#lgt: origin :reload(sys)
#换为如下两行
import importlib,sys
importlib.reload(sys)

#lgt:去掉本行 sys.setdefaultencoding('utf-8')

common_path = '../data/NY_info/members_by_group%d'
group_path = '../data/group/groups_int_category%d.csv'
texts_path = '../data/texts/'


def get_text(text):
    """Read text from a string(html), normalizing whitespace and stripping HTML
    markup."""
    text = re.sub(r'<.*?>', ' ', text)
    text = re.sub('\s+', ' ', text)
    text = text.translate(string.maketrans("",""), string.punctuation)
    return text



#传入参数应为待处理文档
def Text2Vec(filepaths):
    from pprint import pprint
    # getting a stopword list
    path = '../data/StopWords.txt'
    with codecs.open(path, 'r', encoding='utf-8') as fr:
        content = fr.read()
        stoplist = set(content.split())

    # get a corpora(全集)
    documents = []
    for filepath in filepaths:
        with codecs.open(filepath, 'r', encoding='utf-8') as fr:
            content = fr.read()
            documents.append(get_text(str(content)))

    texts = [[word for word in document.lower().split() if
              word not in stoplist] for document in documents]#将text过滤为不含停用词的文本
    #pprint(texts)

    dictionary = corpora.Dictionary(texts)#corpora.Dictionary对象，documents参数也可以是列表的列表例如常见的文档矩阵：
    dictionary.save('../data/dictionary/event_description_test.dict')
    pprint(dictionary.token2id)

    corpus = [dictionary.doc2bow(text) for text in texts]
    corpora.MmCorpus.serialize('../data/dictionary/event_description_test.mm', corpus)
    pprint(corpus)

    pass


def VecApplyLDA():
    from gensim import corpora, models, similarities
    if os.path.exists('../data/dictionary/event_description_test.dict'): ##字典找不到，或者怎么生成呢？
        dictionary = corpora.Dictionary.load('../data/dictionary/event_description_test.dict')
        corpus = corpora.MmCorpus('../data/dictionary/event_description_test.mm')
        print("used files generated from test documents")
    else:
        print("No matched files found! ")

    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]

    lda = models.LdaModel(corpus_tfidf, id2word=dictionary, num_topics=3)
    corpus_lda = lda[corpus_tfidf]

    for doc in corpus_lda:
        print(doc)


    pass


if __name__ == '__main__':
    #retrieveGroupMembers(21)
    #retrieveDescription(1)
    """for i in range(1, 37):
        if i == 7 or i == 19:
            continue
        else:
            retrieveDescription(i)"""
    #retrieveEventDescription()
    path = '../data/texts/event_description/'
    #filepaths = [path + filename for filename in os.listdir(path)]

    #Text2Vec(filepaths[:5])
    VecApplyLDA()

    #print(get_text('a,b , c;?'))

    pass
