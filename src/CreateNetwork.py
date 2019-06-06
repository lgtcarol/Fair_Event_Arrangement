from AnalyData import *
import networkx as nx

trainG = nx.Graph()
'''添加user节点'''
# 3th
for item in user_tags_raw:
    trainG.add_node(item)
    trainG.nodes[item]['node_type'] = 'U'

'''添加group节点'''
for item in group_tags_raw:
    trainG.add_node(item)
    trainG.nodes[item]['node_type'] = 'G'

'''添加event节点'''
for item in events_dealt:
    trainG.add_node(item)
    trainG.nodes[item]['node_type'] = 'E'
    trainG.nodes[item]['which_day'] = events_dealt[item][1]
    trainG.nodes[item]['what_time'] = events_dealt[item][2]

'''添加user-group连边信息'''
redunt_ugu = set()
redunt_ugg = set()
for item_u in user_groups_raw:
    for item_g in user_groups_raw[item_u]:
        if (item_u in user_tags_raw) and (item_g in group_tags_raw):
            trainG.add_edge(item_u, item_g)
        elif (item_u not in user_tags_raw):
            redunt_ugu.add(item_u)
        else:
            redunt_ugg.add(item_g)


'''添加event-group连边信息'''
#debug:竟然因为不熟悉返回值类型和错用工作空间已有的变量item导致出现逻辑错误
#debug：每步的结果验证还是很重要的，不然在其他步再定位过来确实繁琐
# redundant_g = [] 没有出现多余的group
for item_e in events_dealt:
    if events_dealt[item_e][3] in list(trainG.nodes):
        trainG.add_edge(item_e, events_dealt[item_e][3])

'''建立event-users连边信息'''
#发现冗余的连边信息都是因为确实user信息导致
#!!此处要用set,不然得到大量的冗余user（63728），实际是17546个多余用户
redunt_eue = set()
redunt_euu = set()
for item_e in event_users_raw:
    for item_u in event_users_raw[item_e]:
        if (item_u in user_tags_raw) and (item_e in events_dealt):
            trainG.add_edge(item_e, item_u)
        elif (item_u not in user_tags_raw):
            redunt_euu.add(item_u)
        else:
            redunt_eue.add(item_e)

'''统计删除没有user的group和其发起过的event'''
empty_group = [] #23个
for node in list(trainG.nodes):
    if trainG.nodes[node]['node_type']=='G' and trainG.nodes[node]['num_of_u'] == 0:
        empty_group.append(node)
# group节点删除
for g in empty_group:
    if g in trainG.nodes():
        trainG.remove_node(g)
empty_event = []#831
for node in empty_group:
    for item in trainG.neighbors(node):
        if trainG.nodes[item]['node_type'] == 'E':
            empty_event.append(item)

# event节点删除
for e in empty_event:
    if e in trainG.nodes():
        trainG.remove_node(e)
'''没有event的group统计和（没有user的group已经处理过近23例）'''
NA_event_group = [] #0
for x in list(trainG.nodes):
    if trainG.nodes[x]['node_type'] == 'G':
        has_event = False
        for y in list(trainG.neighbors(x)):
            if trainG.nodes[y]['node_type'] == 'E':
                has_event = True
                break
        if has_event == False:
            NA_event_group.append(x)

'''插曲: 发现存在没有user参加的event'''
# 逻辑漏洞在于：原文件中该事件虽然有参与user全都不在trainG
edges_eu = defaultdict(list)
for e in list(trainG.nodes()):
    if trainG.nodes[e]['node_type'] == 'E':
        for u in trainG.neighbors(e):
            if trainG.nodes[u]['node_type'] == 'U':
                edges_eu[e].append(u)

#没有user的event和(没有group的event不存在因为原数据文件events.txt保证了event-group的对应，能添加到trainG上的边也保证了对应关系)
#并统计发现len(NA_event_group) = 0
'''统计删除没有user的event和没有group的event'''
NA_user_event = [] #19
NA_group_event = [] #0
for x in list(trainG.nodes):
    if trainG.nodes[x]['node_type'] == 'E':
        has_user = False
        has_group = False
        for y in list(trainG.neighbors(x)):
            if trainG.nodes[y]['node_type'] == 'U':
                has_user = True
                continue
            if trainG.nodes[y]['node_type'] == 'G':
                has_group = True
                continue
            if(has_user and has_group):
                break
        if has_user == False:
            NA_user_event.append(x)
        if has_group == False:
            NA_group_event.append(x)

for ex in NA_user_event:
    if ex in trainG.nodes():
        trainG.remove_node(ex)

'''统计删除没有event的user和没有group的user'''
NA_event_user = [] #仅仅是统计, 4110
NA_group_user = [] #不允许, 2228
for x in list(trainG.nodes):
    if trainG.nodes[x]['node_type'] == 'U':
        has_event = False
        has_group = False
        for y in list(trainG.neighbors(x)):
            if trainG.nodes[y]['node_type'] == 'E':
                has_event = True
                continue
            if trainG.nodes[y]['node_type'] == 'G':
                has_group = True
                continue
            if(has_event and has_group):
                break
        if has_event == False:
            NA_event_user.append(x)
        if has_group == False:
            NA_group_user.append(x)
NA_evtgrp_user = set(NA_event_user) & set(NA_group_user) #2204
for u in NA_group_user:
    if u in trainG.nodes():
        trainG.remove_node(u)

