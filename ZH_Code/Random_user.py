# coding=utf-8
from collections import defaultdict
import random
import time


def myp(a):
    """
    :type a: object
    """
    for i in a:
        print(i)
        print(a[i])


eventcf = defaultdict(list)
infile = open("day_eventscf.txt", "r")
for line in infile:
    p = line.split()
    eventcf[p[1]] = p[2:]
infile.close()

# 用户及事件容量
user_capacity = {}
event_capacity = {}
userlist = []
eventlist = []
infile = open("user_cap.txt", "r")
for line in infile:
    p = line.split()
    user_capacity[p[0]] = float(p[1]) + 1.0
    userlist.append(p[0])
infile.close()

infile = open("event_cap.txt", "r")
for line in infile:
    p = line.split()
    event_capacity[p[0]] = float(p[1])
    eventlist.append(p[0])
infile.close()

U = float(len(userlist))
V = float(len(eventlist))

"Random-user"


def judge(event, events):
    for each in events:
        if (event in eventcf[each]) or (event == each):
            return 0
    return 1


start = time.time()
user_eventsRandom_user = defaultdict(list)
event_users = defaultdict(list)
for user in userlist: #逐个遍历用户，为其分配事件
    count = user_capacity[user] * 90
    user_eventsRandom_user[user] = []
    flag = 0
    while (count and flag < count):
        event = random.choice(eventlist)
        if judge(event, user_eventsRandom_user[user]) and (len(event_users[event]) < event_capacity[event]):
            p = random.randint(0, 100) * 1.0 / 100000
            if p < (event_capacity[event] / U):
                user_eventsRandom_user[user].append(event)
                event_users[event].append(user)
                count -= 1
            else:
                flag += 1
        else:
            flag += 1
end = time.time()
# myp(event_users)
out = open("Random_user.txt", "w")
for line in event_users:
    out.write(line)
    for i in event_users[line]:
        out.write(' ')
        out.write(i)
    out.write('\n')
out.close()
print(end - start)
