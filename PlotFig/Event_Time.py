from Feature_Extract import *
import matplotlib as plt
import numpy as np

#https://blog.csdn.net/zhangxiaojiakele/article/details/78014627
fig=plt.figure(1)
ax1=plt.subplot(111)

data = []
month = 0
for i in enumerate(num_month_events):
    data.append(num_month_events[month][1])
    month += 1
width = 0.5
x_bar = np.arange(12)

rect = ax1.bar(left=x_bar, height=data, width=width)

for rec in rect:
    x = rec.get_x()
    y = rec.get_height()
    ax1.text(x+0.1, 1.02*y, str(y))

ax1.set_xticks(x_bar)
ax1.set_xticklabels(("1","2","3","4","5","6","7","8","9","10","11","12"))
plt.xlabel('month')
ax1.set_ylabel('events_number')
ax1.set_title("Events_Num of every month")
ax1.set_ylim(600, 1500)
plt.show()
