import os
import csv
import random
import threading
from concurrent.futures import ProcessPoolExecutor
import time 

lock = threading.Lock()

def parse_cnf(file_path):
    clauses = []
    num_vars = 0
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith('c') or line.strip() == '':
                continue
            if line.startswith('p'):
                parts = line.split()
                if len(parts) >= 3:
                    try:
                        num_vars = int(parts[2])
                    except ValueError:
                        pass
            else:
                try:
                    clause = [int(x) for x in line.strip().split() if x and x != '0']
                    if clause:
                        clauses.append(clause)
                except ValueError:
                    continue

    max_lit = max((abs(lit) for c in clauses for lit in c), default=0)
    num_vars = max(num_vars, max_lit)
    return clauses, num_vars


def check_clause(clause, assignment):
    
    return any(
        (assignment[abs(l)] if l > 0 else not assignment[abs(l)])
        for l in clause
    )


def calculate_break_count(var, assignment, clauses, var_to_clauses_map):
 
    break_count = 0
    assignment[var] = not assignment[var]
    for clause in var_to_clauses_map.get(var, []):
        if not check_clause(clause, assignment):
            break_count += 1
    assignment[var] = not assignment[var]
    return break_count


def walksat_optimized(clauses, num_vars, max_flips=500, max_tries=5, p=0.3):
    var_to_clauses_map = {i: [] for i in range(1, num_vars + 1)}
    for clause in clauses:
        for lit in clause:
            var_to_clauses_map[abs(lit)].append(clause)

    for _try in range(max_tries):
        assignment = [random.choice([True, False]) for _ in range(num_vars + 1)]
        unsat_clauses = [c for c in clauses if not check_clause(c, assignment)]

        for _ in range(max_flips):
            if not unsat_clauses:
                return True

            clause = random.choice(unsat_clauses)

            if random.random() < p:
                lit_to_flip = random.choice(clause)
                var_to_flip = abs(lit_to_flip)
            else:
                best_var = 0
                min_breaks = float("inf")
                for lit in clause:
                    var = abs(lit)
                    breaks = calculate_break_count(var, assignment, clauses, var_to_clauses_map)
                    if breaks < min_breaks:
                        min_breaks = breaks
                        best_var = var
                        if min_breaks == 0:
                            break
                var_to_flip = best_var

            assignment[var_to_flip] = not assignment[var_to_flip]
            affected_clauses = var_to_clauses_map.get(var_to_flip, [])

            for c in affected_clauses:
                is_sat = check_clause(c, assignment)
                if is_sat:
                    if c in unsat_clauses:
                        unsat_clauses.remove(c)
                else:
                    if c not in unsat_clauses:
                        unsat_clauses.append(c)

    return False


def process_file(file_info):
    idx, file, folder, output_file = file_info
    path = os.path.join(folder, file)

    try:
        clauses, num_vars = parse_cnf(path)
    except Exception as e:
        print(f"Error parsing {file}: {e}")
        return None

    start_time = time.perf_counter()
    sat = walksat_optimized(clauses, num_vars)
    end_time = time.perf_counter()
    runtime = end_time - start_time

    result_entry = {
        "instance": file,
        "solver": "WalkSAT_Optimized",
        "num_vars": num_vars,
        "num_clauses": len(clauses),
        "result": "SAT" if sat else "UNSAT",
        "runtime_seconds": round(runtime, 4)
    }

    with lock:
        write_header = not os.path.exists(output_file)
        with open(output_file, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=result_entry.keys())
            if write_header:
                writer.writeheader()
            writer.writerow(result_entry)

    print(f"[{idx}] {file} -> {result_entry['result']} ({runtime:.3f}s)")
    return result_entry


if __name__ == "__main__":
    folder = "instances/"
    output_file = "results_walksat.csv"

    if os.path.exists(output_file):
        os.remove(output_file)

    if not os.path.isdir(folder):
        print(f"Error: Instance folder '{folder}' not found.")
    else:
        cnf_files = [f for f in os.listdir(folder) if f.endswith(".cnf")]
        if not cnf_files:
            print(f"No .cnf files found in '{folder}'. Nothing to process.")
        else:
            file_info_list = [(i + 1, f, folder, output_file) for i, f in enumerate(cnf_files)]
            max_workers = min(8, os.cpu_count() or 4)
            print(f"Starting processing with {max_workers} worker processes...")

            with ProcessPoolExecutor(max_workers=max_workers) as executor:
                executor.map(process_file, file_info_list)

            print(f"\n WalkSAT results saved to '{output_file}'")
