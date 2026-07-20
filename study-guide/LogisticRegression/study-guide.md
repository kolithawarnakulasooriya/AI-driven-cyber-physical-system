# Study Guide: Logistic Regression

## Executive Summary
This notebook provides a hands‑on introduction to logistic regression, a fundamental classification algorithm for binary and multi‑class problems. It covers the underlying theory, walks through data preparation, model training, evaluation, and hyper‑parameter tuning, and includes practical labs using scikit‑learn. The guide is tailored for beginners who are comfortable with Python and pandas but new to statistical learning methods.

## Core Learning Objectives
- Understand the difference between linear regression and logistic regression, and when to use each.  
- Grasp the sigmoid (logistic) function, decision boundary, and how probabilities are derived from linear combinations.  
- Implement binary and multi‑class logistic regression with scikit‑learn, covering regularization, class weighting, and different solvers.  
- Evaluate model performance using accuracy, confusion matrix, precision‑recall, ROC‑AUC, and calibration curves.  
- Perform hyper‑parameter tuning (regularization strength *C*, penalty type, solver) and interpret learning curves to avoid over‑/under‑fitting.  
- Apply logistic regression to a real‑world dataset (e.g., breast cancer or credit‑card fraud) and translate the results into actionable insights for a cyber‑physical system context.

## Notebook Overview
The notebook is organized into the following sections:

| Section | Description |
|---------|-------------|
| **1️⃣ Imports & Setup** | Loads `numpy`, `pandas`, `matplotlib`, `seaborn`, and `sklearn`; sets plot style. |
| **2️⃣ Data Loading & Exploration** | Reads a dataset (e.g., `breast_cancer.csv`), shows basic stats, class distribution, and pairwise relationships. |
| **3️⃣ Data Preprocessing** | Handles missing values, encodes categorical features if present, and scales numeric columns with `StandardScaler`. |
| **4️⃣ Train‑Test Split** | Splits data into training (70 %) and test (30 %) sets using stratified sampling. |
| **5️⃣ Baseline Logistic Regression Model** | Instantiates `LogisticRegression` (default settings), fits on training data, and predicts on test set. |
| **6️⃣ Model Evaluation** | Computes accuracy, confusion matrix, classification report, ROC curve, and calibration plot. |
| **7️⃣ Hyper‑parameter Tuning** | Experiments with regularization strengths `[0.01, 0.1, 1, 10]`, penalty types (`l2`, `l1`), and solvers (`lbfgs`, `saga`). Uses cross‑validation to select the best combination. |
| **8️⃣ Model Interpretation** | Extracts model coefficients, creates a coefficient plot, and explains feature impact. |
| **9️⃣ Calibration & Reliability** | Plots reliability diagram and discusses probability calibration. |
| **🔟 Summary & Next Steps** | Recap of key takeaways, ideas for extending the analysis (e.g., feature engineering, ensemble methods). |

## Mathematical Foundations
- **Sigmoid Function**: `σ(z) = 1 / (1 + e⁻ᶻ` transforms the linear combination of features `z = wᵀx + b` into a probability between 0 and 1.  
- **Decision Boundary**: For binary classification, the boundary is where `σ(z) = 0.5`, i.e., `z = 0`. In multi‑class settings, each class has its own boundary defined by the highest probability.  
- **Loss Function**: Logistic regression uses **binary cross‑entropy** (log‑loss): `- [y·log(p) + (1‑y)·log(1‑p)]`. For multi‑class, it extends to **multinomial log‑loss**.  
- **Regularization**: To prevent over‑fitting, an L2 (or L1) penalty adds `λ/2 · ||w||²` to the loss. The regularization strength is controlled by hyper‑parameter `C = 1/λ`. Smaller `C` → stronger regularization.  
- **Solver Choice**: Different solvers (`lbfgs`, `newton-cg`, `sag`, `saga`) are suited to different problem sizes and regularization types (e.g., `saga` supports L1).

## Implementation Details
- **Scaling**: Even though regularization mitigates some scale issues, standardizing features (zero mean, unit variance) improves convergence speed and numerical stability.  
- **Class Weighting**: Imbalanced datasets can be addressed by setting `class_weight='balanced'` or providing custom weights.  
- **scikit‑learn API**:  
  ```python
  from sklearn.linear_model import LogisticRegression
  from sklearn.metrics import roc_auc_score, roc_curve, confusion_matrix
  from sklearn.preprocessing import StandardScaler
  ```  
- **Hyper‑parameter Search**: Loop over `C` values, fit each model on training data, evaluate on validation set, and select the best based on ROC‑AUC or accuracy.  
- **Cross‑validation**: Use `StratifiedKFold` to preserve class ratios across folds.

## Hands‑On Labs & Exercises
1. **Lab 1 – Load & Visualize**  
   - Run data‑exploration cells.  
   - Produce a pair‑plot of the first three numeric features; note any separability between classes.  

2. **Lab 2 – Preprocess & Scale**  
   - Apply `StandardScaler` to all numeric columns.  
   - Verify that the scaled data has mean ≈ 0 and std ≈ 1 using `np.mean` and `np.std`.  

3. **Lab 3 – Train Baseline Model**  
   - Instantiate `LogisticRegression(max_iter=1000)`.  
   - Fit on training data and predict on test data.  
   - Compute accuracy and generate a confusion matrix heatmap.  

4. **Lab 4 – Tune Hyper‑parameters**  
   - Iterate over `C` in `[0.01, 0.1, 1, 10]`.  
   - Compare ROC‑AUC scores and select the best `C`.  
   - Plot ROC curves for at least three candidate models.  

5. **Lab 5 – Interpret Coefficients**  
   - Extract `model.coef_` and plot a horizontal bar chart of feature coefficients.  
   - Discuss which features increase/decrease the odds of the positive class.  

6. **Lab 6 – Calibration Check**  
   - Plot a reliability diagram to see if predicted probabilities align with observed frequencies.  
   - If mis‑calibrated, discuss next steps (e.g., Platt scaling).  

## Verification Steps
1. **Confirm Notebook Execution**  
   ```bash
   jupyter nbconvert --execute notebooks/LogisticRegression.ipynb --to pdf
   ```  
   Expected: PDF generation completes without errors; all cells run from start to finish.

2. **Inspect Output Artifacts**  
   ```bash
   ls -l study-guide/LogisticRegression/*.png study-guide/LogisticRegression/*.csv
   ```  
   Expected: Files such as `confusion_matrix.png`, `roc_curve.png`, `coefficients.png`, and `calibration.png` exist and are non‑empty.

3. **Run Provided Verification Script**  
   ```bash
   bash scripts/verify-notebook.sh notebooks/LogisticRegression.ipynb
   ```  
   Expected output includes “All verification steps passed”.

4. **Import Sanity Check**  
   ```bash
   python - <<'PY'
   import pandas as pd, numpy as np, sklearn
   from sklearn.linear_model import LogisticRegression
   print('LogisticRegression imports OK, sklearn version:', sklearn.__version__)
   PY
   ```  
   Expected: No import errors; prints `LogisticRegression imports OK, sklearn version: X.Y.Z`.

## Common Pitfalls
- **Missing Feature Scaling**: Unscaled features can cause slow convergence or cause the optimizer to stall, especially with L1 or L2 regularization. Always apply `StandardScaler`.  
- **Imbalanced Classes**: Accuracy can be misleading; when the positive class is rare, use precision, recall, and ROC‑AUC to gauge performance.  
- **Choosing the Wrong Solver**: Some solvers (`lbfgs`) do not support L1 regularization; using them with `penalty='l1'` raises an error. Choose `saga` for L1.  
- **Insufficient Max Iterations**: Default `max_iter=100` may be too low for convergence on larger datasets; increase it (`max_iter=1000`) or set `solver='saga'`.  
- **Over‑fitting with Weak Regularization**: A very small `C` (strong regularization) can under‑fit, while a large `C` (weak regularization) can over‑fit. Use validation performance to pick an appropriate `C`.  
- **Multiclass Ambiguity**: By default, scikit‑learn uses a one‑vs‑rest scheme for multi‑class; ensure the chosen solver supports the selected penalty.

## Further Reading
- **Books**:  
  - “The Elements of Statistical Learning” – Hastie, Tibshirani, and Friedman (Chapter 4 on linear methods).  
  - “Pattern Recognition and Machine Learning” – Christopher Bishop (Section 4.1 on logistic regression).  
- **Articles**:  
  - “Understanding Logistic Regression Analysis” – Towards Data Science (online).  
  - “Regularization in Logistic Regression” – Machine Learning Mastery (tutorial).  
- **Documentation**:  
  - scikit‑learn Logistic Regression guide: <https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression>  
  - Cross‑validation with scikit‑learn: <https://scikit-learn.org/stable/modules/cross_validation.html>  

---

*Generated by the **study‑guide‑preparer** skill for the notebook `notebooks/LogisticRegression.ipynb`.*