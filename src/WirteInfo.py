'''
trainG_vars = open("src/trainG_vars_1106.pkl", 'wb')
pickle.dump(user_tags_raw, trainG_vars,True)
pickle.dump(group_tags_raw, trainG_vars,True)
pickle.dump(user_groups_raw, trainG_vars,True)
pickle.dump(events_raw, trainG_vars,True)
pickle.dump(events_dealt, trainG_vars,True)
pickle.dump(event_users_raw, trainG_vars,True)
trainG_vars.close()

trainG_vars = open("src/trainG_Gvars_1113.pkl", 'wb')
pickle.dump(trainG_U, trainG_vars,True)
pickle.dump(trainG_G, trainG_vars,True)
pickle.dump(trainG_E, trainG_vars,True)
pickle.dump(edge_ge, trainG_vars,True)
pickle.dump(edge_gu, trainG_vars,True)
pickle.dump(edge_ue, trainG_vars,True)
pickle.dump(edge_eu, trainG_vars,True)
pickle.dump(edge_ug, trainG_vars,True)
trainG_vars.close()

ueg_sample_onehot.to_csv("src/ltmp_vars/ueg_sample_onehot.csv", encoding="utf-8")

nx.write_gpickle(trainG,"src/trainG_1106.gpickle")
trainG_redunt = open("src/trainG_redunt_1106.pkl", 'wb')
pickle.dump(redunt_ugu, trainG_redunt, True)
pickle.dump(redunt_ugg, trainG_redunt, True)
pickle.dump(redunt_eue, trainG_redunt, True)
pickle.dump(redunt_euu, trainG_redunt, True)
trainG_redunt.close()

《AnalyData_test.py》中完成文件信息读入内存变量，下面为变量固化到文件的操作过程
testG_vars = open("src/testG_vars_1106.pkl", 'wb')
pickle.dump(user_tags_raw_td, testG_vars,True)
pickle.dump(group_tags_raw_td, testG_vars,True)
pickle.dump(user_groups_raw_td, testG_vars,True)
pickle.dump(events_raw_td, testG_vars,True)
pickle.dump(events_dealt_td, testG_vars,True)
pickle.dump(event_users_raw_td, testG_vars,True)
testG_vars.close()

df_var = open('src/ltmp_vars/uegdf_var.pkl', 'wb')
pickle.dump(zip_event_df, df_var, True)
pickle.dump(group_df, df_var, True)
pickle.dump(ueg_df, df_var,True)
df_var.close()

《CreateNetwork.py》中完成网络的建立，下面为将其固话到文件
nx.write_gpickle(testG,"testG_1106.gpickle")

《冗余信息》
testG_redundant = open("src/testG_redundant_1106.pkl", 'wb')
pickle.dump(redundant_ugu, testG_redundant, True)
pickle.dump(redundant_ugg, testG_redundant, True)
pickle.dump(redundant_eue, testG_redundant, True)
pickle.dump(redundant_euu, testG_redundant, True)
testG_redundant.close()
'''

import pickle
import networkx as nx
import pandas as pd
import numpy as np
from collections import defaultdict
from datetime import date
import copy
from Feature_Extract import *

'''write到外存'''

'''将真实存在于图中的节点和边保存到txt文件中'''
from collections import defaultdict
# 1. 节点集
trainG_U = []
trainG_G = []
trainG_E = []
for node in trainG.nodes():
    if trainG.nodes[node]['node_type'] == 'U':
        trainG_U.append(node)
    elif trainG.nodes[node]['node_type'] == 'G':
        trainG_G.append(node)
    elif trainG.nodes[node]['node_type'] == 'E':
        trainG_E.append(node)
    else:
        continue
out_u = open("dataset/trainG_users.txt","w")
for user in trainG_U:
    out_u.write(user)
    out_u.write('\n')
out_u.close()

out_g = open("dataset/trainG_groups.txt","w")
for group in trainG_G:
    out_g.write(group)
    out_g.write('\n')
out_g.close()

out_e = open("dataset/trainG_events.txt", "w")
for event in trainG_E:
    out_e.write(event)
    out_e.write('\n')
out_e.close()

# 2. 边集
#edge_gu, edge_ge
edge_gu = defaultdict(list)
edge_ge = defaultdict(list)
for g in list(trainG.nodes()):
    if trainG.nodes[g]['node_type'] == 'G':
        for item in list(trainG.neighbors(g)):
            if trainG.nodes[item]['node_type'] == 'U':
                edge_gu[g].append(item)
            elif trainG.nodes[item]['node_type'] == 'E':
                edge_ge[g].append(item)
            else:
                continue
u = defaultdict(list)
for e in trainG.nodes():
    if trainG.nodes[e]['node_type'] == 'E':
        for u in trainG.neighbors(e):
            if trainG.nodes[u]['node_type'] == 'U':
                edge_eu[e].append(u)
#edge_ue,edge_ug
edge_ue = defaultdict(list) #发现有1906个用户没有参加一个event
edge_ug = defaultdict(list)
for u in trainG.nodes():
    if trainG.nodes[u]['node_type'] == 'U':
        for item in trainG.neighbors(u):
            if trainG.nodes[item]['node_type'] == 'E':
                edge_ue[u].append(item)
            elif trainG.nodes[item]['node_type'] == 'G':
                edge_ug[u].append(item)
            else:
                continue
out_gu = open("dataset/trainG_gu.txt", "w")  # 1
for group in edge_gu:
    out_gu.write(group)
    out_gu.write(' ')
    for user in edge_gu[group]:
        out_gu.write(user)
        out_gu.write(' ')
    out_gu.write('\n')
out_gu.close()

out_ge = open("dataset/trainG_ge.txt", "w")  # 2
for group in edge_ge:
    out_ge.write(group)
    out_ge.write(' ')
    for event in edge_ge[group]:
        out_ge.write(event)
        out_ge.write(' ')
    out_ge.write('\n')
out_ge.close()

out_eu = open("dataset/trainG_eu.txt", "w")  # 3
for event in edge_eu:
    out_eu.write(event)
    out_eu.write(' ')
    for user in edge_eu[event]:
        out_eu.write(user)
        out_eu.write(' ')
    out_eu.write('\n')
out_eu.close()

def save_edeges(fpname, edges_var):
    out = open(fpname, "w")
    for ox in edges_var:
        out.write(ox)
        out.write(' ')
        for oy in edges_var[ox]:
            out.write(oy)
            out.write(' ')
        out.write('\n')
    out.close()
save_edeges("dataset/trainG_ue.txt", edge_ue)  # 4
save_edeges("dataset/trainG_ug.txt", edge_ug)  # 5

# 群组标签丰富结果，思路见
# save_edeges("dataset/rich_gtags.txt", rich_gtags)
































'''test dataset'''
trainG_vars = open("src/testG_vars_1106.pkl", 'rb')
user_tags_raw_td = pickle.load(trainG_vars)
group_tags_raw_td = pickle.load(trainG_vars)
user_groups_raw_td = pickle.load(trainG_vars)
events_raw_td = pickle.load(trainG_vars)
events_dealt_td = pickle.load(trainG_vars)
event_users_raw_td = pickle.load(trainG_vars)
trainG_vars.close()
testG = nx.read_gpickle("src/testG_1106.gpickle")
testG_redundant = open("src/testG_redundant_1106.pkl", 'rb')
redundant_ugu = pickle.load(testG_redundant)
redundant_ugg = pickle.load(testG_redundant)
redundant_eue = pickle.load(testG_redundant)
redundant_euu = pickle.load(testG_redundant)
testG_redundant.close()

'''图运算尝试'''
subG = nx.read_gpickle("src/SubG_user_group.gpickle")
testG = nx.subgraph(trainG, list(events_dealt.keys()))

'''2018/11/9新增变量'''
#trainG表示在train数据集上的操作，var则显然不是图上的变量，图上的变量会直接作用到图
# trainG_vars_1109 = open("src/trainG_vars_1109.pkl", 'wb')
# pickle.dump(month_events_num, trainG_vars_1109, True)
# pickle.dump(month_events_list,trainG_vars_1109, True)
# trainG_vars_1109.close()
