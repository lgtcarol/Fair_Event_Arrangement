import networkx as nx
import numpy as np
import json
from networkx.readwrite import json_graph
import pandas as pd
import codecs
import os
import scipy.stats as stats
import time
import random
import matplotlib.pyplot as plt
from pprint import pprint

#graph = nx.Graph()
#users = []


def seo_graph_construction():
    """with open('./data/graph_construction.json', 'r') as f:
        s = json.load(f)
        # the same graph defined in the outer scope
        graph = json_graph.node_link_graph(s)
        return graph"""
    graph = nx.Graph()
    member_dir_path = './data/NY_info/group_members/'
    members_path = [member_dir_path + filename for filename in os.listdir(member_dir_path)]
    event_dir_path = './data/events/'
    events_path = [event_dir_path + filename for filename in os.listdir(event_dir_path)]
    group_dir_path = './data/group/'
    groups_path = [group_dir_path + filename for filename in os.listdir(group_dir_path)]
    group_member_dir_path = './data/NY_info/group_members/'
    #group_member_path = ['./data/NY_info/group_members/Pokemon-Go-Events-New-York-City.csv',
    #                     './data/NY_info/group_members/1-Million-Cups-NYC.csv']
    group_member_path = members_path

    df_member = pd.DataFrame()
    for eachfile in members_path[:0]:
        df_member = df_member.append(pd.read_csv(eachfile), ignore_index=True)

    # add user nodes
    for i in range(len(df_member)):
        graph.add_node(df_member.ix[i]['id'], name=df_member.ix[i]['name'], type='user')

    """df_event = pd.DataFrame()
    for eachfile in events_path[:0]:
        df_event = df_event.append(pd.read_csv(eachfile), ignore_index=True)
    # add event nodes
    for i in range(len(df_event)):
        graph.add_node(df_event.ix[i]['id'], name=df_event.ix[i]['name'], type='event')"""

    df_group = pd.DataFrame()
    for eachfile in groups_path[:0]:
        df_group = df_group.append(pd.read_csv(eachfile), ignore_index=True)
    # add group nodes
    for i in range(len(df_group)):
        graph.add_node(df_group.ix[i]['urlname'], name=df_group.ix[i]['urlname'], type='group')

    # add group-member edges
    df_group_member = pd.DataFrame()
    for eachfile in group_member_path[:40]:
        df_group_member = df_group_member.append(pd.read_csv(eachfile), ignore_index=True)
    for i in range(len(df_group_member)):
        graph.add_node(df_group_member.ix[i]['id'], name=df_group_member.ix[i]['name'], type='user')
        graph.add_node(df_group_member.ix[i]['group'], name=df_group_member.ix[i]['group'], type='group')
        graph.add_edge(df_group_member.ix[i]['group'], df_group_member.ix[i]['id'])

    return graph


def is_event(g, node):
    """
    to return a bool value, telling a node in graph being or not being a event node
    :param g: a constructed graph
    :param node:
    """
    if node not in g.nodes():
        print('Not a node in the graph')
        return False
    else:
        if g.node[node]['type'] == 'event':
            return True
        else:
            return False


def is_group(g, node):
    """
    to return a bool value, telling a node in graph being or not being a group node
    :param g, a constructed graph
    :param node
    """
    if node not in g.nodes():
        print('Not a node in the graph')
        return False
    elif g.node[node]['type'] == 'group':
        return True
    else:
        return False


def is_user(g, node):
    """
    to return a bool value, telling a node in graph being or not being a user node
    :param g, a constructed graph
    :param node
    """
    if node not in g.nodes():
        print('Not a node in the graph')
        return False
    elif g.node[node]['type'] == 'user':
        return True
    else:
        return False


def count_user_neighbors(g, user, param1, param2=None):

    """
    :param user, a user node in graph; if not, return -1
    :param param1, if equals to '', to count all neighbor nodes
                    if param1 == 'group', to count all group neighbor nodes
                    if param1 == 'event', to count all event neighbor nodes

    :param param2  if 'present', to count the currently present status neighbor nodes
                    not used for the moment
    """
    if not is_user(g, user):
        print('Not a user node !')
        return -1

    count = []
    if param1 == '':
        for neighbor in g.neighbors(user):
            count.append(neighbor)
    elif param1 == 'event':
        for neighbor in g.neighbors(user):
            if is_event(g, neighbor) and not param2:
                count.append(neighbor)
            elif is_event(g, neighbor) and param2 == 'present':
                if g.node[neighbor]['status'] == 'present':
                    count.append(neighbor)
    elif param1 == 'group':
        for neighbor in g.neighbors(user):
            if is_group(g, neighbor):
                count.append(neighbor)
    return count


def add_edge_attr(g, node1, node2, attr):
    """
    :param g: a constructed graph
    :param node1: a node id (often referring to a user node, or a group node)
    :param node2: a node id (often referring to a group node, or a event node)
    :param attr: a value to add to this edge
    :return:
    """
    if node1 not in g.nodes():
        print("Node 1 is not a valid node in the graph")
        return
    if node2 not in g.nodes():
        print("Node 2 is not a valid node in the graph")
        return
    if (node1, node2) not in g.edges():
        print("Not an existed edge in the graph")
        return
    g.edge[node1][node2]['weight'] = attr
    pass


def update_score(g, node, param, value=0):
    """
    :param g
    :param node
    :param param
    """
    alpha1 = 0.5
    alpha2 = 0.5
    beta = 1.0

    if param == 'group':
        if is_group(g, node):
            """
            updating group score needs to do:
            1. update the group score
            2. update each group-user score in the same formula
            """
            g.node[node]['score'] = alpha1 * g.node[node]['score'] + alpha2
            for nbr_user in g.neighbors(node):
                if is_user(g, nbr_user):
                    g.edge(node, nbr_user)['score'] = alpha1 * g.edge(node, nbr_user)['score'] + alpha2
        else:
            print('please input a valid group')
    elif param == 'user':
        if is_user(g, node):
            #print g.node[node]['score']
            g.node[node]['score'] = (1-beta) * g.node[node]['score'] + beta * value
            #print g.node[node]['score']
        else:
            print('please input a valid user')
    pass


def update_score_iter(historical_score, interest_score, parametre):
    return parametre * historical_score + (1 - parametre) * interest_score


def calculate_array_similarity(arr1, arr2):
    return 1 - np.sqrt((arr1 - arr2) * (arr1 - arr2))/len(arr1)


def find_first_available_user(g, users, begin_index):
    """
    :param g: a constructed graph
    :param users: a users' list
    :param begin_index
    :return:

    in the Users' list, find and return the first available ( unassigned
    during this round) user in the sorted list from an assigned index
    if no available user node is found, return 'None'
    """
    # test if the given list users is a valid users list
    for i in range(begin_index, len(users)):
        # each user node has an attribute 'capacity'
        # if a user's assigned events number is smaller than its capacity
        # then this is an available user
        if len(count_user_neighbors(g, users[i], 'event')) < g.node[users[i]]['capacity']:
            return users[i]
    return 'None'


# for groups, if a group has open events, then it returns a list of
# accessible events for users ready to register for
# else, it returns 'None' meaning all the events are unavailable
# at this moment
# open means:
# - the event status is present
# - and event's users neighbor is less than its upper_bound
def has_open_events(g, group):
    """
    a group node is connected to several events which it created
    the events list stores inside ___
    test if the given group is a valid node in the graph
    :param g
    :param group

    """
    events = []
    if not is_group(g, group):
        print('Please input a valid group')
        return 'None'

    for nbr in g.neighbors(group):
        if is_event(g, nbr):
            #neighbor_users_count = len([u for u in g.neighbors(nbr) if is_user(g, u)])
            if g.node[nbr]['count'] < g.node[nbr]['capacity']:
                events.append(nbr)
    return events


# check if the group list of the user hsas events to push
# - no, update the specific group score
# - yes, do nothing
# - return an ordered list of all active groups (which have available events)
# actually, this is a punishment action for groups' non-action
def check_user_groups(g, user):
    events = []
    for group in g.neighbors(user):
        if is_group(g, group):
            if len(has_open_events(g, group)) == 0:
                #update_score()
                pass
            else:
                # merge open events into one events' list
                events += [(e, group) for e in has_open_events(g, group)]
    return events


# return a node's score value when applying a graph.nodes(data=True)
# function
def key_rule(node):
    return (node[1]).get('score')


# in the simplified arrangement, no need to sort the users' list
def simplified_arrangement_random(g, userlist, contras):
    total_available_events =[]
    for node in g.nodes():
        if is_event(g, node) and g.node[node]['count'] < g.node[node]['capacity']:
            total_available_events.append(node)

    new_edges = []

    for user in userlist:
        #
        random_event_index = np.random.randint(0, len(total_available_events)-1)
        g.node[user]['count'] += 1
        g.node[total_available_events[random_event_index]]['count'] += 1
        for neighbor in g.neighbors(total_available_events[random_event_index]):
            if is_group(g, neighbor):
                event_in_group = neighbor
                break

        # a new parameter gamma
        gamma = 0.5
        value = gamma * g.edge[event_in_group][total_available_events[random_event_index]]['weight']

        update_score(g, user, 'user', value=value)

        g.add_edge(user, total_available_events[random_event_index])
        new_edges.append((user, (total_available_events[random_event_index], event_in_group)))
        if g.node[total_available_events[random_event_index]]['count'] == g.node[total_available_events[random_event_index]]['capacity']:
            total_available_events.pop(random_event_index)
    #import matplotlib.pyplot as plt
    #nx.draw_networkx_nodes(g, pos=nx.spring_layout(g), node)
    return (g, new_edges)
    pass


def simplified_arrangement_greedy(g, userlist, PrefM, contras):
    # PrefM is a matrix for recording users preferences for each event
    total_available_events = []
    for node in g.nodes():
        if is_event(g, node) and g.node[node]['count'] < g.node[node]['capacity']:
            total_available_events.append(node)

    new_edges = []


    for user in userlist:

        greedy_event = total_available_events[0]
        for event in total_available_events:
            if PrefM.ix[user][greedy_event] < PrefM.ix[user][event]:
                greedy_event = event

        g.node[user]['count'] += 1
        g.node[greedy_event]['count'] += 1
        for neighbor in g.neighbors(greedy_event):
            if is_group(g, neighbor):
                event_in_group = neighbor
                break

        # a new parameter gamma
        gamma = 0.5
        value = gamma * g.edge[event_in_group][greedy_event]['weight']

        update_score(g, user, 'user', value=value)

        g.add_edge(user, greedy_event)
        new_edges.append((user, (greedy_event, event_in_group), value))
        if g.node[greedy_event]['count'] == \
                g.node[greedy_event]['capacity']:
            total_available_events.pop(total_available_events.index(greedy_event))
    # import matplotlib.pyplot as plt
    # nx.draw_networkx_nodes(g, pos=nx.spring_layout(g), node)
    return (g, new_edges)
    pass
    pass


def contradiction(contras, event1, event2):
    # given a contradiction matrix
    #pprint(contras)
    if not contras:
        return False
    if (event1, event2) in contras:
        return True
    else:
        return False
    pass


def contradiction_pair_gen(eventlist, ratio):
    count = int(len(eventlist) * ratio)
    result = []
    for i in range(count):
        pair = random.sample(eventlist, 2)
        result.append((pair[0], pair[1]))
    #pprint(result)
    return result
    pass


def pref_matrix_gen(gpickle_name):
    g = nx.read_gpickle(gpickle_name)
    pprint(g.edges(data=True))
    users = [e for e in g.nodes() if is_user(g, e)]
    events = [e for e in g.nodes() if is_event(g, e)]
    prefM = pd.DataFrame(0.0, index=users, columns=events)

    pprint(g.nodes(data=True))

    for edge in g.edges():
        if is_user(g, edge[0]):
            if is_group(g,edge[1]):
                events_tmp = [e for e in g.neighbors(edge[1]) if is_event(g, e)]
                for e in events_tmp:
                    #pprint(g.edge[edge[0]][edge[1]]['weight'])
                    #pprint(g.edge[edge[1]][e]['weight'])
                    #prefM.ix[edge[0]][e] = 1
                    #pprint(float(g.edge[edge[0]][edge[1]]['weight']) * float(g.edge[edge[1]][e]['weight']))
                    prefM.ix[edge[0]][e] = float(g.edge[edge[0]][edge[1]]['weight']) * float(g.edge[edge[1]][e]['weight'])
            if is_event(g, edge[1]):
                prefM.ix[edge[0]][edge[1]] = float(g.edge[edge[0]][edge[1]]['weight'])
    pprint(prefM)
    return prefM
    pass


def baseline_arrangement(g, prefM, contras):
    result_edges = []
    userlist = [user for user in g.nodes() if
                (is_user(g, user) and len(count_user_neighbors(g, user, 'event')) < g.node[user]['capacity'])]
    if not userlist:
        return result_edges
    g, new_greedy_edges = simplified_arrangement_greedy(g, userlist, prefM, contras)
    result_edges += new_greedy_edges

    baseline_arrangement(g, prefM, contras)
    return g, result_edges
    pass


def events_arrangement(g, prefM, contras):
    result_edges = []
    userlist = [user for user in g.nodes() if (is_user(g, user) and len(count_user_neighbors(g, user, 'event')) < g.node[user]['capacity'])]
    while len(userlist) > 0:
        # use built-in function to sort users list by key = score value
        userlist = sorted(userlist, key=lambda user: g.node[user]['score'], reverse=True)

        user = find_first_available_user(g, userlist, 0)
        visited = []
        checked = []

        while len(visited)+len(checked) < len(userlist):
            if checked != []:
                checked.append(user)
                user = find_first_available_user(g, userlist, userlist.index(user) + 1)
                continue
            user_group_list = check_user_groups(g, user)
            if not user_group_list:
                # if there is no group with available events
                if user not in checked:
                    #update_score()
                    checked.append(user)
                    #sorted(userlist)
            else:
                # arrange an event to the user
                open_events = sorted(user_group_list, key=lambda event_group:
                           g.edge[event_group[0]][event_group[1]]['weight']*g.edge[user][event_group[1]]['weight']
                           )

                # contradiction judging
                for i in range(len(open_events)):
                    exist_contra = False
                    for pair in result_edges:
                        if pair[0] == user:
                            if contradiction(contras, pair[1], open_events[i]):
                                exist_contra = True
                                break
                            else:
                                continue
                        else:
                            continue
                    if exist_contra:
                        continue
                    else:
                        e_final = open_events[i]
                        break

                g.add_edge(user, e_final[0])
                g.node[user]['count'] += 1
                g.node[e_final[0]]['count'] += 1

                #print(g.edges(data=True))
                #print(g.nodes(data=True))

                # update user score
                edge_weight = g.edge[user][e_final[1]]['weight'] * g.edge[e_final[1]][e_final[0]]['weight']
                update_score(g, user, 'user', edge_weight)

                result_edges.append((user, e_final))
                visited.append(user)

            user = find_first_available_user(g, userlist, userlist.index(user)+1)


        g, new_random_edges = simplified_arrangement_random(g, checked, contras)
        result_edges += new_random_edges

        # update
        tmp_userlist = []
        for user in userlist:
            if g.node[user]['count'] < g.node[user]['capacity']:
                tmp_userlist.append(user)
        userlist = tmp_userlist

    #from pprint import pprint
    #pprint(result_edges)

    return (g, [edge for edge in g.edges() if is_user(g, edge[0]) and is_event(g, edge[1])])


def events_arrangement_greedy(g, PrefM, contras):
    result_edges = []
    userlist = [user for user in g.nodes() if (is_user(g, user) and len(count_user_neighbors(g, user, 'event')) < g.node[user]['capacity'])]
    while len(userlist) > 0:
        # use built-in function to sort users list by key = score value
        userlist = sorted(userlist, key=lambda user: g.node[user]['score'], reverse=True)

        user = find_first_available_user(g, userlist, 0)
        visited = []
        checked = []

        while len(visited)+len(checked) < len(userlist):
            if checked != []:
                checked.append(user)
                user = find_first_available_user(g, userlist, userlist.index(user) + 1)
                continue
            user_group_list = check_user_groups(g, user)
            if not user_group_list:
                # if there is no group with available events
                if user not in checked:
                    #update_score()
                    checked.append(user)
                    #sorted(userlist)
            else:
                # arrange an event to the user
                open_events = sorted(user_group_list, key=lambda event_group:
                           g.edge[event_group[0]][event_group[1]]['weight']*g.edge[user][event_group[1]]['weight']
                           )

                # contradiction judging
                for i in range(len(open_events)):
                    exist_contra = False
                    for pair in result_edges:
                        if pair[0] == user:
                            if contradiction(contras, pair[1], open_events[i]):
                                exist_contra = True
                                break
                            else:
                                continue
                        else:
                            continue
                    if exist_contra:
                        continue
                    else:
                        e_final = open_events[i]
                        break

                g.add_edge(user, e_final[0])
                g.node[user]['count'] += 1
                g.node[e_final[0]]['count'] += 1

                #print(g.edges(data=True))
                #print(g.nodes(data=True))

                # update user score
                edge_weight = g.edge[user][e_final[1]]['weight'] * g.edge[e_final[1]][e_final[0]]['weight']
                update_score(g, user, 'user', edge_weight)

                result_edges.append((user, e_final, edge_weight))
                visited.append(user)
            user = find_first_available_user(g, userlist, userlist.index(user)+1)

        g, new_random_edges = simplified_arrangement_greedy(g, checked, PrefM, contras)
        result_edges += new_random_edges

        # update
        tmp_userlist = []
        for user in userlist:
            if g.node[user]['count'] < g.node[user]['capacity']:
                tmp_userlist.append(user)
        userlist = tmp_userlist

    #from pprint import pprint
    #pprint(result_edges)

    return (g, [edge for edge in g.edges() if is_user(g, edge[0]) and is_event(g, edge[1])])

def min_cost_flow(G):
    res = {}
    CM = G.get_conflict_matrix()
    userlist = G.get_users()
    events = G.get_events()
    min_delta = min(len(userlist), len(events))
    max_delta = max()
    pass

def random_graph_construction(scale):
    user_num, group_num, event_num = scale

    userList = range(1, user_num+1)
    groupList = range(user_num+1, user_num+group_num+1)
    eventList = range((user_num+group_num)+1, (user_num+group_num+event_num)+1)

    #user_per_group_range = np.random.randint(1, len(userList)/len(groupList))
    scale = len(userList) / len(groupList)
    user_group_count = [int(e) for e in stats.expon.rvs(scale=scale, size=len(userList))]
    edges = []

    g = nx.Graph()

    for user in userList:
        groups = np.random.randint(low=(user_num)+1, high=(user_num+group_num), size=user_group_count[user-1])
        user_score = 0
        for group in groups:
            user_group_score = np.random.uniform()
            edges.append((user, group, {'weight': user_group_score}))
            user_score += user_group_score
        g.add_node(user, type='user', capacity=4, count=0, score=user_score)

    for event in eventList:
        group = np.random.randint(low=(user_num)+1, high=(user_num+group_num))
        edges.append((group, event, {'weight': np.random.uniform()}))

    #g = nx.Graph()
    #g.add_nodes_from(userList, type='user', capacity=2, count=0)
    g.add_nodes_from(groupList, type='group')
    g.add_nodes_from(eventList, type='event', capacity=4, count=0)
    g.add_edges_from(edges)

    #import matplotlib.pyplot as plt
    #plt.figure()
    #position = nx.fruchterman_reingold_layout(g)
    #color = [1 for i in range(user_num)]+[2 for i in range(group_num)] + [3 for i in range(event_num)]
    #nx.draw_networkx_nodes(g, pos=position, nodelist=userList, node_size=100, node_color='pink')
    #nx.draw_networkx_nodes(g, pos=position, nodelist=groupList, node_size=100, node_color='turquoise')
    #nx.draw_networkx_nodes(g, pos=position, nodelist=eventList, node_size=100, node_color='coral')
    #nx.draw_networkx_edges(g, pos=position, edgelist=edges)
    #nx.draw_networkx(g, pos=position, nodesize=50,  nodecolor=color)
    #plt.show()
    from pprint import pprint
    pprint(g.nodes(data=True))
    nx.write_gpickle(g, './data/graphs/%d-%d-%d.gpickle' % (user_num, group_num, event_num))
    return g

def running_time_cal(func, g, prefM, contras):
    start = time.time()
    func(g, prefM, contras)
    end = time.time()
    return str(end - start)


def plot_graph(g1, position, new_edges=None):
    users = [u for u in g1.nodes() if is_user(g1, u)]
    userList = [u for u in g1.nodes() if is_user(g1, u)]
    groupList = [gr for gr in g1.nodes() if is_group(g1, gr)]
    eventList = [e for e in g1.nodes() if is_event(g1, e)]
    edges = [edge for edge in g1.edges()]

    #position = nx.fruchterman_reingold_layout(g1)
    plt.figure()
    # color = [1 for i in range(user_num)] + [2 for i in range(group_num)] + [3 for i in range(event_num)]
    nx.draw_networkx_nodes(g1, pos=position, nodelist=userList, node_size=30, node_color='red')
    nx.draw_networkx_nodes(g1, pos=position, nodelist=groupList, node_size=30, node_color='blue')
    nx.draw_networkx_nodes(g1, pos=position, nodelist=eventList, node_size=30, node_color='yellow')
    nx.draw_networkx_edges(g1, pos=position, edgelist=edges)
    if new_edges != None:
        nx.draw_networkx_edges(g1, pos=position, edgelist=new_edges, edge_color='orange')


def total_utility(g):
    users = [e for e in g.nodes() if is_user(g, e)]
    #pprint(users)
    userscoreList = [g.node[user]['score'] for user in users]
    #pprint(userscoreList)

    beta = 0.5
    sum1 = 0.0
    sum2 = 0.0
    for score in userscoreList:
        sum1 += score
        sum2 += score**2.0
    mean = sum1/len(userscoreList)
    var = sum2/len(userscoreList) - mean**2.0

    return sum1 - beta*var
    pass

if __name__ == '__main__':
    #array = [2, 4, 6, 23, 56, 33]
    #print(sorted(array)[0])
    from pprint import pprint
    #graph = seo_graph_construction()
    #pprint(graph.nodes(data=True))
    #pprint(graph.edges())
    #pprint(graph.node[191258350.0]['type'])
    #pprint(is_user(graph, 191258350.0))



    #random_graph_construction((100, 11, 160))
    #random_graph_construction((100, 15, 160))
    #random_graph_construction((100, 12, 160))
    #random_graph_construction((100, 13, 160))
    #random_graph_construction((100, 14, 160))
    #g1 = random_graph_construction((100, 200, 200))
    g1 = nx.read_gpickle('./data/graphs/30-14-50.gpickle')
    #pref_matrix_gen('./data/graphs/15-5-20.gpickle')
    #pprint(g1.edges(data=True))
    #position = nx.fruchterman_reingold_layout(g1)
    #plot_graph(g1, position)

    prefM = pref_matrix_gen('./data/graphs/30-14-50.gpickle')
    eventlist = [e for e in g1.nodes() if is_event(g1, e)]
    contras = contradiction_pair_gen(eventlist, 0.0)
    #events_arrangement_greedy(g1)

    #g1, new_edges = simplified_arrangement_random(g1, users)
    #g1, new_edges = events_arrangement(g1)
    #pprint(running_time_cal(baseline_arrangement, g1, prefM, contras))
    """
    Run time comparation:
    """
    g1 = nx.read_gpickle('./data/graphs/30-14-50.gpickle')
    pprint(running_time_cal(events_arrangement_greedy,g1, prefM, contras))
    g1 = nx.read_gpickle('./data/graphs/30-14-50.gpickle')
    pprint(running_time_cal(events_arrangement, g1, prefM, contras))
    g1 = nx.read_gpickle('./data/graphs/30-14-50.gpickle')
    pprint(running_time_cal(baseline_arrangement,g1, prefM, contras))

    #pprint(g1.nodes(data=True))
    #pprint(g1.edges(data=True))
    #plot_graph(g1, position, new_edges)
    #plt.show()

    """
    Total utility comparation:
    """

    g1 = nx.read_gpickle('./data/graphs/20-10-40.gpickle')
    g1, new_edges = events_arrangement_greedy(g1, prefM, contras)
    pprint(total_utility(g1))
    g1 = nx.read_gpickle('./data/graphs/20-10-40.gpickle')
    g1, new_edges = events_arrangement(g1, prefM, contras)
    pprint(total_utility(g1))
    g1 = nx.read_gpickle('./data/graphs/20-10-40.gpickle')
    g1, new_edges = baseline_arrangement(g1, prefM, contras)
    pprint(total_utility(g1))

    pass
