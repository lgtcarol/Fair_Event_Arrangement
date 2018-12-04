from AnalyData import *
from CreateNetwork import *
import pandas as pd
from datetime import date
import numpy as np

from src.lgt_v1.event_deal import *

'''图中user节点属性设置'''
def set_unode_attr():
    for node in list(trainG.nodes):
        if trainG.nodes[node]['node_type'] == 'U':
            trainG.nodes[node]['num_of_g'] = len(edge_ug[node])
            trainG.nodes[node]['num_of_e'] = len(edge_ue[node])
            attend_e = edge_ue[node]
            venue_times = defaultdict(int)
            # 后面探索用户时间倾向
            for event in attend_e:
                venue_times[events_dealt[event][0]] += 1
            trainG.nodes[node]['venue_times'] = venue_times

class User(object):

    @classmethod
    def generate_labeldf(self, zip_event_df):
        #统计u-e关系总数
        ue_cnt = 0
        for u in edge_ue:
            for e in edge_ue[u]:
                ue_cnt += 1
        label_mat = np.zeros((ue_cnt, 7202), dtype=int)
        row_index = 0
        for u in edge_ue:
            for e in edge_ue[u]:
                tmp = list(zip_event_df[zip_event_df['event_id']==e]['category_id'])
                col_index = tmp[0]-1 #矩阵下标从0开始的
                label_mat[row_index, col_index] = 1
                row_index += 1
        print("row_index = %d"%row_index)
        #categories实际只会用到7192
        column = ['catg_' + str(i) for i in range(1, 7203)]
        user_label_df = pd.DataFrame(label_mat, columns=column)
        user_index = []
        for u in edge_ue:
            for e in edge_ue[u]:
                user_index.append(u)
        print('len(user_index) = %d' % len(user_index))
        col_df = pd.DataFrame(user_index, columns=['user_id'])
        user_label_df = pd.concat([col_df, user_label_df], axis=1)
        #3. user及其标签Dataframe
        return user_label_df

    def combine_df(self, zip_event_df, group_df):
        #user-event
        data = defaultdict(list)
        data['user_id'] = []
        data['event_id'] = []
        for u in edge_ue:
            for e in edge_ue[u]:
                data['user_id'].append(u)
                data['event_id'].append(e)
        print('len(user_index) = %d' % len(data['user_id']))
        uecol_df = pd.DataFrame(data, columns=['user_id', 'event_id'])
        # 直接merge试试,之后再考虑删除event_id，因为拼接label矩阵会用
        ue_df = pd.merge(uecol_df,zip_event_df)
        ueg_df = pd.merge(ue_df, group_df, left_on=['group_id'])#由于左比右多'G_376'导致最终为13026条,26列


        '''
        不考虑内存时的流利做法
        grouped = ueg_df.groupby(['user_id','group_id', 'venue_id', 'weekday','clock']) #可形成94332条独立的参与信息
        one_hot = pd.get_dummies(ueg_df['category_id'])
        column = ['c_' + str(i) for i in range(1, 7193)]
        one_hot.to_csv("one_hot.csv", encoding="utf-8")
        '''
        x = ueg_df['category_id'].copy()
        del ueg_df['category_id']
        ueg_df['category_id'] = x


        ueg_label= pd.merge(ueg_df, user_label_df, on=['user_id', 'event_id'])
        x = [1, 4, 7]
        ue_df.drop(ue_df.columns[x], axis=1, inplace=True)
        ue_df.drop_duplicates(keep='first', inplace=True)#剩余94392
        ue_df = ue_df.reset_index(drop=True)
        #user-group
        ueg_df = pd.merge(ue_df, group_df)
        ueg_df


    @classmethod
    def param_analyze(self):
        nx.average_clustering(trainG) #全图的聚类系数在0.355
        sum_degree = 0
        user_degree = []
        #计算用户节点的平均度数
        i = 0
        for node in list(trainG.nodes):
            if trainG.nodes[node]['node_type'] == 'U':
                i += 1
                sum_degree += trainG.degree(node)
                user_degree.append(trainG.degree(node))
        ave_degree = sum_degree/i
        print("average degree of U: %d" % ave_degree)

user_object = User()
user_label_df = user_object.generate_labeldf(zip_event_df)
#user.set_unode_attr()