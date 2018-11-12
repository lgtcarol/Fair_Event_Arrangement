# -*- coding: utf-8 -*-

import pandas as pd
import os
import codecs
import networkx as nx


def event2node(event_file):
    if not os.path.exists(event_file):
        print('This file does not exist!')
        return

    with codecs.open(event_file, 'r', encoding='utf-8') as fr:
        df = pd.read_csv(fr)
        pass
    pass
    return df


def member2node(member_file):
    if not os.path.exists(member_file):
        print('This file does not exist!')
        return

    with codecs.open(member_file, 'r', encoding='utf-8') as fr:
        df = pd.read_csv(fr)
        pass
    pass
    return df
    pass


def group2node():
    pass


def get_top(group, n):
    return group.sort_index(ascending=True)[:n]


if __name__ == "__main__":
    from pprint import pprint
    """df = event2node('../data/total_member.csv')
    pprint(len(df))
    df = df[['id', 'name', 'topics', 'city', 'status']]
    df['capacity'] = 2
    df['count'] = 0
    pprint(len(df.drop_duplicates(['id'])))
    df = df.drop_duplicates(['id'])"""
    #df.to_csv('../data/filtered_total_members.csv', index=False)
    #graph = nx.Graph()
    #for i in range(len(df)/10000):
        #graph.add_node(df.ix[i]['id'], name=df.ix[i]['name'], type='event')

    #pprint(graph.nodes(data=True))
    import matplotlib.pyplot as plt
    member_group_file = '../data/event_group.csv'#
    if not os.path.exists(member_group_file):
        print('This file does not exist!')
    else:
        with codecs.open(member_group_file, 'r', encoding='utf-8') as fr:
            df = pd.read_csv(fr)
            print(df[:5])
            grouped = df['id'].groupby(df['group']).size()
            #fig = plt.figure()
            #ax = fig.add_subplot(1,1,1)
            #ax.plot(grouped)
            #print get_top(grouped, 100)
            #grouped_cut = pd.cut(sorted(grouped, reverse=True), 1000)
            pprint(len(grouped))
            #pprint(grouped_cut)
            pd.Series(sorted(grouped, reverse=True)).plot()
            plt.show()
            pass
    pass
