#-*-conding:utf-8-*-
#dict这个数据结构由于hash的特性，是无序的，这在有的时候会给我们带来一些麻烦， 幸运的是，collections模块为我们提供了OrderedDict，当你要获得一个有序的字典对象时，用它就对了。
#默认字典：defaultdict的参数默认是dict，也可以为list,tuple
#https://blog.csdn.net/IqqIqqIqqIqq/article/details/52734178解释了默认字典之默认用处

#先尝试直接读取，发现为List
#然后放入defaultdict，原因是每行的第一项确实相当于字典的key一样，后面的list可看作defaultdict的value值，而且不用担心原数据集万一同个用户对应两行的去重合并问题
from collections import defaultdict

import numpy as np
from Feature_Extract import *

user_tags = open("dataset/user_tags.txt", "r")
user_tags_raw = []
for line in user_tags:
    tmp_line = line.strip('\n')
    read_line = tmp_line.split(' ')#字串作为元素的列表
    user_tags_raw.append(read_line)

#如何读取defaultdict中的元素，以key,value形式
group_tags = open("dataset/group_tags.txt", "r")
group_tags_raw = defaultdict(list)
for line in group_tags:
    tmp_line = line.strip('\n')
    read_line = tmp_line.split(' ')#字串作为元素的列表
    group_tags_raw[read_line[0]] = (read_line[1:])
for x in group_tags_raw:
    print(group_tags_raw[x])

#获取defaultdict的key值：user_tags_raw.keys(),list(user_tags_raw.keys())将其转为列表
#-------------Draft_CreateNetwork------------------
import networkx as nx
G = nx.Graph()
'''添加user节点'''
#1st
for item in user_tags_raw:
    G.add_nodes_from(item)
#2st
user_list = []
for item in user_tags_raw:
    user_list.append(item)
    G.add_node(user_list)

nx.draw(G, with_labels=True, font_weight='bold')
'''为user-group计算权重'''
A= set(group_tags_raw['G_456']) #获得g的tags,并从list转为set类型
G.neighbors('G_56') #1184个用户
G.neighbors('G_456') #419个用户,有个用户是U_50657


'''Jaccard系数作为边权值有些欠佳'''
neighbor = []
for x in nx.neighbors(G,'G_456'):
    neighbor.append(x)
weight_nzero = 0
for x in neighbor:
    if G['G_456'][x]['weight'] > 0.0000:
        weight_nzero += 1
#len(neighbor)=419,weight_nzero=186

#-----------------熟悉graph的信息---------------------
G.get_edge_data(0, 1) #两节点连边信息
G.has_node(n) #是否有该节点
G.has_edge(u, v) #有连边信息
G.neighbors(n) #某节点邻居
G['G_415']['U_23364'] #两点间连边信息
G.nodes['G_415'] #节点信息
G.nodes['G_415']['num_of_u'] #访问节点规模
G.nodes.data() #获取图中的节点信息和值

#按照边去遍历整张图
for e in list(G.edges):
    print(G.edges[e]['weight'])
#保存和载入图
nx.write_gpickle(G,"SubG_user_group.gpickle")
import networkx as nx
G = nx.read_gpickle("SubG_user_group.gpickle")

'''常规变量保存到文件中'''
#导入pickle包，变量相继存入文件，顺序读出变量
import pickle
pickle.dump() #不加s的和文件读写相关
pickle.load()

#----------------Draw Graph---------------------------
import matplotlib.pyplot as plt
plt.subplots(2, 2, figsize=(15, 6))

# 返回Zachary的空手道俱乐部图。
G.clear()
G = nx.karate_club_graph()
plt.subplot(1, 2, 1)
nx.draw(G, with_labels=True)
plt.title('karate_club_graph')
plt.axis('on')
plt.xticks([])
plt.yticks([])

# 戴维斯南方女性社交网络。
G.clear()
G = nx.davis_southern_women_graph()
plt.subplot(1, 2, 2)
nx.draw(G, with_labels=True)
plt.title('davis_southern_women_graph')
plt.axis('on')
plt.xticks([])
plt.yticks([])

plt.show()
round(G['G_456']['U_50657']['weight'],2)

'''11/12 测试debug'''
from Save_Load_info import *
i= 0
for u in trainG.nodes():
    if trainG.nodes[u]['node_type'] == 'U':
        flag = False
        for e in trainG.neighbors(u):
            if trainG.nodes[e]['node_type'] == 'E':
                flag = True
                break
        if flag == False:
            i += 1

'''11/14 一些统计'''

t = 0
for i in repeat_v:
    if i > 0.5:
        t += 1

t = 0
num_gu = 0
for g in list(trainG.nodes()):
    if trainG.nodes[g]['node_type'] == 'G':
        for item in list(trainG.neighbors(g)):
            if trainG.nodes[item]['node_type'] == 'U' :
                num_gu += 1
                if trainG[g][item]['weight']>0:
                    t += 1






