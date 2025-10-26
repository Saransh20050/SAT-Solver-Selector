import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
# Using imblearn for standardized oversampling
from imblearn.over_sampling import RandomOverSampler
import joblib 

# --- Configuration ---
DPLL_SOLVER_NAME = "DPLL (Class 0)"
WALKSAT_SOLVER_NAME = "WalkSAT (Class 1)"

print("Loading solver results...")

# --- Load both solver result files ---
try:
    dpll_df = pd.read_csv("results_dpll.csv")
    walksat_df = pd.read_csv("results_walksat.csv")
except FileNotFoundError:
    print("Error: Ensure 'results_dpll.csv' and 'results_walksat.csv' are present.")
    exit()

if 'runtime_seconds' not in dpll_df.columns or 'runtime_seconds' not in walksat_df.columns:
    print("CRITICAL ERROR: Runtime column 'runtime_seconds' not found. Cannot determine best solver.")
    exit()

print("DPLL columns:", dpll_df.columns.tolist())
print("WalkSAT columns:", walksat_df.columns.tolist())

merged = pd.merge(
    dpll_df,
    walksat_df,
    on="instance",
    suffixes=("_dpll", "_walksat")
)
print(f"Merged {len(merged)} instances successfully.")


merged["ratio_dpll"] = merged["num_clauses_dpll"] / (merged["num_vars_dpll"] + 1e-6)
merged["ratio_walksat"] = merged["num_clauses_walksat"] / (merged["num_vars_walksat"] + 1e-6)
merged["var_diff"] = merged["num_vars_dpll"] - merged["num_vars_walksat"]
merged["clause_diff"] = merged["num_clauses_dpll"] - merged["num_clauses_walksat"]
merged["var_ratio"] = merged["num_vars_dpll"] / (merged["num_vars_walksat"] + 1e-6)
merged["clause_ratio"] = merged["num_clauses_dpll"] / (merged["num_clauses_walksat"] + 1e-6)
merged["vars_times_clauses_dpll"] = merged["num_vars_dpll"] * merged["num_clauses_dpll"]
merged["clause_density_dpll"] = merged["num_clauses_dpll"] / (merged["num_vars_dpll"] + 1e-6)
merged["vars_times_clauses_walksat"] = merged["num_vars_walksat"] * merged["num_clauses_walksat"]
merged["clause_density_walksat"] = merged["num_clauses_walksat"] / (merged["num_vars_walksat"] + 1e-6)
merged["is_sudoku"] = merged["instance"].str.contains("sudoku", case=False, na=False).astype(int)
merged["is_random3sat"] = merged["instance"].str.contains("random", case=False, na=False).astype(int)


def get_best_solver(row):
 
    runtime_dpll = row["runtime_seconds_dpll"]
    runtime_walksat = row["runtime_seconds_walksat"]
    

    if runtime_dpll < runtime_walksat - 1e-6:
        return 0 
  
    elif runtime_walksat < runtime_dpll - 1e-6:
        return 1
   
    else:
        return 0 

merged["best_solver_actual"] = merged.apply(get_best_solver, axis=1)


merged = merged.dropna(subset=["num_vars_dpll"]) 



feature_cols = [
    "num_vars_dpll", "num_clauses_dpll", "ratio_dpll",
    "num_vars_walksat", "num_clauses_walksat", "ratio_walksat",
    "is_sudoku", "is_random3sat", "vars_times_clauses_dpll",
    "clause_density_dpll", "vars_times_clauses_walksat",
    "clause_density_walksat", "var_diff", "clause_diff",
    "var_ratio", "clause_ratio"
]

X = merged[feature_cols]
y = merged["best_solver_actual"]

print("\n Original label distribution:")
print(y.value_counts().to_string())


ros = RandomOverSampler(random_state=42)
X_res, y_res = ros.fit_resample(X, y)

print("\n After balancing:")
print(y_res.value_counts().to_string())


X_train, X_test, y_train, y_test = train_test_split(
    X_res, y_res, test_size=0.2, random_state=42, stratify=y_res
)


model = RandomForestClassifier(n_estimators=150, random_state=42)
model.fit(X_train, y_train)


joblib.dump(model, "best_solver_predictor.pkl")
print("Trained model saved as 'best_solver_predictor.pkl'")



y_pred = model.predict(X_test)

print("\n" + "="*50)
print(" MODEL EVALUATION RESULTS")
print("="*50)
print(f"Model Type: Random Forest Classifier (n_estimators=150)")
print(f"Overall Accuracy: {accuracy_score(y_test, y_pred):.3f}\n")

print("\n--- A. Classification Report ---")
print(classification_report(y_test, y_pred, target_names=["DPLL (0)", "WalkSAT (1)"]))


cm = confusion_matrix(y_test, y_pred)
cm_df = pd.DataFrame(
    cm, 
    index=[f"Actual {DPLL_SOLVER_NAME}", f"Actual {WALKSAT_SOLVER_NAME}"], 
    columns=[f"Predicted {DPLL_SOLVER_NAME}", f"Predicted {WALKSAT_SOLVER_NAME}"]
)

print("\n--- B. Confusion Matrix (Detailed) ---")
print(cm_df)



print("\n" + "="*50)
print(" Feature Importances:")
print("="*50)
importances = pd.Series(model.feature_importances_, index=feature_cols).sort_values(ascending=False)
print(importances.to_string())


merged.to_csv("merged_results_enhanced.csv", index=False)
print("\n Final dataset saved as 'merged_results_enhanced.csv'")