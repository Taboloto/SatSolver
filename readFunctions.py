from utils import opposite
from structures import *


# Read from a file .cnf
def read_from_cnf(filename):
    proof = list()
    formula_raw = list()
    all_literals = dict()
    all_clauses = dict()
    singlets = list()
    literals_set = set()
    literals_counter = dict()
    clauses = list()
    i = 1
    with open(filename) as f:
        lines = f.readlines()
        for clause_raw in lines:
            clause_raw = " ".join(clause_raw.split())
            title = clause_raw.split('\n')[0].split(' ')
            if title[0] == '':
                title = title[1:]
            if title[0] == 'c' or title[0] == '0':
                continue
            elif title[0] == 'p':
                clause_count = int(title[3])
                literals_count = int(title[2])
            else:
                if title[0] == '%':
                    break
                literals_list = []
                literals_list_raw = []
                clause = clause_raw.split('\n')[0]
                literals_raw = clause.split(" ")[:-1]
                if len(literals_raw) == 1:
                    if literals_raw[0] not in literals_counter.keys():
                        literals_counter[literals_raw[0]] = 1
                    else:
                        literals_counter[literals_raw[0]] += 1
                    if literals_raw[0] not in list(all_literals.keys()):
                        new_literal = Literal(literals_raw[0])
                        all_literals[new_literal.key] = new_literal
                    else:
                        new_literal = all_literals[literals_raw[0]]
                    if opposite(new_literal) in formula_raw:
                        formula_raw.append(new_literal.key)
                        proof.append(new_literal.key)
                        proof.append(opposite(new_literal))
                        break
                    new_clause = Clause([new_literal], i)
                    singlets.append(new_clause)
                    all_clauses[new_clause.id] = new_clause
                    clauses.append(new_clause)
                    if opposite(new_literal) not in list(all_literals.keys()):
                        literals_set.add(new_literal)
                    formula_raw.append(new_literal.key)

                else:
                    for l in literals_raw:
                        if l != '':
                            if l not in literals_counter.keys():
                                literals_counter[l] = 1
                            else:
                                literals_counter[l] += 1
                            if l not in list(all_literals.keys()):
                                new_literal = Literal(l)
                                all_literals[new_literal.key] = new_literal
                            else:
                                new_literal = all_literals[l]
                            literals_list.append(new_literal)
                            literals_list_raw.append(new_literal.key)
                            if opposite(new_literal) not in list(all_literals.keys()):
                                literals_set.add(new_literal)
                        # print(literals_list)
                    new_clause = Clause(literals_list, i)
                    all_clauses[new_clause.id] = new_clause
                    clauses.append(new_clause)
                    formula_raw.append(literals_list_raw)
                i += 1
        if proof != []:
            return clauses, all_literals, all_clauses, singlets, formula_raw, proof, literals_counter
        if len(clauses) != clause_count or len(literals_set) != literals_count:
            raise Exception(f'Reading from file {filename} \n'
                            f'Wrong number or clauses or literals: \n'
                            f'{len(clauses)} clauses expected {clause_count} \n'
                            f'{len(literals_set)} literals expected {literals_count}')
        f.close()
    return clauses, all_literals, all_clauses, singlets, formula_raw, proof, literals_counter


