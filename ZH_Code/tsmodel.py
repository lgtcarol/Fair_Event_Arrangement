#coding=utf-8
from collections import defaultdict
"一个基于TS模型进行不同时间段产生冲突beta分布参数估计的小程序"
def myp(a):
    for i in a:
        print(i)
        print (a[i])
# 0:冲突 1:不冲突
def juge(a, b):
    x = int(a[0])
    y = int(b[0])
    if abs(x - y) <= 30000:
        return 1
    else:
        return 0
def caltime(a):
    if a/10000.0 - a/10000 <0.3:
        return a/10000
    else:
        if 1 + (a/10000) > 23:
            return 0
        else:
            return 1 + (a/10000)
def meanlist(a):
    s = 0.0
    for i in a:
        s += i
    return s / len(a)
#########################################数据录入#############################################
day_events = defaultdict(list)
event_info = {}
event_group = {}
infile = open("eventscattr.txt","r")
for line in infile:
    p = line.split()
    day_events[p[2]].append(p[0])
    event_info[p[0]] = (caltime(int(p[3])),int(p[4]))#time,weekday
    event_group[p[0]] = p[5]
infile.close()
group_users = defaultdict(list)
infile = open("user_groups.txt","r")
for line in infile:
    p = line.split()
    for i in p[1:]:
        group_users[i].append(p[0])
infile.close()
event_userstend = defaultdict(set)
for each in event_group:
    event_userstend[each] = set(group_users[event_group[each]])

ucg = defaultdict(dict)
daytime_events = defaultdict(dict)
for day in day_events:
    time_events = defaultdict(list)
    for e in day_events[day]:
        time_events[event_info[e][0]].append(e)
    daytime_events[day] = time_events
for day in daytime_events:
    te = daytime_events[day]
    for each in te.keys():
        chongtu = []
        if each - 3 < 0:
            ts = 0
        else:
            ts = each -3
        if each + 4 > 24:
            tee = 24
        else:
            tee = each + 4
        for i in range(ts,each):
            chongtu.extend(te[i])
        for j in range(each+1,tee):
            chongtu.extend(te[i])
        ss = 0
        for e in te[each]:
            for ee in chongtu:
                c = event_userstend[e]
                d = event_userstend[ee]
                if len(c & d) != 0 and juge(event_info[e], event_info[ee]):
                    ss += len(c&d)
        ucg[day][each] = ss
train = defaultdict(dict)
for day in ucg:
    avelist = []
    for each in ucg[day]:
        avelist.append(ucg[day][each])
    avenum = meanlist(avelist)
    for each in ucg[day]:
        if ucg[day][each] > avenum:
            train[day][each] = 0
        else:
            train[day][each] = 1
result = defaultdict(list)
for i in range(0,24):
    result[i] = [1,1]
for day in train:
    for each in train[day]:
        if train[day][each] == 0:
            result[each][1] += 1
        else:
            result[each][0] += 1
myp(result)
out = open("tsmodel.txt","w")
for each in result:
    out.write(str(each))
    out.write(' ')
    out.write(str(result[each][0]))
    out.write(' ')
    out.write(str(result[each][1]))
    out.write('\n')
out.close()