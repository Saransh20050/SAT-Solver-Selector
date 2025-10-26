# SAT-Solver-Selector
This project implements a Meta-Algorithmic Solver Selection system for Boolean Satisfiability (SAT) problems. Using supervised machine learning, we classify Conjunctive Normal Form (CNF) instances to predict which of two core solvers—DPLL (Complete) or WalkSAT (Incomplete)—is expected to yield the fastest runtime.

The goal is to optimize problem-solving efficiency by routing instances to the most suitable algorithm based on their intrinsic features, effectively creating a basic, high-level solver portfolio.
This project was collaboratively completed in 4 major stages:

1.Generate 300 Sudoku CNF files and 1000 random 3-SAT .cnf files.
2.Run DPLL and record runtime & success/fail, outputting results to a CSV file.
3.Run WalkSAT and record runtime & success/fail outputting another CSV file.
4.Add features.Train ML model to predict which solver performs better.











