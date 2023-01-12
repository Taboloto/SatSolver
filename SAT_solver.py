# SAT_SOLVER
# AUTHOR: LORENZO TABARELLI
# RELEASE_DATE: 10-01-2023

# IMPORTS
import os
from solver import solver
from readFunctions import *
import time
import sys

def main():
    # INITIALIZATIONS
    sys.setrecursionlimit(10000)
    try:
        args = sys.argv
        path = args[1]
        result_filename = path.split('/')[-2]
        heuristic = args[2]
        print_proof = args[3]
    except:
        raise Exception("Wrong parameters, please try again")

    directory = os.listdir(path)
    file_counter, counter_unsat, counter_sat = 0, 0, 0
    total_time = time.time()
    result = ''

    # PROGRAM
    try:
        # For each file .cnf in directory
        for f in directory:
            model = []
            conflicts = []
            file_counter += 1
            result += f"Reading from {f} --- file number {file_counter} \n"
            print(f'Reading from {f} --- file number {file_counter} \n')
            start_time = time.time()

            # Read from file .cnf
            clauses, all_literals, all_clauses, singlets, formula_raw, proof, literals_counter = read_from_cnf(f"{path}{f}")
            literals_counter = dict(sorted(literals_counter.items(), key=lambda x: x[1], reverse=True))

            # Solve the formula
            answer, model, proof, level = solver(all_literals, all_clauses, clauses, model, singlets,
                                                 conflicts, proof, literals_counter, heuristic)

            partial_time = time.time() - start_time
            minutes, seconds = divmod(partial_time, 60)
            if minutes > 1:
                minutes_string = f" {int(minutes)} minutes"
            elif minutes == 1:
                minutes_string = f" {int(minutes)} minute"
            else:
                minutes_string = ""

            # Print result for each file .cnf
            if print_proof == '-p':
                result += f" ====={minutes_string} {seconds:.3f} seconds  ===== \n" \
                          f" ===== ANSWER  {answer} ===== \n" \
                          f" ===== MODEL  {model} ===== \n" \
                          f" ===== LEVEL  {level} =====\n" \
                          f" ===== PROOF  {print_proof(proof)} ===== \n \n"
                print(f'  ===== {minutes_string} {seconds:.3f} seconds ===== \n',
                      f' ===== ANSWER  {answer} ===== \n',
                      f' ===== MODEL  {model} ===== \n',
                      f' ===== LEVEL  {level} ===== \n',
                      f' ===== PROOF  {print_proof(proof)} ===== \n')
            else:
                result += f" ====={minutes_string} {seconds:.3f} seconds  ===== \n" \
                          f" ===== ANSWER  {answer} ===== \n" \
                          f" ===== MODEL  {model} ===== \n" \
                          f" ===== LEVEL  {level} =====\n" \
                          f" ===== PROOF  []  ===== \n \n"
                print(f'  ===== {minutes_string} {seconds:.3f} seconds ===== \n',
                      f' ===== ANSWER  {answer} ===== \n',
                      f' ===== MODEL  {model} ===== \n',
                      f' ===== LEVEL  {level} ===== \n',
                      f' ===== PROOF  [] ===== \n')

            # Increment counters
            if answer == "UNSAT" or answer is False:
                counter_unsat += 1
            else:
                counter_sat += 1

        total_time = time.time() - total_time
        minutes, seconds = divmod(total_time, 60)
        if minutes > 1:
            minutes_string = f" {int(minutes)} minutes"
        elif minutes == 1:
            minutes_string = f" {int(minutes)} minute"
        else:
            minutes_string = ""

        # Print the stats at the end
        result += f"\n [--------------------------------------------------------------------------------------------------] \n"\
                  f" ===== {counter_sat + counter_unsat} files FINISHED in{minutes_string} {seconds:.3f} seconds ===== \n" \
                  f" ===== HEURISTIC  {heuristic} ===== \n" \
                  f" ===== SAT  {counter_sat} ===== \n" \
                  f" ===== UNSAT  {counter_unsat} ===== \n"
        print(f'  ===== {counter_sat + counter_unsat} files FINISHED in{minutes_string} {seconds:.3f} seconds ===== \n',
              f' ===== HEURISTIC  {heuristic} ===== \n',
              f' ===== SAT  {counter_sat} ===== \n',
              f' ===== UNSAT  {counter_unsat} ===== \n')

    except:
        raise Exception("Something went wrong!!!")

    # Save result on file "directory".txt
    f = open(f"./Benchmarks/results/{result_filename}_{heuristic}.txt", "w")
    f.write(result)
    f.close()


if __name__ == '__main__':
    main()