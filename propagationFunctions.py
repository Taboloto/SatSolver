from utils import find_new_sentinels, opposite, print_literals


# Propagate every possible literal
def propagation_step(poli_literals, model, all_literals, level, conflicts, tmp_proof):
    flag = True
    while conflicts == [] and flag:
        flag = False
        for c in poli_literals:
            s1, s2 = c.sentinels
            if s1.value == False and s2.value == True:
                new_s = find_new_sentinels(c)
                if len(new_s) > 0:
                    c.sentinels = [new_s[0], s2]
                    flag = True
            elif s2.value == False and s1.value == True:
                new_s = find_new_sentinels(c)
                if len(new_s) > 0:
                    c.sentinels = [s1, new_s[0]]
                    flag = True
            elif s1.value == False and s2.value == None:
                new_s = find_new_sentinels(c)
                if len(new_s) > 0:
                    c.sentinels = [new_s[0], s2]
                    flag = True
                elif s2.key not in model:
                    s2.value = True
                    s2.level = level
                    s2.propagated = c.id
                    model.append(s2.key)
                    if opposite(s2) in all_literals.keys():
                        all_literals[opposite(s2)].value = False
                        all_literals[opposite(s2)].level = level
                        all_literals[opposite(s2)].propagated = c.id

                    flag = True
            elif s2.value == False and s1.value == None:
                new_s = find_new_sentinels(c)
                if len(new_s) > 0:
                    c.sentinels = [s1, new_s[0]]
                    flag = True
                elif s1.key not in model:
                    s1.value = True
                    s1.level = level
                    s1.propagated = c.id
                    model.append(s1.key)
                    if opposite(s1) in all_literals.keys():
                        all_literals[opposite(s1)].value = False
                        all_literals[opposite(s1)].level = level
                        all_literals[opposite(s1)].propagated = c.id
                    flag = True
            elif s1.value == False and s2.value == False:
                new_s = find_new_sentinels(c)
                if len(new_s) > 1:
                    c.sentinels = [new_s[0], new_s[1]]
                    flag = True
                elif len(new_s) == 1:
                    if new_s[0].value != True:
                        new_s[0].value = True
                        new_s[0].level = level
                        new_s[0].propagated = c.id
                        model.append(new_s[0].key)
                        if opposite(new_s[0]) in all_literals.keys():
                            all_literals[opposite(new_s[0])].value = False
                            all_literals[opposite(new_s[0])].level = level
                            all_literals[opposite(new_s[0])].propagated = c.id
                        flag = True
                else:
                    if level != 0:
                        conflicts.append(c)
                        break
                    else:
                        tmp_proof.append(print_literals(c))
                        conflicts.append("UNSAT")
                        break
        if conflicts != []:
            break
    return model


# Propagate a single literal
def single_propagation(s, level, model, all_literals, literal):
    l = literal
    s.value = True
    l.value = True
    l.level = level
    l.propagated = s.id
    l.decided = None
    model.append(l.key)
    if opposite(l) in all_literals.keys():
        all_literals[opposite(l)].value = False
        all_literals[opposite(l)].level = level
        all_literals[opposite(l)].decided = None
        all_literals[opposite(l)].propagated = s.id

    return model