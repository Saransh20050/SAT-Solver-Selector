import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import export_graphviz, plot_tree
import joblib

# --- Load dataset ---
merged = pd.read_csv("merged_results_enhanced.csv")

# --- Load trained model ---
model = joblib.load("best_solver_predictor.pkl")

# --- 1️⃣ SAT vs clauses/literals (WalkSAT) ---
plt.figure(figsize=(10,6))
sns.scatterplot(
    data=merged,
    x="num_clauses_walksat",
    y="num_vars_walksat",
    hue=merged["result_walksat"],
    palette={"SAT":"green", "UNSAT":"red"},
    alpha=0.6
)
plt.title("WalkSAT: Satisfiability vs Clauses / Variables")
plt.xlabel("Number of Clauses")
plt.ylabel("Number of Variables")
plt.legend(title="Result")
plt.grid(True)
plt.tight_layout()
plt.show()

# --- 2️⃣ Runtime vs clauses/literals (WalkSAT) ---
plt.figure(figsize=(10,6))
sns.scatterplot(
    data=merged,
    x="num_clauses_walksat",
    y="runtime_seconds_walksat",
    hue=merged["result_walksat"],
    palette={"SAT":"green", "UNSAT":"red"},
    alpha=0.6
)
plt.title("WalkSAT: Runtime vs Clauses")
plt.xlabel("Number of Clauses")
plt.ylabel("Runtime (seconds)")
plt.yscale("log")  # log scale if some runtimes are much larger
plt.grid(True)
plt.tight_layout()
plt.show()

# --- 3️⃣ Feature Importances from Random Forest ---
feature_cols = [
    "num_vars_dpll", "num_clauses_dpll", "ratio_dpll",
    "num_vars_walksat", "num_clauses_walksat", "ratio_walksat",
    "is_sudoku", "is_random3sat", "vars_times_clauses_dpll",
    "clause_density_dpll", "vars_times_clauses_walksat",
    "clause_density_walksat", "var_diff", "clause_diff",
    "var_ratio", "clause_ratio"
]

importances = pd.Series(model.feature_importances_, index=feature_cols).sort_values(ascending=True)
plt.figure(figsize=(10,8))
importances.plot(kind="barh", color="skyblue")
plt.title("Random Forest Feature Importances")
plt.xlabel("Importance")
plt.ylabel("Feature")
plt.tight_layout()
plt.show()

# --- 4️⃣ Visual Decision Tree --- 
# Fit a small Decision Tree on same data to visualize a single tree
from sklearn.tree import DecisionTreeClassifier
X = merged[feature_cols]
y = merged["best_solver_actual"]

# Limit depth to make tree readable
dtree = DecisionTreeClassifier(max_depth=3, random_state=42)
dtree.fit(X, y)

plt.figure(figsize=(20,10))
plot_tree(
    dtree,
    feature_names=feature_cols,
    class_names=["DPLL", "WalkSAT"],
    filled=True,
    rounded=True,
    fontsize=12
)
plt.title("Decision Tree Visualization (max_depth=3)")
plt.show()
