import random

def generate_sudoku_cnf(filename):
    num_vars = 81
    num_clauses = random.randint(200, 400)
    with open(filename, 'w') as f:
        f.write(f"p cnf {num_vars} {num_clauses}\n")
        for _ in range(num_clauses):
            clause = [str(random.randint(1, num_vars) * random.choice([-1, 1])) for _ in range(3)]
            f.write(" ".join(clause) + " 0\n")

for i in range(1, 11):
    fname = f"sudoku_{i}.cnf"
    generate_sudoku_cnf(fname)
    print(f"Generated {fname}")
