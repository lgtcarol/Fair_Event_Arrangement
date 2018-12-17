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
    if data < '10:00':
        return 0
    elif data < '14:00':
        return 1
    elif data < '18:00':
        return 2
    elif data < '20:00':
        return 3
    else:
        return 4


event_df['clock_range'] = event_df['clock'].map(clock_bin)

# 2. 生成choices字典
def get_choices(now_e, event_df):
    now_row = event_df[event_df.event_id == now_e]
    if len(now_row) == 0:
        return []
    now_venue = now_row['venue_id'].values[0] #下标是格式导致的取数方式
    now_weekday = now_row['weekday'].values[0]
    now_clock = now_row['clock_range'].values[0]
    valid_e = list(event_df[(event_df['venue_id'] == now_venue) & (event_df['weekday'] == now_weekday) & (event_df['clock_range'] == now_clock)]['event_id'])
    # valid_venue = event_df[event_df.venue_id.notnull()]
    # valid_weekday = valid_venue[valid_venue.weekday == now_weekday]
    # valid_clock = valid_weekday[valid_weekday.clock == now_clock]
    #valid_e = list(valid_clock['event_id'])
    #print("get_choices:%d" % len(valid_e))
    return valid_e

u_choices = defaultdict(list)
i = 0
for u in edge_ue:
    if i < 10:
        now_u = u
        attended = list(edge_ue[u])
        choices = set()
        for e in attended:
            now_e = e
            e_choices = get_choices(now_e, event_df)
            if len(e_choices)==0:#所以通过len(u_choices)可得到哪些用户无反例
                continue
            for each in e_choices:
                if each not in attended:
                    choices.add(each)
        if len(choices) == 0:
            continue
        print("outer_circle:%d" % len(choices))
        u_choices[now_u]=choices
        i+=1



