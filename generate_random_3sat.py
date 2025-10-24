# generate_random_3sat.py
import random
import os

def generate_random_3sat(num_vars, num_clauses, filename):
    with open(filename, "w") as f:
        f.write(f"p cnf {num_vars} {num_clauses}\n")
        for _ in range(num_clauses):
            # ensure 3 distinct variables per clause for variety
            vars_ = random.sample(range(1, num_vars+1), 3)
            lits = [str(v * random.choice([-1, 1])) for v in vars_]
            f.write(" ".join(lits) + " 0\n")

os.makedirs("instances", exist_ok=True)
for i in range(1, 11):
    fname = os.path.join("instances", f"random3sat{i}.cnf")
    generate_random_3sat(num_vars=50, num_clauses=200, filename=fname)
    print("Wrote", fname)
