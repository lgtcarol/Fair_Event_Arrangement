from AnalyData import *
from CreateNetwork import *
import pandas as pd
from datetime import date
import numpy as np
import copy

from src.lgt_v1.user_deal import *

'''2018/12/17 尝试一'''
# （建议用set而不是list）
u_choices = defaultdict(list)
for index, row in ueg_df.iterrows():  # 未经过preprosess_df函数
    now_u = row['user_id']
    now_e = row['event_id']
    venue = row['venue_id']
    weekday = row['weekday']
    clock = row['clock']
    choices = list(
        ueg_df[(ueg_df['venue_id'] == venue) & (ueg_df['date'] == date) & (ueg_df['clock'] == clock)]['event_id'])
    print("%s len:%d" % (now_u, len(choices)))
    for e in choices:
        if e == now_e:
            continue
        else:
            print("1")
            u_choices[now_u].append(e)

'''2018/12/17 尝试二'''
# 1. 将clock转换为clock_range
event_df['sum'] = 1
clock_count = event_df.groupby(['clock'], as_index=False)['sum'].agg({'count': np.sum})


def clock_bin(data):
    if data < '7:00':
        return 0
    elif data < '8:00':
        return 1
    elif data < '9:00':
        return 2
    elif data < '10:00':
        return 3
    elif data < '11:00':
        return 4
    elif data < '12:00':
        return 5
    elif data < '13:00':
        return 6
    elif data < '14:00':
        return 7
    elif data < '15:00':
        return 8
    elif data < '16:00':
        return 9
    elif data < '17:00':
        return 10
    elif data < '18:00':
        return 11
    elif data < '19:00':
        return 12
    elif data < '20:00':
        return 13
    elif data < '21:00':
        return 14
    elif data < '22:00':
        return 15
    else:
        return 16


event_df['clock_range'] = event_df['clock'].map(clock_bin)


# 2. 生成choices字典
def get_choices(now_e, event_df):
    now_row = event_df[event_df.event_id == now_e]
    if len(now_row) == 0:
        return []
    now_group = now_row['group_id'].values[0]
    now_venue = now_row['venue_id'].values[0]  # 下标是格式导致的取数方式
    now_weekday = now_row['weekday'].values[0]
    now_clock = now_row['clock_range'].values[0]
    valid_e = list(event_df[(event_df['group_id'] == now_group) & (event_df['venue_id'] == now_venue) & (
            event_df['weekday'] == now_weekday) & (event_df['clock_range'] == now_clock)]['event_id'])
    # valid_venue = event_df[event_df.venue_id.notnull()]
    # valid_weekday = valid_venue[valid_venue.weekday == now_weekday]
    # valid_clock = valid_weekday[valid_weekday.clock == now_clock]
    # valid_e = list(valid_clock['event_id'])
    # print("get_choices:%d" % len(valid_e))
    return valid_e


u_choices = defaultdict(list)
for u in edge_ue:
    now_u = u
    attended = list(edge_ue[u])
    choices = set()
    for e in attended:
        now_e = e
        e_choices = get_choices(now_e, event_df)
        if len(e_choices) == 0:  # 所以通过len(u_choices)可得到哪些用户无反例
            continue
        for each in e_choices:
            if each not in attended:
                choices.add(each)
    if len(choices) == 0:
        continue
    u_choices[now_u] = choices

# 3. 构造负样本集
u_info = []
e_info = []
for u in u_choices:
    allow_len = len(edge_ue[u])*1.2
    now_u = u
    cnt = 0
    for e in u_choices[u]:
        if(cnt < allow_len):
            now_e = e
            now_u_info = user_df[user_df.user_id==now_u].iloc[0,]
            now_e_info = event_df[event_df.event_id == now_e]
            u_info.append(now_u_info.values)
            e_info.append(now_e_info.values)
            cnt += 1

u_column = user_df.columns
u_df = pd.DataFrame(columns = u_column)
e_column = event_df.columns
e_df = pd.DataFrame(columns = e_column)
u_info = np.c_[list(u_info)]
e_info = np.c_[list(e_info)]
for i in range(4):
    u_df[u_df.columns[i]] = u_info[:,i]
for i in range(26):
    e_df[e_df.columns[i]] = e_info[:,i]

x = [1]
u_df.drop(u_df.columns[x], axis=1, inplace=True)
neg_ueg_df = pd.concat([u_df, e_df], axis=1)
#标识正负样本
ueg_df['class'] = 1
neg_ueg_df['class'] = 0

#2018/12/19
#1. 预处理
del ueg_df['event_id']
del neg_ueg_df['event_id']
del ueg_df['date']
del neg_ueg_df['date']
ueg_df['clock_h'] = pd.to_datetime(ueg_df.clock, format="%H:%M")
ueg_df['clock_h'] = pd.Index(ueg_df['clock_h']).hour
neg_ueg_df['clock_h'] = pd.to_datetime(neg_ueg_df.clock, format="%H:%M")
neg_ueg_df['clock_h'] = pd.Index(neg_ueg_df['clock_h']).hour
del ueg_df['clock']
del neg_ueg_df['clock']
def preprosess1_df(ueg_df):
    catcols = ['user_id', 'group_id', 'venue_id']
    for col in catcols:
        col_float = []
        for i in ueg_df[col].values:
            tmp = i[2:]
            col_float.append(tmp)
        col_float = pd.Series(col_float)
        col_float = col_float.astype(float)
        ueg_df[col] = col_float
    return ueg_df
ueg_df =preprosess1_df(ueg_df)
neg_ueg_df = preprosess1_df(neg_ueg_df)# 28cols
def adjust_colseq(ueg_df):
    tmp = ueg_df['class'].copy()
    del ueg_df['class']
    ueg_df['class'] = tmp
    return ueg_df
ueg_df = adjust_colseq(ueg_df)
neg_ueg_df = adjust_colseq(neg_ueg_df)
#先不离散化了
def preprosess2_df(ueg_df):
    dummies_wd = pd.get_dummies(ueg_df['weekday'], prefix='wd')
    dummies_cr = pd.get_dummies(ueg_df['clock_range'], prefix='cr')
    ueg_df = pd.concat([dummies_wd, dummies_cr], axis=1)
    ueg_df.drop(['weekday','clock_range'], axis=1,inplace=True)
    return ueg_df
ueg_df =preprosess2_df(ueg_df)
neg_ueg_df = preprosess2_df(neg_ueg_df)

#2. 加载模型
from sklearn.model_selection import train_test_split
X1_train, X1_test, y1_train, y1_test = train_test_split(ueg_df.ix[:, 0:27], ueg_df.ix[:,27], test_size=0.3, random_state=33)
X2_train, X2_test, y2_train, y2_test = train_test_split(neg_ueg_df.ix[:, 0:27], neg_ueg_df.ix[:,27], test_size=0.2, random_state=33)
X_train = pd.concat([X1_train, X2_train], axis=0)
X_test = pd.concat([X1_test, X2_test], axis=0)
y_train = pd.concat([y1_train, y2_train], axis=0)
y_test = pd.concat([y1_test, y2_test], axis=0)

from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier
# 标准化数据，保证每个维度的特征数据方差为1，均值为0。使得预测结果不会被某些维度过大的特征值而主导。
ss = StandardScaler()
X_train = ss.fit_transform(X_train)
X_test = ss.transform(X_test)
# 初始化LogisticRegression与SGDClassifier。
lr = LogisticRegression()
sgdc = SGDClassifier()

# 调用LogisticRegression中的fit函数/模块用来训练模型参数。
lr.fit(X_train, y_train)
# 使用训练好的模型lr对X_test进行预测，结果储存在变量lr_y_predict中。
lr_y_predict = lr.predict(X_test)

# 调用SGDClassifier中的fit函数/模块用来训练模型参数。
sgdc.fit(X_train, y_train)
# 使用训练好的模型sgdc对X_test进行预测，结果储存在变量sgdc_y_predict中。
sgdc_y_predict = sgdc.predict(X_test)

# 从sklearn.metrics里导入classification_report模块。
from sklearn.metrics import classification_report

# 使用逻辑斯蒂回归模型自带的评分函数score获得模型在测试集上的准确性结果。
print ('Accuracy of LR Classifier: %f' % lr.score(X_test, y_test))
# 利用classification_report模块获得LogisticRegression其他三个指标的结果。
print (classification_report(y_test, lr_y_predict))

 # 使用随机梯度下降模型自带的评分函数score获得模型在测试集上的准确性结果。
print ('Accuarcy of SGD Classifier: %f' %  sgdc.score(X_test, y_test))
# 利用classification_report模块获得SGDClassifier其他三个指标的结果。
print (classification_report(y_test, sgdc_y_predict, target_names=['N_attended', 'attended']))

