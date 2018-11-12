#coding=utf-8
from collections import defaultdict
import random
import time


def myp(a):
    """
    :type a: object
    """
    for i in a:
        print (i)
        print (a[i])


eventcf = defaultdict(list)
infile = open("day_eventscf.txt","r")
for line in infile:
    p = line.split()
    eventcf[p[1]] = p[2:]
infile.close()

#用户及事件容量
user_capacity = {}
userlist = []
infile = open("user_cap.txt","r")
for line in infile:
    p = line.split()
    user_capacity[p[0]] = float(p[1]) + 1.0
    userlist.append(p[0])
infile.close()

event_capacity = {}
eventlist = []
infile = open("event_cap.txt","r")
for line in infile:
    p = line.split()
    event_capacity[p[0]] = float(p[1])
    eventlist.append(p[0])
infile.close()

U = float(len(userlist))
V = float(len(eventlist))

"Random-event"

def judge(event,events): #查询是否为冲突事件的方法
    for each in events:
        if (event in eventcf[each]) or (event == each):
            return 0
    return 1

'''
    type: U V 分别是float(len(userlist)) 和 float(len(eventlist))
          eventlist是通过读取events_cap.txt获得的事件list
          event_capacity是上述形成的字典
          同理，userlist和user_capacity是users_cap.txt的结果
          ？user_events[user]相当于直接赋值了
          ？为何容量*90
'''
start = time.time() #返回当前时间戳
event_usersRandom_event = defaultdict(list)
user_events = defaultdict(list)
for event in eventlist:
    count = event_capacity[event] #事件容量
    event_usersRandom_event[event] = [] #每个事件的安排结果初始为空list
    while(count): #该事件未满
        user = random.choice(userlist)  #choice函数返回列表，元组或字串的随即项
        if judge(event,user_events[user]) and (len(user_events[user]) < (user_capacity[user] * 90)):
            p = random.randint(0, 100)*1.0/100 #随机概率
            if p < (user_capacity[user]*90 / V):
                event_usersRandom_event[event].append(user)
                user_events[user].append(event)
                count -= 1
end = time.time()
#myp(event_usersRandom_event)
out = open("Random_event.txt","w")
for line in event_usersRandom_event:
    out.write(line)
    for i in event_usersRandom_event[line]:
        out.write(' ')
        out.write(i)
    out.write('\n')
out.close()
print (end - start)