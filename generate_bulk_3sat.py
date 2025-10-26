# generate_bulk_3sat_realistic.py
import random
import os

# Folder to save CNFs
folder = "instances/"
os.makedirs(folder, exist_ok=True)

# Parameters
num_new_instances = 1000        # total new instances
num_vars_options = [50, 60, 70, 80, 90, 100, 120, 150]  # variable sizes
clause_ratio_options = [3, 4, 5, 6]  # m/n ratio ranges
clause_size_options = [2, 3, 4]      # mostly 3-SAT, some 2- and 4-literal clauses

print(f"📂 Generating {num_new_instances} enhanced 3-SAT CNF instances...")

for i in range(1, num_new_instances + 1):
    num_vars = random.choice(num_vars_options)
    ratio = random.choice(clause_ratio_options)
    num_clauses = num_vars * ratio
    
    filename = f"random3sat_realistic_{i}.cnf"
    filepath = os.path.join(folder, filename)
    
    with open(filepath, 'w') as f:
        f.write(f"p cnf {num_vars} {num_clauses}\n")
        for _ in range(num_clauses):
            clause_size = random.choice(clause_size_options)
            clause = []
            for _ in range(clause_size):
                var = random.randint(1, num_vars)
                sign = random.choice([-1, 1])
                clause.append(str(sign * var))
            f.write(" ".join(clause) + " 0\n")
    
    if i % 100 == 0:
        print(f"✅ {i}/{num_new_instances} instances generated")

print(f"🎉 Completed generating {num_new_instances} enhanced 3-SAT CNF files in '{folder}'")
