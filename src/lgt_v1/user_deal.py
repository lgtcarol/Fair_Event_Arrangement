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

    # 思路二
    @classmethod
    def generate_uegdf(self, event_df, group_df):
        # user-event条目
        data = defaultdict(list)
        data['user_id'] = []
        data['event_id'] = []
        data['u_num_g'] = []
        data['u_num_e'] = []
        for u in edge_ue:
            for e in edge_ue[u]:
                data['user_id'].append(u)
                data['event_id'].append(e)
                x = trainG.nodes[u]['num_of_g']
                y = trainG.nodes[u]['num_of_e']
                data['u_num_g'].append(x)
                data['u_num_e'].append(y)
        print('len(user_index) = %d' % len(data['user_id']))
        user_df = pd.DataFrame(data)

        # 符合edge_ue 130358 ,ue中的event估计和trainG_E一样多，经过group_df过滤后event减少导致ue_df减少
        ueg_df = pd.merge(user_df,event_df)
        #ueg_df = pd.merge(ue_df, group_df)  # 最终为130264条,26列
        return user_df,ueg_df


    # 思路一：event_df中有category_id时的考虑
    @classmethod
    def generate_uegdf(self, zip_event_df, group_df):
        # user-event条目
        data = defaultdict(list)
        data['user_id'] = []
        data['event_id'] = []
        data['u_num_g'] = []
        data['u_num_e'] = []
        for u in edge_ue:
            for e in edge_ue[u]:
                data['user_id'].append(u)
                data['event_id'].append(e)
                x = trainG.nodes[u]['num_of_g']
                y = trainG.nodes[u]['num_of_e']
                data['u_num_g'].append(x)
                data['u_num_e'].append(y)
        print('len(user_index) = %d' % len(data['user_id']))
        user_df = pd.DataFrame(data)

        # 直接merge试试,之后再考虑删除event_id，因为拼接label矩阵会用
        ue_df = pd.merge(user_df,
                         zip_event_df)  # 符合edge_ue 130358 ,ue中的event估计和trainG_E一样多，经过group_df过滤后event减少导致ue_df减少
        ueg_df = pd.merge(ue_df, group_df)  # 最终为130264条,26列

        tmp = ueg_df['category_id'].copy()
        del ueg_df['category_id']
        ueg_df['category_id'] = tmp
        '''
        不考虑内存时的流利做法
        grouped = ueg_df.groupby(['user_id','group_id', 'venue_id', 'weekday','clock']) #可形成94332条独立的参与信息
        one_hot = pd.get_dummies(ueg_df['category_id'])
        column = ['c_' + str(i) for i in range(1, 7193)]
        one_hot.columns = column
        zip_ueg_df = pd.concat([ueg_df, one_hot], axis=1)
        zip_ueg_df.to_csv("zip_ueg_df.csv", encoding="utf-8")
        '''

        '''
        删除某些特征并调整index
        ueg_label= pd.merge(ueg_df, user_label_df, on=['user_id', 'event_id'])
        x = [1, 4, 7]
        ue_df.drop(ue_df.columns[x], axis=1, inplace=True)
        ue_df.drop_duplicates(keep='first', inplace=True)#剩余94392
        ue_df = ue_df.reset_index(drop=True)
        '''
        return ueg_df
    @classmethod
    # feature_v1
    def preprosess_df(self, ueg_df):
        # tran_list = ['user_id', 'event_id', 'group_id', 'venue_id', 'clock']
        date_deal = []
        for x in ueg_df['date']:
            tmp = x.split('-')
            tmp = tmp[0] + tmp[1] + tmp[2]
            date_deal.append(tmp)
        ueg_df['date'] = date_deal
        ueg_df['date'] = ueg_df['date'].astype(float)

        clock_deal = []
        for y in ueg_df['clock']:
            tmp = y.replace(':', '')
            clock_deal.append(tmp)
        ueg_df['clock'] = clock_deal
        ueg_df['clock'] = ueg_df['clock'].astype(float)

        tran_list = ['user_id','event_id', 'group_id', 'venue_id']
        for col in tran_list:
            col_float = []
            for i in ueg_df[col].values:
                tmp = i[2:]
                col_float.append(tmp)
            col_float = pd.Series(col_float)
            col_float = col_float.astype(float)
            ueg_df[col] = col_float

        return ueg_df
    @classmethod
    def sample_df(self, zip_event_df, group_df):
        # user-event
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
        ue_df = pd.merge(uecol_df, zip_event_df)
        ueg_df = pd.merge(ue_df, group_df, left_on=['group_id'])
        from sklearn.utils import shuffle
        ueg_df = shuffle(ueg_df)
        # from here!!
        ueg_sample = ueg_df.copy()
        ueg_sample = shuffle(ueg_sample)
        ueg_sample = ueg_sample.sample(frac=0.3)  # 39079
        ueg_sample = ueg_sample.reset_index(drop=True)
        onehot_sample = pd.get_dummies(ueg_sample['category_id'])
        column = ['c_' + str(i) for i in range(1, 6346)]
        onehot_sample.columns = column
        frames = [ueg_sample, onehot_sample]
        ueg_sample_onehot = pd.concat(frames, axis=1)
        return ueg_sample_onehot

    # 点子二
    @classmethod
    def generate_labeldf(self, zip_event_df):
        # 统计u-e关系总数
        ue_cnt = 0
        for u in edge_ue:
            for e in edge_ue[u]:
                ue_cnt += 1
        label_mat = np.zeros((ue_cnt, 7202), dtype=int)
        row_index = 0
        for u in edge_ue:
            for e in edge_ue[u]:
                tmp = list(zip_event_df[zip_event_df['event_id'] == e]['category_id'])
                col_index = tmp[0] - 1  # 矩阵下标从0开始的
                label_mat[row_index, col_index] = 1
                row_index += 1
        print("row_index = %d" % row_index)
        # categories实际只会用到7192
        column = ['catg_' + str(i) for i in range(1, 7203)]
        user_label_df = pd.DataFrame(label_mat, columns=column)
        user_index = []
        for u in edge_ue:
            for e in edge_ue[u]:
                user_index.append(u)
        print('len(user_index) = %d' % len(user_index))
        col_df = pd.DataFrame(user_index, columns=['user_id'])
        user_label_df = pd.concat([col_df, user_label_df], axis=1)
        # 3. user及其标签Dataframe

        # ueg_onehot = pd.get_dummies(ueg_df['category_id'])#!!所以是因为合并group时导致event需要重新归类，少了6个label
        # zip_ueg_df = pd.concat([ueg_onehot, ueg_df], axis=1)
        return user_label_df
    @classmethod
    def param_analyze(self):
        nx.average_clustering(trainG)  # 全图的聚类系数在0.355
        sum_degree = 0
        user_degree = []
        # 计算用户节点的平均度数
        i = 0
        for node in list(trainG.nodes):
            if trainG.nodes[node]['node_type'] == 'U':
                i += 1
                sum_degree += trainG.degree(node)
                user_degree.append(trainG.degree(node))
        ave_degree = sum_degree / i
        print("average degree of U: %d" % ave_degree)

user_object = User()
user_df, ueg_df = user_object.generate_uegdf(event_df, group_df)

ueg_df = user_object.preprosess_df(ueg_df)
#2018/12/13
#区别在于ueg_df是7192类，ueg2_df是6780类
ueg2_df = user_object.generate_uegdf(zip2_event_df, group_df)
ueg2_df = user_object.preprosess_df(ueg2_df)



