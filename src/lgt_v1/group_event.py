'''按月份获取event数量和event列表，并添加各group的venue信息'''
num_month_events = defaultdict(int)
month_events = defaultdict(list)
for event in list(trainG_E):
    month = events_dealt[event][1][5:7]
    num_month_events[month] += 1
    month_events[month].append(event)
#按照月份升序排列,排序使二者类型变为list
num_month_events = sorted(num_month_events.items(),key=lambda item:item[0])
month_events = sorted(month_events.items(),key=lambda item:item[0])