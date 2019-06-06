# -*- coding: utf-8 -*-
# __author__ = 'lgtcarol'
from src.WirteInfo import *

# 1. events_dealt删掉多余的并存为trainG_events.csv
del_events = set(list(events_dealt.keys())) - set(trainG_E)
data = defaultdict(list)
event_id = []  # 作为索引在遍历节点时依次获得
venue_id = []
date_time = []
clock_time = []
e_group = []
for event in list(trainG_E):
    event_id.append(event)
    venue_id.append(events_dealt[event][0])
    date_time.append(events_dealt[event][1])
    clock_time.append(events_dealt[event][2])
    e_group.append(events_dealt[event][3])
data['event_id'] = event_id
data['group_id'] = e_group
data['venue_id'] = venue_id
data['date'] = date_time
data['clock'] = clock_time
events_rawinfo = pd.DataFrame(data)

# 2. 修改图中‘G_304’连边信息
real_e = edge_ge['G_304']
neigh_e = copy.copy(list(trainG.neighbors('G_304')))
for node in neigh_e:
    if trainG.nodes[node]['node_type'] == 'E':
        if node not in real_e:
            trainG.remove_edge('G_304',node)

'''添加user-group权重信息：Jaccard相似度'''
#示例：'G_456'和'U_50657'
for item_g in trainG_G:
    A = set(group_tags_raw[item_g])
    for item_u in trainG.neighbors(item_g):
        if trainG.nodes[item_u]['node_type'] == 'U':
            B = set(user_tags_raw[item_u])  # 获取一个用户的tags并转为set
            numerator = A & B
            denominator = A | B
            Jaccard_score = (len(numerator) / len(denominator))*1.0
            trainG[item_u][item_g]['weight'] = round(Jaccard_score, 3)


'''将每个group中成员Jaccard_score为0.0个数保存到node属性'''
for item_dictg in group_tags_raw:
    cnt = 0
    for item_u in trainG.neighbors(item_dictg):
        if(trainG[item_u][item_dictg]['weight'] > 0.0):
            cnt += 1
    trainG.nodes[item_dictg]['cap_zero'] = trainG.nodes[item_dictg]['num_of_u'] - cnt

