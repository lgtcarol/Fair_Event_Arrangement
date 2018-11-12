#coding=utf-8
from collections import defaultdict
import copy
import time
def myp(a):
    for i in a:
        print(i)
        print(a[i])

#用户及事件容量
user_capacity = {}
event_capacity = {}
userlist = []
infile = open("user_cap.txt","r")
for line in infile:
    p = line.split()#应该得到类似x1, x2
    user_capacity[p[0]] = float(p[1]) + 1.0
    userlist.append(p[0])
infile.close()

infile = open("event_cap.txt","r")
for line in infile:
    p = line.split()
    event_capacity[p[0]] = float(p[1])
infile.close()

#用户对事件评分
user_eventIn = defaultdict(dict)
infile = open("user_eventIn1.txt","r")
for line in infile:
    p = line.split()
    user_eventIn[p[0]][p[1]] = float(p[2])
infile.close()

#冲突集
day_cfevent = defaultdict(list)
infile = open("day_cfevents1.txt","r")
for line in infile:
    p = line.split()
    day = p[0] #该行数据是：重复日期 事件序列吗？
    events = p[1:]
    day_cfevent[day].append(events) #以日期作为键值，以事件序列作为有序字典值
infile.close()

day_events = defaultdict(list)
infile = open("day_events1.txt","r")
for line in infile:
    p = line.split()
    day_events[p[0]] = p[1:] #是某天发生的所有事件序列吗
infile.close()

#每个事件冲突集合
day_eventscf = defaultdict(dict)
infile = open("day_eventscf1.txt","r")
for line in infile:
    p = line.split()
    day_eventscf[p[0]][p[1]] = p[2:] #??第一列，第二列和后面的列有什么不同？
infile.close()

'''
#比较每次删除的边是否相同
for t in day_eventscf:
    print t
    for i in day_eventscf[t]:
        #print i
        #print day_eventscf[t][i]
        m = len(day_eventscf[t][i])
        for j in day_cfevent[t]:
            if i in j:
                #print j
                n = len(j)-1
        print m - n
'''
#函数开始
def canstop(ue): #判断列表是否为空
    for i in ue:
        if len(ue[i]) != 0:
            return 1
    return 0

def Deleteuser(u,ue): #置空
    ue[u] = []

def Findecf(e): #遍历冲突集找到该事件，但和谁冲突呢？？
    for i in range(len(cfevents)):
        if e in cfevents[i]:
            return cfevents[i]

def Deleteusercf(u,cf,ue): #遍历删除用户
    for i in cf:
        if i in ue[u]:
            ue[u].remove(i)

def Deleteevent(ue,e): #遍历删除事件
    for i in ue:
        if e in ue[i]:
            ue[i].remove(e)

def colorse(usere,userl,userc,eventc):
    ue = copy.deepcopy(usere)
    ul = copy.deepcopy(userl)
    uc = copy.deepcopy(userc)
    ec = copy.deepcopy(eventc)
    #copy()其实是与deep copy相对的shallow copy，复杂的Object，如list中套着list的情况，shallow copy中的子list并未从原object真的独立出来
    #deep copy则更加符合我们对复制的直觉定义：一旦复制出来了，就应该是独立的了。

    M = defaultdict(list)
    #  Python中可以使用collections中的defaultdict类实现创建进行统一初始化的字典。
    # 当初始化为list时 可以实现统计几个key出现过哪几个value，即dict_items([('yellow', [1, 3]), ('blue', [2, 4]), ('red', [1])])
    # 当初始化为int时 可以统计一个key出现过多少次，如dict_items([('m', 1), ('i', 4), ('s', 4), ('p', 2)])
    # 具体代码见https://blog.csdn.net/grey_csdn/article/details/66528109
    while(canstop(ue)):
        for i in ul:
            if uc[i] == 0 | len(ue[i]) == 0:
                ul.remove(i)
        for i in ul:
            if len(ue[i]) == 0:
                continue
            else:
                emax = ue[i][0]
                if jugeslack(i,emax):
                    etran = slack(ec,i,emax,M,ue)
                    if etran:
                        emax = etran
                uc[i] -= 1
                ec[emax] -= 1
                if uc[i] == 0:
                    Deleteuser(i,ue)
                else:
                    cf = Findecf(emax)
                    Deleteusercf(i,cf,ue)
                if ec[emax] == 0:
                    Deleteevent(ue,emax)
                M[emax].append(i)
    return M
def colorsenslack(usere,userl,userc,eventc):
    ue = copy.deepcopy(usere)
    ul = copy.deepcopy(userl)
    uc = copy.deepcopy(userc)
    ec = copy.deepcopy(eventc)
    M = defaultdict(list)
    while(canstop(ue)):
        for i in ul:
            if uc[i] == 0 | len(ue[i]) == 0:
                ul.remove(i)
        for i in ul:
            if len(ue[i]) == 0:
                continue
            else:
                emax = ue[i][0]
                uc[i] -= 1
                ec[emax] -= 1
                if uc[i] == 0:
                    Deleteuser(i,ue)
                else:
                    cf = Findecf(emax)
                    Deleteusercf(i,cf,ue)
                if ec[emax] == 0:
                    Deleteevent(ue,emax)
                M[emax].append(i)
    return M
def jugeslack(u,e):
    if e not in user_eventmax[u]:
        return 1
    else:
        return 0
def slack(ec,u,e,M,ue):
    min = 2.0
    emin = ''
    umin = ''
    for i in user_eventmax[u]:
        for j in M[i]:
            if user_eventIn[j][i] < min:
                min = user_eventIn[j][i]
                emin = i
                umin = j
    if emin:
        cfx = Findecf(emin)
        max = 0.0
        emax = ''
        for k in cfx:
            if ec[k] > 0:
                if k in user_eventIn[umin]:
                    if user_eventIn[umin][k] > max:
                        max = user_eventIn[umin][k]
                        emax = k
        if emax:
            before = user_eventIn[umin][emin] + user_eventIn[u][e]
            after = user_eventIn[umin][emax] + user_eventIn[u][emin]
            if after - before > 0:
                M[emin].remove(umin)
                M[emax].append(umin)
                ec[emax] -= 1
                if ec[emax] == 0:
                    Deleteevent(ue, emax)
                ec[emin] += 1
                return emin
    return ''
def slack2(ec,u,e,M,ue):
    min = 2.0
    emin = ''
    umin = ''
    for i in user_eventmax[u]:
        for j in M[i]:
            if user_eventIn[j][i] < min:
                min = user_eventIn[j][i]
                emin = i
                umin = j
    if emin:
        cfx = eventcf[emin]
        max = 0.0
        emax = ''
        for k in cfx:
            if ec[k] > 0:
                if k in user_eventIn[umin]:
                    if user_eventIn[umin][k] > max:
                        max = user_eventIn[umin][k]
                        emax = k
        if emax:
            before = user_eventIn[umin][emin] + user_eventIn[u][e]
            after = user_eventIn[umin][emax] + user_eventIn[u][emin]
            if after - before > 0:
                M[emin].remove(umin)
                M[emax].append(umin)
                ec[emax] -= 1
                if ec[emax] == 0:
                    Deleteevent(ue, emax)
                ec[emin] += 1
                return emin
    return ''
def greedybasic(usere,userl,userc,eventc):
    ue = copy.deepcopy(usere)
    ul = copy.deepcopy(userl)
    uc = copy.deepcopy(userc)
    ec = copy.deepcopy(eventc)
    M = defaultdict(list)
    while (canstop(ue)):
        for i in ul:
            if uc[i] == 0 | len(ue[i]) == 0:
                ul.remove(i)
        for i in ul:
            if len(ue[i]) == 0:
                continue
            else:
                emax = ue[i][0]
                if jugeslack(i,emax):
                    etran = slack2(ec,i,emax,M,ue)
                    if etran:
                        emax = etran
                print (emax)
                uc[i] -= 1
                ec[emax] -= 1
                if uc[i] == 0:
                    Deleteuser(i, ue)
                else:
                    cf = eventcf[emax]
                    Deleteusercf(i, cf, ue)
                if ec[emax] == 0:
                    Deleteevent(ue, emax)
                M[emax].append(i)
    print (M)
    return M
def greedybasicnslack(usere,userl,userc,eventc):
    ue = copy.deepcopy(usere)
    ul = copy.deepcopy(userl)
    uc = copy.deepcopy(userc)
    ec = copy.deepcopy(eventc)
    M = defaultdict(list)
    while (canstop(ue)):
        for i in ul:
            if uc[i] == 0 | len(ue[i]) == 0:
                ul.remove(i)
        for i in ul:
            if len(ue[i]) == 0:
                continue
            else:
                emax = ue[i][0]
                print (emax)
                uc[i] -= 1
                ec[emax] -= 1
                if uc[i] == 0:
                    Deleteuser(i, ue)
                else:
                    cf = eventcf[emax]
                    Deleteusercf(i, cf, ue)
                if ec[emax] == 0:
                    Deleteevent(ue, emax)
                M[emax].append(i)
    print (M)
    return M
#数据定义
user_eventsort = defaultdict(list)
for each in user_eventIn:
    t = user_eventIn[each]
    st = sorted(t.items(),key=lambda d:d[1],reverse=True)
    max = st[0][1]
    for i in st:
        user_eventsort[each].append(i[0])
user_eventsorteachday = defaultdict(dict)
for each in day_events:
    t = day_events[each]
    tran = defaultdict(list)
    for i in user_eventsort:
        tt = user_eventsort[i]
        for j in tt:
            if j in t:
                tran[i].append(j)
    user_eventsorteachday[each] = tran
user_eventmaxday = defaultdict(dict)
for each in user_eventsorteachday:
    t = defaultdict(list)
    for i in user_eventsorteachday[each]:
        max = user_eventIn[i][user_eventsorteachday[each][i][0]]
        for j in user_eventsorteachday[each][i]:
            if user_eventIn[i][j] == max:
                t[i].append(j)
    user_eventmaxday[each] = t
userlist_day = defaultdict(list)
for each in user_eventsorteachday:
    for i in user_eventsorteachday[each]:
        userlist_day[each].append(i)
Management1 = defaultdict(dict)
Management2 = defaultdict(dict)
start = time.time()
for each in day_cfevent:
    userlistday = userlist_day[each]
    cfevents = day_cfevent[each]
    userevents = user_eventsorteachday[each]
    user_eventmax = user_eventmaxday[each]
    eventcf = day_eventscf[each]
    #m1 = colorse(userevents,userlistday,user_capacity,event_capacity)
    m1 = colorsenslack(userevents,userlistday,user_capacity,event_capacity)
    #m2 = greedybasicnslack(userevents, userlistday, user_capacity, event_capacity)
    #m2 = greedybasic(userevents,userlistday,user_capacity,event_capacity)
    Management1[each] = m1
    #Management2[each] = m2
end = time.time()
print (end - start)

out = open("colorsewithoutslack1.txt","w")
for each in Management1:
    for i in Management1[each]:
        out.write(i)
        for j in Management1[each][i]:
            out.write(' ')
            out.write(j)
        # out.write('\n')
out.close()
'''
t = 0
for each in Management1:
    for i in Management1[each]:
        a = Management1[each][i]
        b = Management2[each][i]
        s = set(a) - set(b)
        ds = set(b) - set(a)
        if s | ds:
            t += 1
            print i
            print s
            print ds
            print t
'''