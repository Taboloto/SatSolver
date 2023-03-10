# SAT_SOLVER

## Intro
This program is an assignment to achieve an exam at the University of Verona.

## Structure
+ SAT_solver.py: this file contains the main, and it's the one that has to be run
+ solver.py: contains the complete CDCL procedure
+ decisionFunctions.py: contains the different decision functions, with heuristic or not.
+ propagationFunctions.py: contains the single propagation function and the propagation step function. Here is where the **"watched literals"** procedure is implemented.
+ checkFunctions.py: contains the checkValidity, checkClause, checkSinglets and checkAssertion functions.
+ conflitcFunctions.py: contains the acknowledge function, backjump function and explanation function.
+ readFunctions.py: contains the function that read the files **.cnf**
+ structures.py: contains the two C-like structures for Literals and Clauses.
+ utils.py: contains the printFunctions and other useful functions like **opposite()** or **find_new_sentinels()**.

## How to use
First of all install the libraries (sys, time, os, etc...) if not yet done.

It's very easy to use this program:

1. Create a directory (i.e. "Benchmarks") where you put every **file.cnf** you want to solve (FILE MUST BE .CNF).


2. Choose which heuristic you want (' ' Standard, 'VSIDS' Vsids)


3. Choose if you want the proof for each UNSAT problem (' ' no proof, '-p' proof)


4. Run the program as follows: <br>
`
python SAT_solver.py "directory_path" "heuristic" "proof"
`
   

5. The results will be saved as .txt where is reported:
+ Time spent for each file.cnf
+ Answer (SAT / UNSAT)
+ Model (as list of literals)
+ Level (level reached)
+ Proof (if "-p" in args, as list of clauses)
+ Time spent for the whole run

### Example of file.cnf
c This Formular is generated by mcnf <br>
c <br>
c    horn? no  <br>
c    forced? no  <br>
c    mixed sat? no  <br>
c    clause length = 3  <br>
c <br>
p cnf 20  91 <br>
-10 -16 5 0 <br>
16 -6 5 0 <br>
-17 -14 -18 0 <br>
-10 -15 19 0 <br>
-1 -9 -18 0 <br>
3 7 -6 0 <br>
... <br>
+ the lines that starts with c are comments
+ the line that starts with p describes the characteristics of the formula (cnf (conjunctive Normal Form), 20 (number of literals), 91 (number of clauses))
+ each line is a clause and has to end with a '0'
### Developer
_LORENZO TABARELLI_
