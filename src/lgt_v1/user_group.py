'''添加user-group权重信息：Jaccard相似度'''
#示例：'G_456'和'U_50657'
for item_g in trainG_G:
    A = set(group_tags_raw[item_g])
    for item_u in trainG.neighbors(item_g):
        if trainG.nodes[item_u]['node_type'] == 'U':
            B = set(user_tags_raw[item_u])  # 获取一个用户的tags并转为set
            numerator = A & B
            denominator = A | B
            Jaccard_score = (len(numerator) / len(denominator))*1.0
            trainG[item_u][item_g]['weight'] = round(Jaccard_score, 3)


'''将每个group中成员Jaccard_score为0.0个数保存到node属性'''
for item_dictg in group_tags_raw:
    cnt = 0
    for item_u in trainG.neighbors(item_dictg):
        if(trainG[item_u][item_dictg]['weight'] > 0.0):
            cnt += 1
    trainG.nodes[item_dictg]['cap_zero'] = trainG.nodes[item_dictg]['num_of_u'] - cnt