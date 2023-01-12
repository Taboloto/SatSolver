from utils import opposite, print_literals
from propagationFunctions import single_propagation
from structures import Clause


# Learn the new clause (add in all_clauses)
def acknowledge(conflict_clause, all_clauses, poli_literals, literals_counter, min_index):
    for l in conflict_clause.literals:
        literals_counter[l.key] += 1
    all_clauses[conflict_clause.id] = conflict_clause
    if len(conflict_clause.literals) > 1:
        poli_literals.append(conflict_clause)
    literals_counter = dict(sorted(literals_counter.items(), key=lambda x: x[1], reverse=True))
    return literals_counter, all_clauses, min_index


# BackJump to a specific literal
def backjump(model, conflict_clause, all_literals, literals_in_model, min_index):
    level_to_jump = 0
    index_to_jump = min_index
    for l in conflict_clause.literals:
        if l.level >= level_to_jump and opposite(l) in model and l not in literals_in_model and model.index(
                opposite(l)) >= index_to_jump:
            level_to_jump = l.level
            literal_to_jump = l
            index_to_jump = model.index(opposite(literal_to_jump))

    if index_to_jump != 0:
        removed = model[index_to_jump+1:]
        model = model[:index_to_jump+1]
    else:
        removed = model
        model = []

    for l in removed:
        all_literals[l].value = None
        all_literals[l].level = None
        all_literals[l].propagated = None
        all_literals[l].decided = None
        if opposite(all_literals[l]) in all_literals.keys():
            all_literals[opposite(all_literals[l])].value = None
            all_literals[opposite(all_literals[l])].level = None
            all_literals[opposite(all_literals[l])].propagated = None
            all_literals[opposite(all_literals[l])].decided = None
    model = single_propagation(conflict_clause, level_to_jump, model, all_literals, literals_in_model[0])
    level = level_to_jump
    return model, level, all_literals


# Explanation between 2 clauses
def explanation(c1, c2, all_literals, all_clauses, l, clauses_count, tmp_proof):
    new_clause_literals = []
    for lit in c2.literals:
        if lit.key != l and lit.key != opposite(all_literals[l]):
            new_clause_literals.append(lit)
    for lit in c1.literals:
        if lit.key != l and lit.key != opposite(all_literals[l]) and lit not in new_clause_literals:
            new_clause_literals.append(lit)
    clauses_count += 1
    new_clause = Clause(new_clause_literals, clauses_count)
    all_clauses[new_clause.id] = new_clause
    proof_string = f'{print_literals(c1)} {print_literals(c2)}'
    tmp_proof.append(proof_string)
    proof_string = f'{print_literals(new_clause)}'
    tmp_proof.append(proof_string)

    return new_clause, clauses_count, all_literals, all_clauses
