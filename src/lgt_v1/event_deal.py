from AnalyData import *
from CreateNetwork import *
import pandas as pd
from datetime import date
from src.lgt_v1.group_deal import  group_df

'''图中节点属性设置'''
def set_enode_attr():
    for node in list(trainG.nodes):
        if trainG.nodes[node]['node_type'] == 'E':
            trainG.nodes[node]['num_of_u'] = len(edge_eu[node])
            group_u = set(edge_gu[events_dealt[node][3]])
            event_u = set(edge_eu[node])
            trainG.nodes[node]['num_group_u'] = len(group_u & event_u)
            trainG.nodes[node]['group_u'] = list(group_u & event_u)
            trainG.nodes[node]['other_u'] = list(event_u - (group_u & event_u))

class Event(object):

    @classmethod
    def getWeekday(self, row):
        if row == 'null':
            return row
        else:
            return date(int(row[0:4]), int(row[5:7]), int(row[8:10])).weekday() + 1

    @classmethod
    # 此时的event_df已经先和group_df合并了
    def generate_eventdf(self, group_df):
        # 仅是读取节点属性构建DataFrame
        data = defaultdict(list)
        event_id = []  # 作为索引在遍历节点时依次获得
        venue_id = []
        date_time = []
        clock_time = []
        e_group = []
        for event in list(trainG_E):
            event_id.append(event)
            venue_id.append(events_dealt[event][0])
            date_time.append(events_dealt[event][1])
            clock_time.append(events_dealt[event][2])
            e_group.append(events_dealt[event][3])
        data['event_id'] = event_id
        data['group_id'] = e_group
        data['venue_id'] = venue_id
        data['date'] = date_time
        data['weekday'] = (pd.Series(data['date'])).astype(str).apply(self.getWeekday)
        data['clock'] = clock_time
        self.event_df = pd.DataFrame(data)
        self.event_df = pd.merge(self.event_df, group_df) #14715,少20
        return self.event_df
        #2018/12/13
        #丰富事件的属性，如举办人数，举办季度(group角度：group种类)


    '''to use later'''
    @classmethod
    def zip_events(self):
        #进行事件归类（group, venue, weekday）得到6239行, 加上clock得到7202条，原事件数是14738压缩51%事件
        grouped = self.event_df.groupby(['group_id', 'venue_id', 'weekday','clock'])
        data = defaultdict(list)
        label_cnt = 0
        for (k1, k2, k3, k4), block in grouped:
            label_cnt += 1
            #events = list(block['event_id'])
            data['group_id'].append(k1)
            data['venue_id'].append(k2)
            data['weekday'].append(k3)
            data['clock'].append(k4)
            #data['num_sime'].append(len(events)) #归到该类的事件数
            data['category_id'].append(label_cnt)
        sim_event_df = pd.DataFrame(data)
        zip_event_df = pd.merge(self.event_df, sim_event_df, on=['group_id', 'venue_id', 'weekday', 'clock'])
        return sim_event_df, zip_event_df
    #2018/12/13
    @classmethod
    def zip2_events(self):
        #进行事件归类（group, venue, weekday）得到6239行, 加上clock得到7202条，原事件数是14738压缩51%事件
        grouped = self.event_df.groupby(['venue_id', 'weekday','clock'])
        data = defaultdict(list)
        label_cnt = 0
        for (k1, k2, k3), block in grouped:
            label_cnt += 1
            #events = list(block['event_id'])
            #data['group_id'].append(k1)
            data['venue_id'].append(k1)
            data['weekday'].append(k2)
            data['clock'].append(k3)
            #data['num_sime'].append(len(events)) #归到该类的事件数
            data['category_id'].append(label_cnt)
        sim2_event_df = pd.DataFrame(data)
        zip2_event_df = pd.merge(self.event_df, sim2_event_df, on=['venue_id', 'weekday', 'clock'])
        return sim2_event_df, zip2_event_df

event_object = Event()
#event_object.set_enode_attr()
event_df = event_object.generate_eventdf(group_df)
sim_event_df, zip_event_df = event_object.zip_events()
sim2_event_df,zip2_event_df = event_object.zip2_events()