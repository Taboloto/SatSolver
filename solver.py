import time

from checkFunctions import checkSinglets, checkValidity, checkAssertion
from utils import opposite, print_literals, print_all_clauses
from propagationFunctions import propagation_step
from decisionFunctions import decision_step, decision_step_VSIDS
from conflictFunctions import acknowledge, backjump, explanation

# Solver function (Main function that returns ANSWER, MODEL, LEVEL, PROOF)


def solver(all_literals, all_clauses, clauses, model, singlets, conflicts, proof, literals_counter, heuristic):
    # Variable's initialization
    level = 0
    tmp_proof = []
    answer = None
    poli_literals = [i for i in clauses if i not in singlets]

    # Check if there are singlets
    if len(singlets) > 0:
        min_index = len(singlets)
    else:
        min_index = 0
    clauses_count = len(all_clauses)

    # Cicle until SAT or UNSAT
    while answer is None:
        # Propagation of singlets at level 0
        while len(singlets) > 0:
            checkSinglets(singlets, model, level, all_literals)

        # Check if SAT, UNSAT, None
        answer = checkValidity(all_clauses)
        if answer is True or answer is False:
            break

        # Decision step
        if heuristic == 'VSIDS':
            model, level = decision_step_VSIDS(model, all_literals, level, literals_counter)
        else:
            model, level = decision_step(poli_literals, model, all_literals, level)

        # Propagation step
        model = propagation_step(poli_literals, model, all_literals, level, conflicts, tmp_proof)

        # Cicle until zero conflict or UNSAT
        while conflicts != [] and conflicts != ["UNSAT"]:
            # Check if conflict is assertion
            literals_in_model = checkAssertion(model, all_literals, conflicts[0], level)

            # Assertion
            if len(literals_in_model) == 1:
                conflict_clause = conflicts.pop()

                # Acknowledge
                literals_counter, all_clauses, min_index = acknowledge(conflict_clause, all_clauses, poli_literals,
                                                                       literals_counter, min_index)

                # BackJump
                model, level, all_literals = backjump(model, conflict_clause, all_literals, literals_in_model,
                                                      min_index)

                # Propagation
                model = propagation_step(poli_literals, model, all_literals, level, conflicts, tmp_proof)

            # Not Assertion
            else:
                # Find latest literal on model that give conflict
                conflict_literal = literals_in_model[0]
                for l in literals_in_model:
                    if model.index(opposite(l)) > model.index(opposite(conflict_literal)):
                        conflict_literal = l

                # Literal is not decided
                if not conflict_literal.decided:
                    # Explanation
                    new_clause, clauses_count, all_literals, all_clauses = explanation(conflicts[0], all_clauses[
                        conflict_literal.propagated],
                                                                                       all_literals, all_clauses,
                                                                                       conflict_literal.key,
                                                                                       clauses_count, tmp_proof)
                    # Update conflict list
                    conflicts = [new_clause]

                    # Update model and literals
                    model.remove(opposite(conflict_literal))
                    all_literals[opposite(conflict_literal)].value = None
                    all_literals[opposite(conflict_literal)].level = None
                    all_literals[opposite(conflict_literal)].decided = None
                    all_literals[opposite(conflict_literal)].propagated = None
                    conflict_literal.value = None
                    conflict_literal.level = None
                    conflict_literal.decided = None
                    conflict_literal.propagated = None

                # Literal is decided
                else:
                    conflicts = []
                    removed = model[model.index(opposite(conflict_literal)):]
                    model = model[:model.index(opposite(conflict_literal))]

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
                    level -= 1

    # last check on answer
    if not answer or "UNSAT" in conflicts:
        answer = "UNSAT"
        level = 0
        model = []
        proof = tmp_proof
    else:
        answer = "SAT"

    return answer, model, proof, level
