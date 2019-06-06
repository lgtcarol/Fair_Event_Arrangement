#-*-conding:utf-8-*-
import numpy as np
from collections import defaultdict

'''本文件涉及所有外存信息读取'''

'''Part0. 变量文件读取'''
import pickle
'''train dataset'''
#原始变量
trainG_vars = open("src/ltmp_vars/trainG_vars_1221.pkl", 'rb')
user_tags_raw = pickle.load(trainG_vars)
group_tags_raw = pickle.load(trainG_vars)
events_raw = pickle.load(trainG_vars)
events_dealt = pickle.load(trainG_vars)
events_rawinfo = pickle.load(trainG_vars)
trainG_vars.close()
#graph变量
trainG_Gvars = open("src/ltmp_vars/trainG_Gvars_1221.pkl", 'rb')
trainG_U = pickle.load(trainG_Gvars)
trainG_G = pickle.load(trainG_Gvars)
trainG_E = pickle.load(trainG_Gvars)
edge_ge = pickle.load(trainG_Gvars)
edge_gu = pickle.load(trainG_Gvars)
edge_ue = pickle.load(trainG_Gvars)
edge_eu = pickle.load(trainG_Gvars)
edge_ug = pickle.load(trainG_Gvars)
trainG_Gvars.close()
#整张graph
trainG = nx.read_gpickle("src/ltmp_vars/trainG_1221.gpickle")
# trainG_redunt = open("src/trainG_redunt_1106.pkl", 'rb')
# #冗余变量
# redunt_ugu = pickle.load(trainG_redunt)
# redunt_ugg = pickle.load(trainG_redunt)
# redunt_eue = pickle.load(trainG_redunt)
# redunt_euu = pickle.load(trainG_redunt)
# trainG_redunt.close()



'''Part1. 原数据集读取'''
'''1. 读取user_tags.txt'''
user_tags = open("dataset/user_tags.txt", "r")
user_tags_raw = defaultdict(list)
for line in user_tags:
    tmp_line = line.strip('\n')
    read_line = tmp_line.split(' ')#字串作为元素的列表
    user_tags_raw[read_line[0]] = (read_line[1:])
user_tags.close()

'''2. 读取group_tags.txt'''
group_tags = open("dataset/group_tags.txt", "r")
group_tags_raw = defaultdict(list)
for line in group_tags:
    tmp_line = line.strip('\n')
    read_line = tmp_line.split(' ')#字串作为元素的列表
    group_tags_raw[read_line[0]] = (read_line[1:])
group_tags.close()


'''3. 读取user_groups.txt'''
user_groups = open("dataset/user_groups.txt", "r")
user_groups_raw = defaultdict(list)
for line in user_groups:
    tmp_line = line.strip('\n')
    read_line = tmp_line.split(' ')
    user_groups_raw[read_line[0]] = read_line[1:]
user_groups.close()

'''4. 读取events.txt
   该文件可以以DataFrame形式读取，就看后面需求，暂且按照数据格式统一
'''
events = open("dataset/events.txt", "r")
events_raw = defaultdict(list)
for line in events:
    tmp_line = line.strip('\n')
    read_line = tmp_line.split(' ')
    events_raw[read_line[0]] = read_line[1:]
events.close()
'''将event属性中的时间进行切割处理,使原数据时间分为两列'''
def extract_time(raw_time):
    year = raw_time[0:4]
    month = raw_time[4:6] + '-' + raw_time[6:8]
    which_day = year + '-' + month
    what_time = raw_time[8:10] + ':' + raw_time[10:12]
    return which_day,what_time
events_dealt = defaultdict(list)
for item_e in events_raw:
    events_dealt[item_e].append(events_raw[item_e][0]) # 地点信息
    which_day, what_time = extract_time(events_raw[item_e][1]) # 时间分割为：日期+时钟
    events_dealt[item_e].append(which_day)
    events_dealt[item_e].append(what_time)
    events_dealt[item_e].append(events_raw[item_e][2]) # 发起群组

'''5. 读取event_users.txt'''
event_users = open("dataset/event_users.txt", "r")
event_users_raw = defaultdict(list)
for line in event_users:
    tmp_line = line.strip('\n')
    read_line = tmp_line.split(' ')
    event_users_raw[read_line[0]] = read_line[1:]
event_users.close()






'''Part2. 网络对应的点集和边集的读取'''
read_users = open("dataset/trainG_users.txt", "r")
trainG_U = []
for line in read_users:
    tmp = line.strip('\n')
    trainG_U.append(tmp)
read_users.close()

read_groups = open("dataset/trainG_groups.txt", "r")
trainG_G = []
for line in read_groups:
    tmp = line.strip('\n')
    trainG_G.append(tmp)
read_groups.close()

read_events = open("dataset/trainG_events.txt", "r")
trainG_E = []
for line in read_events:
    tmp = line.strip('\n')
    trainG_E.append(tmp)
read_events.close()

def read_edeges(fpname):
    file_read = open(fpname, "r")
    edge = defaultdict(list)
    for line in file_read:
        tmp = line.strip('\n')
        read_line = tmp.split(' ')
        edge[read_line[0]] = read_line[1:]
        edge[read_line[0]].remove('')
    file_read.close()
    return edge
edge_gu = read_edeges("dataset/trainG_gu.txt")
edge_ge = read_edeges("dataset/trainG_ge.txt")
edge_ue = read_edeges("dataset/trainG_ue.txt")
edge_eu = read_edeges("dataset/trainG_eu.txt")
edge_ug = read_edeges("dataset/trainG_ug.txt")

'''11/14 为event合成tag写入txt'''
event_tags = read_edeges("dataset/event_tags.txt")