def optimizeroutine(spotposition): #spotposition type: {97: [21.2910619, -157.843481],..., 98: [21.2629444, -157.8041957]}
    edges = dict()
    ids = list(spotposition.keys())
    for i in range(len(ids)):
        edges[ids[i]] = dict()
    for i in range(len(ids)):
        for j in range(i+1,len(ids)):
            posi = spotposition[ids[i]]
            posj = spotposition[ids[j]]
            dis = abs(posi[0]-posj[0])*100**2+abs(posi[1]-posj[1])*100**2
            edges[ids[i]][ids[j]] = dis
            edges[ids[j]][ids[i]] = dis
    routine = []
    routine.append(ids[0])
    hq = []
    for edge in edges[ids[0]]:
        hq.append([edges[ids[0]][edge],edge])
    heapq.heapify(hq)
    while len(hq)>0:
        dis,nxt = heapq.heappop(hq)
        routine.append(nxt)
        for i in range(len(hq)):
            vertices = hq[i]
            if edges[nxt][vertices[1]]<vertices[0]:
                hq[i][0] = edges[nxt][vertices[1]]
    return routine