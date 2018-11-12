import networkx as nx
from networkx import Graph
import pandas as pd


class social_graph:
    def __init__(self):
        self.graph = Graph()

    #def __repr__(self):
    #   return

    # add a node set of the same type
    def add_nodes(self, df_nodes, type,capacity=int('Inf')):
        for i in range(len(df_nodes)):
            self.graph.add_node(df_nodes.ix[i]['id'], name=df_nodes.ix[i]['name'], type=type,capacity=capacity)

    def get_events(self):
        events = [e for e in self.graph.nodes() if self.get_node_type(e) == 'event']
        return events

    def get_users(self):
        users = [e for e in self.graph.nodes() if self.get_node_type(e) == 'user']
        return users

    # get a node type in social graph
    def get_node_type(self, node):
        """
        to return a bool value, telling a node in graph being or not being a event node
        :param g: a constructed graph
        :param node:
        """
        if node not in self.graph.nodes():
            print('Not a node in the graph')
            return False
        else:
            if self.graph.node[node]['type'] == 'event':
                return 'event'
            elif self.graph.node[node]['type'] == 'user':
                return 'user'
            else:
                return 'group'

    def add_edges_attrs(self, edge_dict):
        for edge in edge_dict:
            self.add_edge_attr(edge[0], edge[1], edge_dict[edge])
        pass

    # add edge attr
    def add_edge_attr(self, node1, node2, attr):
        """
        :param g: a constructed graph
        :param node1: a node id (often referring to a user node, or a group node)
        :param node2: a node id (often referring to a group node, or a event node)
        :param attr: a value to add to this edge
        :return:
        """
        if node1 not in self.graph.nodes():
            print("Node 1 is not a valid node in the graph")
            return
        if node2 not in self.graph.nodes():
            print("Node 2 is not a valid node in the graph")
            return
        if (node1, node2) not in g.edges():
            print("Not an existed edge in the graph")
            return
        self.graph.edge[node1][node2]['weight'] = attr
        pass

    def _init_conflict_matrix(self):
        events = [e for e in self.graph.nodes() if self.get_node_type(e) == 'event']
        self.CM = pd.DataFrame(False, columns=events, index=events, dtype=bool)
        for e in events:
            self.CM[e][e] = True
        pass

    def set_conflict_matrix(self, cfs):
        for cf in cfs:
            self.CM[cf[0]][cf[1]] = True
        return self.CM

    def get_conflict_matrix(self):
        if not self.CM:
            self._init_conflict_matrix()
        return self.CM


    # count node neightcount neighbor
    def count_node_neighbors(self, node, param1, param2=None):

        """
        :param user, a user node in graph; if not, return -1
        :param param1, if equals to '', to count all neighbor nodes
                        if param1 == 'group', to count all group neighbor nodes
                        if param1 == 'event', to count all event neighbor nodes

        :param param2  if 'present', to count the currently present status neighbor nodes
                        not used for the moment
        """
        if node not in self.graph.nodes():
            print('Not a node in the graph !')
            return -1

        # TO DO
        count = []
        if param1 == '':
            for neighbor in g.neighbors(node):
                count.append(neighbor)
        elif param1 == 'event':
            for neighbor in self.graph.neighbors(node):
                if self.get_node_type(neighbor)==param1 and not param2:
                    count.append(neighbor)
                elif self.get_node_type(neighbor) == param1 and param2 == 'present':
                    if g.node[neighbor]['status'] == 'present':
                        count.append(neighbor)
        elif param1 == 'group':
            for neighbor in g.neighbors(node):
                if self.get_node_type(neighbor) == 'group':
                    count.append(neighbor)
        return count

    # for groups, if a group has open events, then it returns a list of
    # accessible events for users ready to register for
    # else, it returns 'None' meaning all the events are unavailable
    # at this moment
    # open means:
    # - the event status is present
    # - and event's users neighbor is less than its upper_bound
    def has_open_events(self, group):
        """
        a group node is connected to several events which it created
        the events list stores inside ___
        test if the given group is a valid node in the graph
        :param g
        :param group

        """
        events = []
        if not self.get_node_type(group) == 'group':
            print('Please input a valid group')
            return 'None'

        for nbr in self.graph.neighbors(group):
            if self.get_node_type(group) == 'event':
                # neighbor_users_count = len([u for u in g.neighbors(nbr) if is_user(g, u)])
                if self.graph.node[nbr]['count'] < self.graph.node[nbr]['capacity']:
                    events.append(nbr)
        return events

    # check if the group list of the user has events to push
    # - no, update the specific group score
    # - yes, do nothing
    # - return an ordered list of all active groups (which have available events)
    # actually, this is a punishment action for groups' non-action
    def check_user_groups(self, user):
        events = []
        for group in g.neighbors(user):
            if self.get_node_type(group) == 'group':
                if len(self.has_open_events(group)) == 0:
                    # update_score()
                    pass
                else:
                    # merge open events into one events' list
                    events += [(e, group) for e in self.has_open_events(group)]
        return events