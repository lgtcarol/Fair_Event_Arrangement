from AnalyData import *
from CreateNetwork import *
from AnalyData_test import *
from CreateNetwork_test import *

'''user相交情况'''
# 42443 & 34479 = 34479 （有7964个新用户）
user_set = set(user_tags_raw.keys())
user_tset = set(user_tags_raw_td.keys())
cap_user = user_set & user_tset


'''group相交情况'''
# 630 & 526 = 526 （有4个group在测试集中没有）
group_set = set(group_tags_raw.keys())
group_tset = set(group_tags_raw_td.keys())
cap_group = group_set & group_tset


'''event相交情况'''
# 15588 & 2725 = 0
event_set = set(events_dealt.keys())
event_tset = set(events_dealt_td.keys())
cap_event = event_set & event_tset

'''冗余个体相互关系'''
# train: u_g为16679和1   e_u为   0和17546 （可分别减少）0和0     0和0
# test:  u_g为3364和66   e_u为1076和6738              358和65  0和1876
'''分析：
   由于test_user是train_user的子集，故train_user未匹配的在test上也不会得到个体info而利用上,redunt_ugu没用
   而test_user未匹配的在train上可能获得相应user的个体info: supplement_user = set(redundant_ugu) & user_set 得到358条信息可能能用，前提是group存在.
   (如果是本着扩充数据信息，不妨将train,test节点信息分别求并，然后再建立e-u,u-g关系即可充分利用所有知道info的对象。
   但现在是想看压根跟平台（train|test）没关联的节点大概什么情况)
   train_group的关系同上，supplement_group = set(redundant_ugg) & group_set 得到test冗余信息中的65个group是平台存在的
   
   train e_u中冗余的user同样不可能在testG中存在，因后者的user是前者user子集
   test e_u中冗余的event不可能在trainG中，因事件举办事件限制
   test e_u中同于的user可能在trainG中，supplement2_user = set(redundant_euu) & user_set得到testG冗余中的1876个user在trainG中 
   
   总之，testG中冗余的连边信息可通过trainG减少，但反过来不行。
'''


'''测试图中各类节点个数'''
node_u = 0
node_g = 0
node_e = 0
for node in trainG.nodes():
    if trainG.nodes[node]['node_type'] == 'U':
        node_u += 1
    elif trainG.nodes[node]['node_type'] == 'G':
        node_g += 1
    elif trainG.nodes[node]['node_type'] == 'E':
        node_e += 1
    else:
        continue

'''测试图中各类连边数目'''
#group-user和group-event
edge_gu = 0
edge_ge = 0
for g in trainG.nodes():
    if trainG.nodes[g]['node_type'] == 'G':
        for item in trainG.neighbors(g):
            if trainG.nodes[item]['node_type'] == 'U':
                edge_gu += 1
            elif trainG.nodes[item]['node_type'] == 'E':
                edge_ge += 1
            else:
                continue
#event-user
edge_eu = 0
for e in trainG.nodes():
    if trainG.nodes[e]['node_type'] == 'E':
        for u in trainG.neighbors(e):
            if trainG.nodes[u]['node_type'] == 'U':
                edge_eu += 1




