def findCombo(dic, code, cur):
    if code == 0:
        return cur
    keys = list(dic.keys())
    for i in range(len(keys)-1, -1, -1):
        # keys[i]
        # dic[keys[i]]
        if keys[i]<=code:
            dic2=dic.copy()
            code-=keys[i]
            if dic[keys[i]] == 'nc':
                dic2[64] = ''
            elif dic[keys[i]] == 'pf':
                dic2[32] = ''
            cur.append(dic[keys[i]])
            del dic2[keys[i]]
            return findCombo(dic2, code, cur)