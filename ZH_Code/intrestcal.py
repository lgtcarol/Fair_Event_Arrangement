#coding=utf-8
from collections import defaultdict
from numpy import mean,std
import matplotlib.pyplot as plt
"一个关于对未知事件用户兴趣度值计算的小程序"

def myp(a):
    for i in a:
        print (i)
        print (a[i])

"计算相似度——标签"
def simlabel(A,B):
    p = 0.0
    for i in A:
        if i in B:
            p += A[i] * B[i]
    return p

def simcalx(a,b,w):
    p = 0.0
    if a[2] == b[2]:
        pp2 = 1.0
    else:
        pp2 = 0.0
    pp3 = simlabel(group_tagcac[a[3]],group_tagcac[b[3]])
    weeknum = float(abs(int(a[0]) - int(b[0])))/7.0
    pp1 = 1 - weeknum
    p = w[0] * pp2 + w[1] * pp1 + w[2] * pp3
    return p

def maxsim(event,userhis,userwei):
    xmax = 0.0
    for each in userhis:
        x = simcalx(event,each,userwei)
        if x > xmax:
            xmax = x
    return xmax

"计算用户对未知事件的兴趣度"
def calintresty(user,event,w,c):
    p = 0.0
    p1 = 0.0
    p2 = 0.0
    g = event[3]
    user_group = list(set(user_grouptp[user]).union(set(user_groupdif[user])))
    user_groupext = list(set(user_groupdifext[user]).difference(set(user_groupdif[user])))
    if g in user_group:
        if user_historyinfo[user].has_key(event):
            p1 = 1.0
        else:
            p1 = maxsim(event,user_historyinfo[user],w)
        p = p1
    elif g in user_groupext:
        p1 = 0.0
        p2 = maxsim(event,user_historyinfo[user],w)
        p = c * p2 + (1 - c) * p1
    return p

def calintrestn(user,event):
    p = 0.0
    if user_historyinfo[user].has_key(event):
        p = 1.0
    else:
        p = maxsim(event,user_historyinfo[user],user_weight[user])
    return p

user_curious = {}
infile = open("curiousca.txt","r")
for line in infile:
    p = line.split()
    user = p[0]
    user_curious[user] = float(p[1])
infile.close()

group_tagcac = defaultdict(dict)
infile = open("group_tagcac.txt","r")
for line in infile:
    p = line.split()
    user = p[0]
    tagc = p[1]
    group_tagcac[user][tagc] = float(p[2])
infile.close()

user_groupdif = defaultdict(list)
infile = open("user_groupdif.txt","r")
for line in infile:
    p = line.split()
    user = p[0]
    groups = p[1:]
    user_groupdif[user] = groups
infile.close()

user_grouptp = defaultdict(list)
infile = open("user_grouptp.txt","r")
for line in infile:
    p = line.split()
    user = p[0]
    groups = p[1:]
    user_grouptp[user] = groups
infile.close()

user_groupdifext = defaultdict(list)
infile = open("user_groupdifext.txt","r")
for line in infile:
    p = line.split()
    user = p[0]
    groups = p[1:]
    user_groupdifext[user] = groups
infile.close()

user_events = defaultdict(list)
userlist = []
infile = open("user_r.txt","r")
for line in infile:
    p = line.split()
    user = p[0]
    events = p[1:]
    user_events[user] = events
    userlist.append(user)
infile.close()

event_info = defaultdict(dict)
infile = open("eventscattr.txt","r")
for line in infile:
    p = line.split()
    event = p[0]
    event_info[event] = (p[4], p[3], p[1], p[5])
infile.close()

event_infot = defaultdict(tuple)
infile = open("eventscat.txt","r")
for line in infile:
    p = line.split()
    event = p[0]
    event_infot[event] = (p[4],p[3],p[1],p[5])
infile.close()

user_weight = defaultdict(list)
infile = open("userweight_vdg.txt","r")
for line in infile:
    p = line.split()
    user = p[0]
    for i in p[1:]:
        user_weight[user].append(float(i))
infile.close()

user_historyinfo = defaultdict(dict)
for each in user_events:
    t = user_events[each]
    for i in t:
        tuptran = event_info[i]
        if user_historyinfo[each].has_key(tuptran):
            user_historyinfo[each][tuptran] += 1.0
        else:
            user_historyinfo[each][tuptran] = 1.0
#myp(user_historyinfo)
"计算用户对每个事件的兴趣度值"
user_eventIn = defaultdict(dict)
for each in userlist:
    for i in event_infot:
        event = event_infot[i]
        Group = event[3]
        userC = user_curious[each]
        if userC != 0:
            t = calintresty(each,event,user_weight[each],userC)
            #if t != 0 :
            if t > 0.6:
                user_eventIn[each][i] = round(t,2)
        else:
            if Group in user_grouptp[each]:
                t = calintrestn(each, event)
                #if t != 0:
                if t > 0.6:
                    user_eventIn[each][i] = round(t,2)
#myp(user_eventIn)
'''
for each in userlist:
    for i in event_infot:
        event = event_infot[i]
        user_eventIn[each][i] = calintrest(each,event,user_weight[each],user_curious[each])

#myp(user_eventIn)
'''
"写入文件"
out = open("user_eventInNtime.txt","w")
for each in user_eventIn:
    for i in user_eventIn[each]:
        out.write(each)
        out.write(' ')
        out.write(i)
        out.write(' ')
        out.write(str(user_eventIn[each][i]))
        out.write('\n')
out.close()
