#-*-conding:utf-8-*-
import numpy as np
from collections import defaultdict

'''读取user_tags.txt'''
user_tags_td = open("dataset/CA/test/user_tags.txt", "r")
user_tags_raw_td = defaultdict(list)
for line in user_tags_td:
    tmp_line = line.strip('\n')
    read_line = tmp_line.split(' ')#字串作为元素的列表
    user_tags_raw_td[read_line[0]] = (read_line[1:])

'''读取group_tags.txt'''
group_tags_td = open("dataset/CA/test/group_tags.txt", "r")
group_tags_raw_td = defaultdict(list)
for line in group_tags_td:
    tmp_line = line.strip('\n')
    read_line = tmp_line.split(' ')#字串作为元素的列表
    group_tags_raw_td[read_line[0]] = (read_line[1:])

'''读取user_groups.txt'''
#按理应建立59106+630=59736个节点，实际为59753,故关系建立时应避免新生节点
user_groups_td = open("dataset/CA/test/user_groups.txt", "r")
user_groups_raw_td = defaultdict(list)
for line in user_groups_td:
    tmp_line = line.strip('\n')
    read_line = tmp_line.split(' ')
    user_groups_raw_td[read_line[0]] = read_line[1:]

'''读取events.txt
   该文件可以以DataFrame形式读取，就看后面需求，暂且按照数据格式统一
'''
events_td = open("dataset/CA/test/events.txt", "r")
events_raw_td = defaultdict(list)
for line in events_td:
    tmp_line = line.strip('\n')
    read_line = tmp_line.split(' ')
    events_raw_td[read_line[0]] = read_line[1:]

#应该可以直接调用，因train数据集读入时运行过
def extract_time(raw_time):
    year = raw_time[0:4]
    month = raw_time[4:6] + '-' + raw_time[6:8]
    which_day = year + '-' + month
    what_time = raw_time[8:10] + ':' + raw_time[10:12]
    return which_day,what_time

'''将event属性中的时间进行切割处理,使原数据时间分为两列'''
events_dealt_td = defaultdict(list)
for item_e in events_raw_td:
    events_dealt_td[item_e].append(events_raw_td[item_e][0])
    which_day, what_time = extract_time(events_raw_td[item_e][1])
    events_dealt_td[item_e].append(which_day)
    events_dealt_td[item_e].append(what_time)
    events_dealt_td[item_e].append(events_raw_td[item_e][2])

'''读取event_users.txt'''
event_users_td = open("dataset/CA/test/event_users.txt", "r")
event_users_raw_td = defaultdict(list)
for line in event_users_td:
    tmp_line = line.strip('\n')
    read_line = tmp_line.split(' ')
    event_users_raw_td[read_line[0]] = read_line[1:]
