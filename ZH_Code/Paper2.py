#coding=utf-8
from collections import defaultdict
import random
"一个的事件时间安排算法的小程序，用于对模拟到来事件时间安排以达到最大用户参与度"
alpha = 0.5 #权重因子
def myp(a):
    for i in a:
        print (i)
        print (a[i])
day_events = defaultdict(list)
infile = open("day_events.txt","r")
for line in infile:
    p = line.split()
    day_events[p[0]] = p[1:]
infile.close()
#模拟事件随机到来：随机打乱
for each in day_events:
    random.shuffle(day_events[each])
eventsList = []
events_timeprefer = defaultdict(list)#事件对时间偏好概率的降序排列
events_done = []#已经分配完事件
events_come = []#未分配事件
userconflict_graph = defaultdict(dict)#事件用户冲突图，格式：event1：event2：weight
current_UCG = defaultdict(dict)
time_eventassignment = defaultdict(list)
heuristic_information = {}
#alg begins here
def UpdateUserConflictGraph(ed,e,cucg):
    for i in ed:
        if userconflict_graph[e].has_key(i):
            cucg[i][e] = userconflict_graph[e][i]
            cucg[e][i] = userconflict_graph[e][i]
    return cucg
for each in eventsList:
    events_come.remove(each)
    events_done.append(each)
    # 建立当前事件用户冲突图
    UpdateUserConflictGraph(events_done,each,current_UCG)
    tdone = -1
    cumin = 10000
    for i in events_timeprefer[each]:
        kk = 0
        tconflictstrat = i - 3
        tconflictend = i + 3
        if tconflictstrat < 0:
            tconflictstrat = 0
        if tconflictend > 23:
            tconflictend = 23
        for j in range(tconflictstrat,tconflictend):
            for k in time_eventassignment[j]:
                if current_UCG[each].has_key(k):
                    kk += current_UCG[each][k]
        if kk < cumin:
            tdone = i
    time_eventassignment[tdone].append(each)
def heuristic():
    for each in eventsList:
        events_come.remove(each)
        events_done.append(each)
        # 建立当前事件用户冲突图
        UpdateUserConflictGraph(events_done, each, current_UCG)
        tdone = -1
        cumin = 10000
        for i in events_timeprefer[each]:
            kk = 0
            tconflictstrat = i - 3
            tconflictend = i + 3
            if tconflictstrat < 0:
                tconflictstrat = 0
            if tconflictend > 23:
                tconflictend = 23
            for j in range(tconflictstrat, tconflictend):
                for k in time_eventassignment[j]:
                    if current_UCG[each].has_key(k):
                        kk += current_UCG[each][k]
            kk = alpha * kk + (1 - alpha) * heuristic_information[i]
            if kk < cumin:
                tdone = i
        time_eventassignment[tdone].append(each)
    return time_eventassignment