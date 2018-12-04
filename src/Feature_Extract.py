from AnalyData import *
from CreateNetwork import *
import pandas as pd

'''ATTENTION：上述导入只是为了编译检查不报错，运行时并非需要运行上两句，而是导入变量'''
from collections import defaultdict


class Group(object):
    @classmethod
    def set_gnode_attr(self):
        for node in list(trainG.nodes):
            if trainG.nodes[node]['node_type'] == 'G':
                trainG.nodes[node]['num_of_u'] = len(edge_gu[node])
                assert isinstance(trainG, object)
                trainG.nodes[node]['num_of_e'] = len(edge_ge[node])
                month_events = defaultdict(list)
                month_events_num = defaultdict(int)
                venue_times = defaultdict(int)
                for event in list(edge_ge[node]):
                    month = events_dealt[event][1][5:7]
                    month_events[month].append(event)
                    month_events_num[month] += 1
                    venue_times[events_dealt[event][0]] += 1
                month_events = sorted(month_events.items(), key=lambda item: item[0])
                month_events_num = sorted(month_events_num.items(), key=lambda item: item[0])
                venue_times = sorted(venue_times.items(), key=lambda item: item[1])
                trainG.nodes[node]['month_events'] = month_events
                trainG.nodes[node]['num_month_events'] = month_events_num
                trainG.nodes[node]['venue_times'] = venue_times

    @classmethod
    def tuple_2_list(self, num_month):
        num_month_list = []
        for item, tuple in enumerate(num_month):
            num_month_list.append(list(num_month[item]))
        return num_month_list

    @classmethod
    def generate_df(self):
        # 仅是读取节点属性构建DataFrame
        data = defaultdict(list)
        g_list = []  # 作为索引在遍历节点时依次获得
        num_u_list = []
        num_e_list = []
        num_venue_list = []
        all_month = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        df_num_month = defaultdict(list)
        for node in list(trainG.nodes):
            if trainG.nodes[node]['node_type'] == 'G':
                g_list.append(node)
                num_u_list.append(trainG.nodes[node]['num_of_u'])
                num_e_list.append(trainG.nodes[node]['num_of_e'])
                num_venue_list.append(len(trainG.nodes[node]['venue_times']))
                # 将二元组排成的列表 转为 列表排成的列表
                g_num_month = self.tuple_2_list(trainG.nodes[node]['num_month_events'])
                zero_month = set(all_month)  # 记录无事件的月份，之后一次填充0
                for month in all_month:
                    for i, item in enumerate(g_num_month):
                        if (g_num_month[i][0] == month):  # 月份匹配则赋值，否则赋0
                            df_num_month[month].append(g_num_month[i][1])
                            zero_month.remove(month)
                for i in zero_month:
                    df_num_month[i].append(0)
                # 到此应完成一个group事件映射到df_num_month各月份
        index = g_list
        data['num_u'] = num_u_list
        data['num_e'] = num_e_list
        data['num_venue'] = num_venue_list
        for month in all_month:
            # 依次获取每月列 对应 group的事件数列表
            data['m_' + month] = df_num_month[month]
        # data期望len=3+12列
        df = pd.DataFrame(data, index=g_list)
        return df

    @classmethod
    def modify_df(self):
        repeat_v = []
        num_freq_month = []  # 某月event数超过1.2*mean
        for index, row in group_df.iterrows():
            num_e = row['num_e']
            num_venue = row['num_venue']
            repeat = num_e - num_venue
            repeat_v.append(round(repeat / num_e, 3))
            cnt = 0
            for i in range(12):
                if row[3 + i] != 0:
                    cnt += 1
            mean_month = row['num_e'] / cnt * 1.0
            cnt_freq = 0
            for i in range(12):
                if row[3 + i] >= 1.5 * mean_month:
                    cnt_freq += 1
            num_freq_month.append(cnt_freq)
        group_df['repeat_v'] = repeat_v
        group_df['freq_month'] = num_freq_month
        return group_df

    def enrich_gtags(self):
        e_tags = defaultdict(list)
        for node in list(trainG.nodes):
            if trainG.nodes[node]['node_type'] == 'E':
                groupu_tags = defaultdict(int)
                otheru_tags = defaultdict(int)
                for item in trainG.nodes[node]['group_u']:  # 遍历成员
                    for tag in user_tags_raw[item]:  # 遍历并标记成员tag
                        groupu_tags[tag] += 1.0
                for item_other in trainG.nodes[node]['other_u']:
                    for tag_other in user_tags_raw[item_other]:
                        otheru_tags[tag_other] += 1.0
                # 选择融入
                for tag_g in groupu_tags:
                    if groupu_tags[tag_g] >= 0.2 * trainG.nodes[node]['num_group_u']:
                        e_tags[node].append(tag_g)

                num_other_u = trainG.nodes[node]['num_of_u'] - trainG.nodes[node]['num_group_u']
                for tag_o in otheru_tags:
                    if otheru_tags[tag_o] >= 0.1 * num_other_u:
                        e_tags[node].append(tag_o)
                group_tags = group_tags_raw[events_dealt[node][3]]
                e_tags[node] = set(e_tags[node]) | set(group_tags)
        return e_tags


#group = Group()
group_df = group.modify_df()
group_df = group.generate_df()
group.set_gnode_attr()


class Event(object):
    def set_enode_attr(self):
        for node in list(trainG.nodes):
            if trainG.nodes[node]['node_type'] == 'E':
                trainG.nodes[node]['num_of_u'] = len(edge_eu[node])
                group_u = set(edge_gu[events_dealt[node][3]])
                event_u = set(edge_eu[node])
                trainG.nodes[node]['num_group_u'] = len(group_u & event_u)
                trainG.nodes[node]['group_u'] = list(group_u & event_u)
                trainG.nodes[node]['other_u'] = list(event_u - (group_u & event_u))

    def generate_etags(self):
        pass


event = Event()
event.set_enode_attr()
event_tags = event.generate_etags()


class User(object):
    def set_unode_attr(self):
        for node in list(trainG.nodes):
            if trainG.nodes[node]['node_type'] == 'U':
                trainG.nodes[node]['num_of_g'] = len(edge_ug[node])
                trainG.nodes[node]['num_of_e'] = len(edge_ue[node])
                attend_e = edge_ue[node]
                venue_times = defaultdict(int)
                #后面探索用户时间倾向
                for event in attend_e:
                    venue_times[events_dealt[event][0]] += 1
                trainG.nodes[node]['venue_times'] = venue_times


user = User()
user.set_unode_attr()

'''添加user-group权重信息：Jaccard相似度'''
#示例：'G_456'和'U_50657'
for item_g in trainG_G:
    A = set(group_tags_raw[item_g])
    for item_u in trainG.neighbors(item_g):
        if trainG.nodes[item_u]['node_type'] == 'U':
            B = set(user_tags_raw[item_u])  # 获取一个用户的tags并转为set
            numerator = A & B
            denominator = A | B
            Jaccard_score = (len(numerator) / len(denominator))*1.0
            trainG[item_u][item_g]['weight'] = round(Jaccard_score, 3)


'''将每个group中成员Jaccard_score为0.0个数保存到node属性'''
for item_dictg in group_tags_raw:
    cnt = 0
    for item_u in trainG.neighbors(item_dictg):
        if(trainG[item_u][item_dictg]['weight'] > 0.0):
            cnt += 1
    trainG.nodes[item_dictg]['cap_zero'] = trainG.nodes[item_dictg]['num_of_u'] - cnt

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













