from AnalyData import *
from CreateNetwork import *
import pandas as pd
from datetime import date
from collections import defaultdict

'''ATTENTION：上述导入只是为了编译检查不报错，运行时并非需要运行上两句，而是导入变量'''


'''图中group节点属性设置'''
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

class Group(object):

    @classmethod
    def tuple_2_list(self, num_month):
        num_month_list = []
        for item, tuple in enumerate(num_month):
            num_month_list.append(list(num_month[item]))
        return num_month_list

    @classmethod
    def generate_groupdf(self):
        # 仅是读取节点属性构建DataFrame
        data = defaultdict(list)
        # g_list = []  # 作为索引在遍历节点时依次获得
        group_id = []
        num_u_list = []
        num_e_list = []
        num_venue_list = []
        all_month = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        df_num_month = defaultdict(list)
        for node in list(trainG.nodes):
            if trainG.nodes[node]['node_type'] == 'G':
                group_id.append(node)
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
        # index = g_list
        data['group_id'] = group_id
        data['num_u'] = num_u_list
        data['num_e'] = num_e_list
        data['num_venue'] = num_venue_list
        #依次获取每月列 对应 group的事件数列表
        for month in all_month:
            data['m_' + month] = df_num_month[month]
        # data期望len=4+12列
        self.group_df = pd.DataFrame(data)
        return self.group_df

    @classmethod
    def modify_groupdf(self):
        repeat_v = []
        mean_num = []
        num_of_freqmonth = []  # 某月event数超过1.2*mean
        for index, row in self.group_df.iterrows():
            num_e = row['num_e']
            num_venue = row['num_venue']
            repeat = num_e - num_venue
            repeat_v.append(round(repeat / num_e, 3))
            cnt = 0
            for i in range(12):
                if row[3 + i] != 0:
                    cnt += 1
            mean_month = row['num_e'] / cnt * 1.0
            mean_num.append(mean_month)
            cnt_freq = 0
            for i in range(12):
                if row[3 + i] >= 1.5 * mean_month:
                    cnt_freq += 1
            num_of_freqmonth.append(cnt_freq)
        self.group_df['mean_month'] = mean_num
        self.group_df['repeat_v'] = repeat_v
        self.group_df['num_of_freqmonth'] = num_of_freqmonth
        #期望列数：16+3=19列
        return self.group_df

    # later to be used
    @classmethod
    def enrich_gtags(self):
        e_tags = defaultdict(list)
        g_tags = defaultdict(list)
        #group标签初始化
        for node in list(trainG.nodes):
            if trainG.nodes[node]['node_type'] == 'G':
                g_tags[node] = group_tags_raw[node]

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
                #group_tags = group_tags_raw[events_dealt[node][3]]
                which_group = events_dealt[node][3]
                g_tags[which_group] = set(g_tags[which_group]) | set(e_tags[node])
        return g_tags



group_object = Group()
#group_object.set_gnode_attr()
group_df = group_object.generate_groupdf()
group_df = group_object.modify_groupdf()


