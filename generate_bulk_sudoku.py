# generate_bulk_sudoku_realistic.py
import os

# Folder to save Sudoku CNFs
folder = "instances/"
os.makedirs(folder, exist_ok=True)

# Parameters
num_instances = 200        # number of Sudoku CNF files
grid_size = 9              # 9x9 standard Sudoku

def sudoku_to_cnf(grid_size):
    """Generate CNF clauses for a standard empty Sudoku puzzle"""
    clauses = []
    N = grid_size
    cells = range(1, N+1)

    # Cell constraints: each cell has at least one value
    for r in cells:
        for c in cells:
            clause = [r*N*N + c*N + v for v in range(1, N+1)]
            clauses.append(clause)

    # Row constraints: no repeated numbers
    for r in cells:
        for v in cells:
            for c1 in cells:
                for c2 in cells:
                    if c1 < c2:
                        clauses.append([-((r-1)*N*N + (c1-1)*N + v), -((r-1)*N*N + (c2-1)*N + v)])

    # Column constraints: no repeated numbers
    for c in cells:
        for v in cells:
            for r1 in cells:
                for r2 in cells:
                    if r1 < r2:
                        clauses.append([-((r1-1)*N*N + (c-1)*N + v), -((r2-1)*N*N + (c-1)*N + v)])

    # Subgrid constraints: no repeated numbers in 3x3 blocks
    block_size = int(N**0.5)
    for br in range(0, N, block_size):
        for bc in range(0, N, block_size):
            for v in cells:
                block_cells = [(r, c) for r in range(br+1, br+block_size+1) for c in range(bc+1, bc+block_size+1)]
                for i in range(len(block_cells)):
                    for j in range(i+1, len(block_cells)):
                        r1, c1 = block_cells[i]
                        r2, c2 = block_cells[j]
                        clauses.append([-((r1-1)*N*N + (c1-1)*N + v), -((r2-1)*N*N + (c2-1)*N + v)])
    return clauses

print(f"📂 Generating {num_instances} Sudoku CNF instances...")

for i in range(1, num_instances + 1):
    filename = f"sudoku_realistic_{i}.cnf"
    filepath = os.path.join(folder, filename)

    clauses = sudoku_to_cnf(grid_size)
    num_vars = grid_size**3
    num_clauses = len(clauses)

    with open(filepath, 'w') as f:
        f.write(f"p cnf {num_vars} {num_clauses}\n")
        for clause in clauses:
            f.write(" ".join(map(str, clause)) + " 0\n")
    
    if i % 20 == 0:
        print(f"✅ {i}/{num_instances} instances generated")

print(f"🎉 Completed generating {num_instances} Sudoku CNF files in '{folder}'")
