# -*- coding: utf-8 -*-
# __author__ = 'lgtcarol'

#zip_event_df, group_df <2018/12/3>
import pickle
import networkx as nx
import pandas as pd
from CreateNetwork import trainG

df_var = open('src/ltmp_vars/uegdf_var.pkl', 'rb')
zip_event_df = pickle.load(df_var)
group_df = pickle.load(df_var)
ueg_df = pickle.load(df_var)
df_var.close()
#检查下user重复 写变量，读出来验证，然后考虑拼凑（之后考虑one-hot）
ueg_sample_onehot = pd.read_csv("src/ltmp_vars/ueg_sample_onehot.csv")


'''11/14 融合event_tag & 生成dataframe'''
group_df.to_csv("dataset/group_df.csv", encoding="utf-8")
#虽函数名不太符合，但要实现的功能一样