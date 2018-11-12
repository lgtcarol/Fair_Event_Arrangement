from AnalyData_test import *
import networkx as nx

testG = nx.Graph()
'''添加user节点'''
for item in user_tags_raw_td:
    testG.add_node(item)
    testG.nodes[item]['node_type'] = 'U'

'''添加group节点'''
for item in group_tags_raw_td:
    testG.add_node(item)
    testG.nodes[item]['node_type'] = 'G'

'''添加user-group连边信息'''
# redundant_ug = [] 冗余的关系有9007
# 缺少tag信息的user和group个数分别是3364和66
redundant_ugu = set()
redundant_ugg = set()
for item_u in user_groups_raw_td:
    for item_g in user_groups_raw_td[item_u]:
        if (item_u in user_tags_raw_td) and (item_g in group_tags_raw_td):
            testG.add_edge(item_u, item_g)
        elif (item_u not in user_tags_raw_td):
            redundant_ugu.add(item_u)
        else:
            redundant_ugg.add(item_g)

'''添加user-group权重信息：Jaccard相似度'''
#示例：'G_456'和'U_50657'
for item_g in group_tags_raw_td:
    A = set(group_tags_raw_td[item_g])
    for item_u in testG.neighbors(item_g):
        B = set(user_tags_raw_td[item_u])  # 获取一个用户的tags并转为set
        numerator = A & B
        denominator = A | B
        Jaccard_score = (len(numerator) / len(denominator))*1.0
        testG[item_u][item_g]['weight'] = round(Jaccard_score, 4)

'''将每个group的成员数保存到node属性中'''
for item_node in testG.nodes:
    num_of_u = 0
    if testG.nodes[item_node]['node_type'] == 'G':
        for item_u in testG.neighbors(item_node):
            num_of_u += 1
        testG.nodes[item_node]['num_of_u'] = num_of_u
'''将每个group中成员Jaccard_score为0.0个数保存到node属性'''
for item_dictg in group_tags_raw_td:
    cnt = 0
    for item_u in testG.neighbors(item_dictg):
        if(testG[item_u][item_dictg]['weight'] > 0.0):
            cnt += 1
    testG.nodes[item_dictg]['cap_zero'] = testG.nodes[item_dictg]['num_of_u'] - cnt
#《已将上述user-group子图保存到SubG_user_group.gpickle中》

'''添加event节点'''
for item in events_dealt_td:
    testG.add_node(item)
    testG.nodes[item]['node_type'] = 'E'
    testG.nodes[item]['which_day'] = events_dealt_td[item][1]
    testG.nodes[item]['what_time'] = events_dealt_td[item][2]

'''添加event-group连边信息'''
# redundant_egg = set() 没有出现多余的group
for item_e in events_dealt_td:
    if events_dealt_td[item][3] in testG.nodes:
        testG.add_edge(item_e, events_dealt_td[item][3])


'''建立event-users连边信息'''
#发现冗余的连边信息都是因为确实user信息导致
#!!此处要用set,不然得到大量的冗余user（63728），实际是17546个多余用户
redundant_eue = set()
redundant_euu = set()
for item_e in event_users_raw_td:
    for item_u in event_users_raw_td[item_e]:
        if (item_u in user_tags_raw_td) and (item_e in events_dealt_td):
            testG.add_edge(item_e, item_u)
        elif (item_u not in user_tags_raw_td):
            redundant_euu.add(item_u)
        else:
            redundant_eue.add(item_e)




