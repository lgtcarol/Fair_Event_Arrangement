# -*- coding: utf-8 -*-
# __author__ = 'lgtcarol'
from src.Save_Load_info import *

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