from CreateNetwork import trainG
'''测试图中各类节点个数'''
node_u = 0
node_g = 0
node_e = 0
for node in trainG.nodes():
    if trainG.nodes[node]['node_type'] == 'U':
        node_u += 1
    elif trainG.nodes[node]['node_type'] == 'G':
        node_g += 1
    elif trainG.nodes[node]['node_type'] == 'E':
        node_e += 1
    else:
        continue

'''测试图中各类连边数目'''
#group-user和group-event
edge_gu = 0
edge_ge = 0
for g in trainG.nodes():
    if trainG.nodes[g]['node_type'] == 'G':
        for item in trainG.neighbors(g):
            if trainG.nodes[item]['node_type'] == 'U':
                edge_gu += 1
            elif trainG.nodes[item]['node_type'] == 'E':
                edge_ge += 1
            else:
                continue
#event-user
edge_eu = 0
for e in trainG.nodes():
    if trainG.nodes[e]['node_type'] == 'E':
        for u in trainG.neighbors(e):
            if trainG.nodes[u]['node_type'] == 'U':
                edge_eu += 1


