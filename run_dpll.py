import os
import csv
import time
from pysat.solvers import Glucose3
from pysat.formula import CNF
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, TimeoutError
import threading

lock = threading.Lock()

def solve_instance(file_info):
    idx, file, folder, output_file, timeout = file_info
    path = os.path.join(folder, file)

    result_entry = {
        "instance": file,
        "solver": "DPLL",
        "num_vars": 0,
        "num_clauses": 0,
        "runtime_seconds": None,
        "result": "UNKNOWN"
    }

    try:
        formula = CNF(from_file=path)
        result_entry["num_vars"] = formula.nv
        result_entry["num_clauses"] = len(formula.clauses)

        solver = Glucose3()
        for clause in formula.clauses:
            solver.add_clause(clause)

        def run_solver():
            return solver.solve()

        start_time = time.time()
        with ThreadPoolExecutor(max_workers=1) as ex:
            future = ex.submit(run_solver)
            try:
                sat = future.result(timeout=timeout)
                result_entry["result"] = "SAT" if sat else "UNSAT"
            except TimeoutError:
                result_entry["result"] = "TIMEOUT"
            except Exception as e:
                result_entry["result"] = "ERROR"
                print(f" Error on {file}: {e}")
        end_time = time.time()

        result_entry["runtime_seconds"] = round(end_time - start_time, 4)

    except Exception as e:
        result_entry["result"] = "ERROR"
        print(f" Error on {file}: {e}")

    with lock:
        write_header = not os.path.exists(output_file)
        with open(output_file, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=result_entry.keys())
            if write_header:
                writer.writeheader()
            writer.writerow(result_entry)

    print(f"[{idx}] {file} -> {result_entry['result']} ({result_entry['runtime_seconds']}s)")
    return result_entry


if __name__ == "__main__":
    folder = "instances/"
    output_file = "results_dpll.csv"
    timeout_seconds = 5

    if os.path.exists(output_file):
        os.remove(output_file)

    cnf_files = [f for f in os.listdir(folder) if f.endswith(".cnf")]
    file_info_list = [(i+1, f, folder, output_file, timeout_seconds) for i, f in enumerate(cnf_files)]
    max_workers = min(8, os.cpu_count() or 4)

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        executor.map(solve_instance, file_info_list)

    print(f"\n DPLL results saved to '{output_file}'")
