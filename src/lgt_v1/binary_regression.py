from AnalyData import *
from CreateNetwork import *
import pandas as pd
from datetime import date
import numpy as np
import copy

from src.lgt_v1.user_deal import *

'''2018/12/17 尝试一'''
# （建议用set而不是list）
u_choices = defaultdict(list)
for index, row in ueg_df.iterrows():  # 未经过preprosess_df函数
    now_u = row['user_id']
    now_e = row['event_id']
    venue = row['venue_id']
    weekday = row['weekday']
    clock = row['clock']
    choices = list(
        ueg_df[(ueg_df['venue_id'] == venue) & (ueg_df['date'] == date) & (ueg_df['clock'] == clock)]['event_id'])
    print("%s len:%d" % (now_u, len(choices)))
    for e in choices:
        if e == now_e:
            continue
        else:
            print("1")
            u_choices[now_u].append(e)

'''2018/12/17 尝试二'''
# 1. 将clock转换为clock_range
event_df['sum'] = 1
clock_count = event_df.groupby(['clock'], as_index=False)['sum'].agg({'count': np.sum})


def clock_bin(data):
    if data < '7:00':
        return 0
    elif data < '8:00':
        return 1
    elif data < '9:00':
        return 2
    elif data < '10:00':
        return 3
    elif data < '11:00':
        return 4
    elif data < '12:00':
        return 5
    elif data < '13:00':
        return 6
    elif data < '14:00':
        return 7
    elif data < '15:00':
        return 8
    elif data < '16:00':
        return 9
    elif data < '17:00':
        return 10
    elif data < '18:00':
        return 11
    elif data < '19:00':
        return 12
    elif data < '20:00':
        return 13
    elif data < '21:00':
        return 14
    elif data < '22:00':
        return 15
    else:
        return 16


event_df['clock_range'] = event_df['clock'].map(clock_bin)


# 2. 生成choices字典
def get_choices(now_e, event_df):
    now_row = event_df[event_df.event_id == now_e]
    if len(now_row) == 0:
        return []
    now_group = now_row['group_id'].values[0]
    now_venue = now_row['venue_id'].values[0]  # 下标是格式导致的取数方式
    now_weekday = now_row['weekday'].values[0]
    now_clock = now_row['clock_range'].values[0]
    valid_e = list(event_df[(event_df['group_id'] == now_group) & (event_df['venue_id'] == now_venue) & (
            event_df['weekday'] == now_weekday) & (event_df['clock_range'] == now_clock)]['event_id'])
    # valid_venue = event_df[event_df.venue_id.notnull()]
    # valid_weekday = valid_venue[valid_venue.weekday == now_weekday]
    # valid_clock = valid_weekday[valid_weekday.clock == now_clock]
    # valid_e = list(valid_clock['event_id'])
    # print("get_choices:%d" % len(valid_e))
    return valid_e


u_choices = defaultdict(list)
for u in edge_ue:
    now_u = u
    attended = list(edge_ue[u])
    choices = set()
    for e in attended:
        now_e = e
        e_choices = get_choices(now_e, event_df)
        if len(e_choices) == 0:  # 所以通过len(u_choices)可得到哪些用户无反例
            continue
        for each in e_choices:
            if each not in attended:
                choices.add(each)
    if len(choices) == 0:
        continue
    u_choices[now_u] = choices

# 3. 构造负样本集
u_info = []
e_info = []
for u in u_choices:
    allow_len = len(edge_ue[u])*1.2
    now_u = u
    cnt = 0
    for e in u_choices[u]:
        if(cnt < allow_len):
            now_e = e
            now_u_info = user_df[user_df.user_id==now_u].iloc[0,]
            now_e_info = event_df[event_df.event_id == now_e]
            u_info.append(now_u_info.values)
            e_info.append(now_e_info.values)
            cnt += 1

u_column = user_df.columns
u_df = pd.DataFrame(columns = u_column)
e_column = event_df.columns
e_df = pd.DataFrame(columns = e_column)
u_info = np.c_[list(u_info)]
e_info = np.c_[list(e_info)]
for i in range(4):
    u_df[u_df.columns[i]] = u_info[:,i]
for i in range(26):
    e_df[e_df.columns[i]] = e_info[:,i]

x = [1]
u_df.drop(u_df.columns[x], axis=1, inplace=True)
neg_ueg_df = pd.concat([u_df, e_df], axis=1)

#标识正负样本
ueg_df['class'] = 1
neg_ueg_df['class'] = 0
del ueg_df['event_id']
del neg_ueg_df['event_id']