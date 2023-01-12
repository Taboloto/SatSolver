from propagationFunctions import single_propagation
from utils import opposite


# Set clause value
def checkClause(c):
    answer = False
    for l in c.literals:
        if l.value is True:
            answer = True
            break
        elif l.value is None:
            answer = None
    return answer


# AND of all clauses of the problem
def checkValidity(all_clauses):
    answer = True
    for c in all_clauses.values():
        c.value = checkClause(c)
        if c.value is False:
            answer = False
        elif c.value is None:
            answer = None
            break

    return answer


# For each singlet in the formula it propagates the literal
def checkSinglets(singlets, model, level, all_literals):
    if len(singlets) == 1:
        s = singlets.pop()
        literal = s.literals[0]
        if literal not in model and opposite(literal) not in model:
            model = single_propagation(s, 0, model, all_literals, literal)
        return 0
    else:
        s = singlets.pop()
        literal = s.literals[0]
        if literal not in model and opposite(literal) not in model :
            model = single_propagation(s, 0, model, all_literals, literal)
            return checkSinglets(singlets, model, level, all_literals)
        return 0


# Check if a clause is an Assertion clause or not
def checkAssertion(model, all_literals, clause, level):
    literals_in_model = []
    for l in clause.literals:
        if opposite(l) in model and all_literals[opposite(l)].level == level:
            literals_in_model.append(l)
    return literals_in_model
