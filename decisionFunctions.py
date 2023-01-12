from utils import opposite


# Decides one literal, first literal not in model
def decision_step(poli_literals, model, all_literals, level):
    found = False
    for c in poli_literals:
        if c.value != True:
            for l in c.literals:
                if l.key not in model and opposite(l) not in model:
                    level += 1
                    c.value = True
                    found = True
                    model.append(l.key)
                    l.value = True
                    l.level = level
                    l.propagated = None
                    l.decided = True
                    if opposite(l) in all_literals.keys():
                        all_literals[opposite(l)].value = False
                        all_literals[opposite(l)].level = level
                        all_literals[opposite(l)].propagated = None
                        all_literals[opposite(l)].decided = True
                    break
        if found:
            break
    return model, level


# Decides one literal with VSIDS heuristic
def decision_step_VSIDS(model, all_literals, level, literals_counter):
    for l in literals_counter:
        if l not in model and opposite(all_literals[l]) not in model:
            literal_to_be_decided = l
            break

    l = literal_to_be_decided
    opposite_l = opposite(all_literals[l])

    level += 1
    model.append(l)
    all_literals[l].value = True
    all_literals[l].level = level
    all_literals[l].propagated = None
    all_literals[l].decided = True
    if opposite_l in all_literals.keys():
        all_literals[opposite_l].value = False
        all_literals[opposite_l].level = level
        all_literals[opposite_l].propagated = None
        all_literals[opposite_l].decided = True

    return model, level