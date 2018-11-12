from AnalyData import *
from CreateNetwork import *
'''ATTENTION：上述导入只是为了编译检查不报错，运行时并非需要运行上两句，而是导入变量'''

class Group(object):
    def set_gnode_attr(self):
        for node in list(trainG.nodes):
            if trainG.nodes[node]['node_type'] == 'G':
                trainG.nodes[node]['num_of_u'] = len(edge_gu[node])
                trainG.nodes[node]['num_events'] = len(edge_ge[node])
                month_events = defaultdict(list)
                month_events_num = defaultdict(int)
                venue_times = defaultdict(int)
                for event in list(edge_ge[node]):
                    if (len(events_dealt[event]) == 0):
                        print('zero')
                    month = events_dealt[event][1][5:7]
                    month_events[month].append(event)
                    month_events_num[month] += 1
                    venue_times[events_dealt[event][0]] += 1
                month_events = sorted(month_events.items(), key=lambda item: item[0])
                month_events_num = sorted(month_events_num.items(), key=lambda item: item[0])
                venue_times = sorted(venue_times.items(), key=lambda item: item[1])
                trainG.nodes[node]['month_events'] = month_events
                trainG.nodes[node]['month_events_num'] = month_events_num
                trainG.nodes[node]['venue_times'] = venue_times
group = Group()
group.set_gnode_attr()

'''添加user-group权重信息：Jaccard相似度'''
#示例：'G_456'和'U_50657'
for item_g in trainG_G:
    A = set(trainG_G[item_g])
    for item_u in trainG.neighbors(item_g):
        B = set(user_tags_raw[item_u])  # 获取一个用户的tags并转为set
        numerator = A & B
        denominator = A | B
        Jaccard_score = (len(numerator) / len(denominator))*1.0
        trainG[item_u][item_g]['weight'] = round(Jaccard_score, 4)

'''将每个group的成员数保存到node属性中'''
for item_node in trainG.nodes:
    num_of_u = 0
    if trainG.nodes[item_node]['node_type'] == 'G':
        for item_u in trainG.neighbors(item_node):
            num_of_u += 1
        trainG.nodes[item_node]['num_of_u'] = num_of_u
'''将每个group中成员Jaccard_score为0.0个数保存到node属性'''
for item_dictg in group_tags_raw:
    cnt = 0
    for item_u in trainG.neighbors(item_dictg):
        if(trainG[item_u][item_dictg]['weight'] > 0.0):
            cnt += 1
    trainG.nodes[item_dictg]['cap_zero'] = trainG.nodes[item_dictg]['num_of_u'] - cnt
#《已将上述user-group子图保存到SubG_user_group.gpickle中》

'''按月份获取event数量和event列表，并添加各group的venue信息'''
month_events_num = defaultdict(int)
month_events_list = defaultdict(list)
for event in events_dealt:
    month = events_dealt[event][1][5:7]
    month_events_num[month] += 1
    month_events_list[month].append(event)
#按照月份升序排列
month_events_num = sorted(month_events_num.items(),key=lambda item:item[0])
month_events_list = sorted(month_events_list.items(),key=lambda item:item[0])

for group in group_tags_raw:
    month_groupevents_num = defaultdict(int)
    month_groupevents_list = defaultdict(list)
    group_venues = defaultdict(int)
    cnt_e = 0
    for month in month_events_list:
        for event in month_events_list[month]:
            if event in list(trainG.neighbors(group)):  # 成立前提：group和其举办的所有事件形参边
                cnt_e += 1
                month = events_dealt[event][1][5:7]
                month_groupevents_num[month] += 1
                month_groupevents_list[month].append(event)
                group_venues[events_dealt[event][0]] += 1
    month_groupevents_num = sorted(month_groupevents_num.items(), key=lambda item: item[0])
    month_groupevents_list = sorted(month_groupevents_list.items(), key=lambda item: item[0])
    group_venues = sorted(group_venues.items(), key=lambda  item: item[0])
    trainG.nodes[group]['num_of_e'] = cnt_e
    trainG.nodes[group]['month_events_num'] = month_groupevents_num
    trainG.nodes[group]['month_events_list'] = month_groupevents_list
    trainG.nodes[group]['venues'] = group_venues

'''获得event节点的user数，group_user数，other_user数'''
#由于event-user连接存在剔除，所以需要从graph上获得实际user
for event in events_dealt:
    cnt_gu = 0
    cnt_ou = 0
    group = events_dealt[event][3]
    for item in trainG.neighbors(event):
        if (item, group) in trainG.edges:
            cnt_gu += 1
        else:
            cnt_ou += 1
    trainG.nodes[event]['num_of_u'] = cnt_gu + cnt_ou
    trainG.nodes[event]['group_users'] = cnt_gu
    trainG.nodes[event]['other_users'] = cnt_ou











