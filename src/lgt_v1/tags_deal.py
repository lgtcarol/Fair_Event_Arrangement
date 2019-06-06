from collections import defaultdict
import pandas as pd

from src.LoadInfo import trainG_U, trainG_G, events_dealt
from src.CreateNetwork import trainG
from src.WirteInfo import user_tags_raw, group_tags_raw

# user's tag
utag_num = defaultdict(int)
user_tagnum = defaultdict(list)
for user in user_tags_raw:
    if user in list(trainG_U):
        user_tagnum['user_id'].append(user)
        user_tagnum['user_tagnum'].append(len(user_tags_raw[user]))
        for tag in user_tags_raw[user]:
            utag_num[tag] += 1
data = defaultdict(list)
data['utag_id'] = list(utag_num.keys())
data['uused_num'] = list(utag_num.values())
utag_df = pd.DataFrame(data) # 各tag被user的使用频率
user_tagnum_df = pd.DataFrame(user_tagnum)

# origin group's tag
gtag_num = defaultdict(int)
group_tagnum = defaultdict(list)
for group in group_tags_raw:
    if group in list(trainG_G):
        group_tagnum['group_id'].append( group)
        group_tagnum['group_tagnum'].append(len(group_tags_raw[group]))
        for tag in group_tags_raw[group]:
            gtag_num[tag] += 1
data = defaultdict(list)
data['gtag_id'] = list(gtag_num.keys())
data['gused_num'] = list(gtag_num.values())
gtag_df = pd.DataFrame(data)
group_tagnum_df = pd.DataFrame(group_tagnum)
intsec = set(utag_df['utag_id']) & set(gtag_df['gtag_id'])
difsec = set(utag_df['utag_id']) | set(gtag_df['gtag_id'])


# rich group's tag
def enrich_gtags():
    e_tags = defaultdict(list)
    g_tags = defaultdict(list)
    # group标签初始化
    for node in list(trainG.nodes):
        if trainG.nodes[node]['node_type'] == 'G':
            g_tags[node] = group_tags_raw[node]
    for node in list(trainG.nodes):
        if trainG.nodes[node]['node_type'] == 'E':
            groupu_tags = defaultdict(int)
            otheru_tags = defaultdict(int)
            for item in trainG.nodes[node]['group_u']:  # 遍历成员
                for tag in user_tags_raw[item]:  # 遍历并标记成员tag
                    groupu_tags[tag] += 1.0
            for item_other in trainG.nodes[node]['other_u']:
                for tag_other in user_tags_raw[item_other]:
                    otheru_tags[tag_other] += 1.0
            # 选择融入
            for tag_g in groupu_tags:
                if groupu_tags[tag_g] >= 0.2 * trainG.nodes[node]['num_group_u']:
                    e_tags[node].append(tag_g)

            num_other_u = trainG.nodes[node]['num_of_u'] - trainG.nodes[node]['num_group_u']
            for tag_o in otheru_tags:
                if otheru_tags[tag_o] >= 0.1 * num_other_u:
                    e_tags[node].append(tag_o)
            which_group = events_dealt[node][3]
            if which_group in g_tags.keys():
                g_tags[which_group] = set(g_tags[which_group]) | set(e_tags[node])
    return g_tags


richgroup_tags = enrich_gtags()
rgtag_num = defaultdict(int)
rgroup_tagnum = defaultdict(list)
for group in richgroup_tags:
    if group in list(trainG_G):
        rgroup_tagnum['rgroup_id'].append(group)
        rgroup_tagnum['rgroup_tagnum'].append(len(richgroup_tags[group]))
        for tag in richgroup_tags[group]:
            rgtag_num[tag] += 1
data = defaultdict(list)
data['rgtag_id'] = list(rgtag_num.keys())
data['rgused_num'] = list(rgtag_num.values())
rgtag_df = pd.DataFrame(data)
rgroup_tagnum_df = pd.DataFrame(rgroup_tagnum)
intsec2 = set(utag_df['utag_id']) & set(rgtag_df['rgtag_id'])
difsec2 = set(utag_df['utag_id']) | set(rgtag_df['rgtag_id'])