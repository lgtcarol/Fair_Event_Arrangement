#-*-conding:utf-8-*-
import numpy as np
from collections import defaultdict

'''本文件涉及所有文件信息读取'''

'''读取user_tags.txt'''
user_tags = open("dataset/user_tags.txt", "r")
user_tags_raw = defaultdict(list)
for line in user_tags:
    tmp_line = line.strip('\n')
    read_line = tmp_line.split(' ')#字串作为元素的列表
    user_tags_raw[read_line[0]] = (read_line[1:])
user_tags.close()

'''读取group_tags.txt'''
group_tags = open("dataset/group_tags.txt", "r")
group_tags_raw = defaultdict(list)
for line in group_tags:
    tmp_line = line.strip('\n')
    read_line = tmp_line.split(' ')#字串作为元素的列表
    group_tags_raw[read_line[0]] = (read_line[1:])
group_tags.close()

'''读取user_groups.txt'''
user_groups = open("dataset/user_groups.txt", "r")
user_groups_raw = defaultdict(list)
for line in user_groups:
    tmp_line = line.strip('\n')
    read_line = tmp_line.split(' ')
    user_groups_raw[read_line[0]] = read_line[1:]
user_groups.close()

'''读取events.txt
   该文件可以以DataFrame形式读取，就看后面需求，暂且按照数据格式统一
'''
events = open("dataset/events.txt", "r")
events_raw = defaultdict(list)
for line in events:
    tmp_line = line.strip('\n')
    read_line = tmp_line.split(' ')
    events_raw[read_line[0]] = read_line[1:]
events.close()

def extract_time(raw_time):
    year = raw_time[0:4]
    month = raw_time[4:6] + '-' + raw_time[6:8]
    which_day = year + '-' + month
    what_time = raw_time[8:10] + ':' + raw_time[10:12]
    return which_day,what_time

'''将event属性中的时间进行切割处理,使原数据时间分为两列'''
events_dealt = defaultdict(list)
for item_e in events_raw:
    events_dealt[item_e].append(events_raw[item_e][0])
    which_day, what_time = extract_time(events_raw[item_e][1])
    events_dealt[item_e].append(which_day)
    events_dealt[item_e].append(what_time)
    events_dealt[item_e].append(events_raw[item_e][2])

'''读取event_users.txt'''
event_users = open("dataset/event_users.txt", "r")
event_users_raw = defaultdict(list)
for line in event_users:
    tmp_line = line.strip('\n')
    read_line = tmp_line.split(' ')
    event_users_raw[read_line[0]] = read_line[1:]
event_users.close()

'''11/12 读取实际的节点连边信息'''

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

read_ge = open("dataset/trainG_ge.txt", "r")
edge_ge = defaultdict(list)
for line in read_ge:
    tmp = line.strip('\n')
    read_line = tmp.split(' ')
    edge_ge[read_line[0]] = read_line[1:]
    edge_ge[read_line[0]].remove('')#由于写入时末尾多个空格，导致文末会写入一个空，然后都出来也会有一个空
read_ge.close()

read_gu = open("dataset/trainG_gu.txt", "r")
edge_gu = defaultdict(list)
for line in read_gu:
    tmp = line.strip('\n')
    read_line = tmp.split(' ')
    edge_gu[read_line[0]] = read_line[1:]
    edge_gu[read_line[0]].remove('')
read_gu.close()

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