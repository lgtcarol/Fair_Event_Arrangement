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

#没太懂，大概就是网页内容正则匹配替换，标点处理吧
def get_text(text):
    """Read text from a string(html), normalizing whitespace and stripping HTML
    markup."""
    text = re.sub(r'<.*?>', ' ', text)
    text = re.sub('\s+', ' ', text)
    text = text.translate(string.maketrans("",""), string.punctuation)
    return text

#获取群组描述文本信息，对应events目录下
def retrieveDescription(category):
    path = group_path % category
    df = pd.read_csv(path)

    for i in range(len(df)):
        group = df.ix[i]

        with codecs.open('../data/texts/group_description/%s.txt' % str(group['urlname']), 'w', encoding='utf-8') as fw:
            fw.write(str(group['description']))
            #pass
    pass

#从群组组织过的事件中抽取出description,对应texts文件夹下的群组和事件描述
def retrieveEventDescription():
    #path = '../data/events/group_past_events/total_past_events.csv'
    path = './data/total_past_events.csv'
    df = pd.read_csv(path)

    for i in range(len(df)):
        event = df.ix[i]
        print(event['name'])
        name = str(event['name']).translate(string.maketrans("",""), string.punctuation)
        name = name.split(' ')
        """new name for identity """
        new_name = ''.join(name)
       # with codecs.open('../data/texts/event_description/%s.txt' % str(new_name), 'w', encoding='utf-8') as fw:
        with codecs.open('./data/event_description/%s.txt' % str(new_name), 'w', encoding='utf-8') as fw:
            fw.write(str(event['description']))
            #pass
    pass
    #retrieveEventDescription（）

#参数为群组编号，每次获取一个群组的成员，并保存到group_urlname.csv文件中
#遗留数据产生：能获取不同group的member.json文件，运行下述代码应能产生csv文件作为输入
def retrieveGroupMembers(category):
    path = common_path % category
    listGroups = os.listdir(path)
    for group_urlname in listGroups:
        group_path = path + '/' + group_urlname
        listMembers = os.listdir(group_path)
        group_members = pd.DataFrame(columns=['group'])
        #print group_members
        for count in listMembers:
            filepath = group_path + '/' + count
            with codecs.open(filepath, 'r', encoding='utf-8') as fr:
                print(filepath)
                content = json.load(fr)
                df = pd.DataFrame(content['results'], columns=['id', 'name'])
                group_members = group_members.append(df, ignore_index=True)
        group_members['group'] = group_urlname
        #print group_members
        group_members.to_csv('../data/NY_info/group_members/%s.csv' % group_urlname)


def Text2Vec(filepaths):
    from pprint import pprint
    # getting a stopword list
    path = '../data/StopWords.txt'
    with codecs.open(path, 'r', encoding='utf-8') as fr:
        content = fr.read()
        stoplist = set(content.split())

    # get a corpora
    documents = []
    for filepath in filepaths:
        with codecs.open(filepath, 'r', encoding='utf-8') as fr:
            content = fr.read()
            documents.append(get_text(str(content)))

    texts = [[word for word in document.lower().split() if
              word not in stoplist] for document in documents]
    #pprint(texts)

    dictionary = corpora.Dictionary(texts)#从texts中得到distinct,生成字典
    dictionary.save('../data/dictionary/event_description_test.dict')#保存生成的字典
    pprint(dictionary.token2id)#将得到的主题word赋予相应的数字id

    corpus = [dictionary.doc2bow(text) for text in texts] #将数据向量化doc2bow(document, allow_update=False, return_missing=False)，其实这一步生成了向量化词袋
    corpora.MmCorpus.serialize('../data/dictionary/event_description_test.mm', corpus)#加载mm文件
    pprint(corpus)

    pass


def VecApplyLDA():
    from gensim import corpora, models, similarities
    if os.path.exists('../data/dictionary/event_description_test.dict'): ##字典找不到，或者怎么生成呢？（通过上面的函数Text2Vec可以生成!）
        dictionary = corpora.Dictionary.load('../data/dictionary/event_description_test.dict')
        corpus = corpora.MmCorpus('../data/dictionary/event_description_test.mm')
        print("used files generated from test documents")
    else:
        print("No matched files found! ")

    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]#将整个corpus转为tf-idf格式

    lda = models.LdaModel(corpus_tfidf, id2word=dictionary, num_topics=3)
    corpus_lda = lda[corpus_tfidf]#LDA模型标准做法:https://www.cnblogs.com/wangqingyi/articles/5911647.html

    for doc in corpus_lda:
        print(doc)#???到底输出如    何呢？从输入开始捋，回忆实现D:\Documents\PythonCode\NLP之gensim.ipynb

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
#备忘：从注释开始，带着其中的问号，利用主函数的部分进行验证