# -*- coding:utf-8 -*-
import networkx as nx
import numpy as np
import json
from networkx.readwrite import json_graph
import pandas as pd
import codecs
import os
import scipy.stats as stats
from pprint import pprint


class seo_graph:

    def __init__(self):
        self.graph = nx.graph()
        self.userList = []

    def seo_graph_construction(self, nodes, edges, userList):

        pass

    def list_nodes(self):
        return self.graph.nodes(data=True)

    def list_edges(self):
        return self.graph.edges(data=True)

    def is_event(self, nodeId):
        pass

    def is_group(self, nodeId):
        pass

    def is_user(self, nodeId):
        pass

    def count_node_neighbor(self, nodeId, param1):
        pass

    def add_edge_attr(self, nodeId1, nodeId2, val):
        pass

    def update_score(self, node, val):
        pass

    def find_first_available_user(self):
        pass

    def has_open_events(self, nodeId):
        pass

    def check_user_groups(self, nodeId):
        pass

    def simplified_random_arrangement(self):
        pass

    def simplified_greedy_arrangement(self):
        pass

    def event_arrangement_random(self):
        pass

    def event_arrangement_greedy(self):
        pass
