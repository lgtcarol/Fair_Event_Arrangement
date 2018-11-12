# -*- coding: utf-8 -*-
import numpy as np


def stable_marriage(mat1, mat2):
    n = len(mat1)
    proposals = []
    rejected = range(n)
    candids = [n+1 for i in range(n)]
    #new_candids = [n+1 for i in range(n)]

    props = {}
    #j = 0
    j = [1 for i in range(n)]
    while len(props) < n:
        #j += 1
        #props = {}
        for i in rejected:
            #props.append((i, mat1[i].index(j)))
            if mat1[i].index(j[i]) in props:
                props[mat1[i].index(j[i])] += [i]
            else:
                props[mat1[i].index(j[i])] = [i]
            #candids[mat1[i].index(j)] = min(candids[mat1[i].index(j)], mat2[i][mat1[i].index(j)])
        #print(props)
        for i in range(n):
            if candids[i] == n+1:
                continue
            else:
                props[i] += candids[i]
        #print(props)
        rejected = []
        for i in props:
            if len(props[i]) == 1:
                continue
            else:
                prio = props[i][0]
                for k in props[i]:
                    if mat2[k][i] < mat2[prio][i]:
                        rejected.append(prio)
                        prio = k
                    elif mat2[k][i] > mat2[prio][i]:
                        rejected.append(k)
                props[i] = [prio]
                for k in rejected:
                    j[k] += 1
            pass

        pass
    return props

    pass


def run(M1, M2):
    # test 1
    m1 = [[1,2,3,4],[1,2,3,4],[3,1,2,4],[2,3,1,4]]
    m2 = [[3,2,1,3],[4,3,2,4],[1,4,3,2],[2,1,4,1]]
    print(stable_marriage(m1, m2))

    # test 2
    m1 = [[1,2,3,4],[1,4,3,2],[2,1,3,4],[4,2,3,1]]
    m2 = [[3,3,2,3],[4,1,3,2],[2,4,4,1],[1,2,1,4]]
    print(stable_marriage(m1,m2))

    print(stable_marriage(M1, M2))


if __name__=="__main__":
    # given M1, M2
    # run()
    pass