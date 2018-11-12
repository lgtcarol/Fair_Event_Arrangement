import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def scatter_visual(x, y, title='Scatter Plot', xlabel='x', ylabel='y'):
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    # Set title
    ax1.set_title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    sValue=x*10
    ax1.scatter(x,y, s=sValue, marker=".")
    plt.show()

if __name__=="__main__":
    u_e = pd.read_csv('./data/user_event.csv', header=None)
    u_e.columns = [0,1]
    print(u_e.head())
    attenders_per_event= u_e.groupby(1).count().reset_index()
    attenders_per_event.columns = [1, 'count']
    attenders_count = attenders_per_event.groupby('count').count().reset_index()
    attenders_count.columns = ['user_counts', 'count']


    data_x = list(attenders_count['count'])
    data_y = list(attenders_count['user_counts'])
    scatter_visual(data_x, data_y)


