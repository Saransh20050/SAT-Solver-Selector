# SAT-Solver-Selector

Instructions to run:

1. Clone the Repository
git clone https://github.com/Saransh20050/SAT-Solver-Selector.git
cd SAT-Solver-Selector

2. Install Dependencies
   
pip install -r requirements.txt

Step 1: Generate Random 3-CNF Instances
python generate_bulk_3sat.py

Step 2: Generate Sudoku-Based SAT Instances
python generate_bulk_sudoku.py

Step 3: Run DPLL Solver
python run_dpll.py

Results are stored in a CSV file (e.g., results_dpll.csv).

Step 4: Run WalkSAT Solver
python run_walksat.py

Results are stored in a CSV file (e.g., results_walksat.csv).

Step 5: Merge and Train the Classifier
python merge_and_train.py

-------------------------------------------------------------------------------------------------------------------------------------------------------------------

This project implements a Meta-Algorithmic Solver Selection system for Boolean Satisfiability (SAT) problems. Using supervised machine learning, we classify Conjunctive Normal Form (CNF) instances to predict which of two core solvers—DPLL (Complete) or WalkSAT (Incomplete)—is expected to yield the fastest runtime.

The goal is to optimize problem-solving efficiency by routing instances to the most suitable algorithm based on their intrinsic features, effectively creating a basic, high-level solver portfolio.
This project was collaboratively completed in 4 major stages:

1.Generate 300 Sudoku CNF files and 1000 random 3-SAT .cnf files.
2.Run DPLL and record runtime & success/fail, outputting results to a CSV file.
3.Run WalkSAT and record runtime & success/fail outputting another CSV file.
4.Add features.Train ML model to predict which solver performs better.














