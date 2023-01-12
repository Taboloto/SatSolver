# Find new sentinels for a clause
def find_new_sentinels(clause):
    s1, s2 = clause.sentinels
    potential_sentinels = []
    for l in clause.literals:
        if len(potential_sentinels) == 2:
            break
        if l.value != False and l.key != s1.key and l.key != s2.key:
            potential_sentinels.append(l)
    return potential_sentinels


# Return the opposite of a literal
def opposite(l):
    if '-' in l.key:
        return l.key.split('-')[1]
    else:
        return f'-{l.key}'


def print_literals(clause):
    list = []
    for l in clause.literals:
        list.append(l.key)
    return list


def print_all_clauses(all_clauses):
    clauses = []
    for c in all_clauses:
        clauses.append(print_literals(all_clauses[c]))
    return clauses


def print_proof(raw_proof):
    proof = ""
    if len(raw_proof) > 1:
        for i in range(int((len(raw_proof) - 1) / 2)):
            proof += str(raw_proof[i * 2]) + '\n'
            proof += str(raw_proof[i * 2 + 1]) + '\n'
            proof += "------------------------------------------------------ \n"
        proof += str(raw_proof[-1]) + '\n'
    return proof