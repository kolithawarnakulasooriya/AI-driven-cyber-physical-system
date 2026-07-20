# Study Guide: Polynomial Regression

## Executive Summary
This notebook introduces **polynomial regression**, a technique that extends linear regression by modeling relationships as a polynomial function of the input variables. It walks through the mathematical rationale, demonstrates how to generate polynomial features, train models, evaluate performance, and tune hyper‑parameters. The guide is aimed at beginners who are comfortable with Python and pandas but new to feature engineering and non‑linear modeling.

## Core Learning Objectives
- Understand the difference between linear and polynomial regression, and when a polynomial model is appropriate.  
- Learn how to generate polynomial features using `PolynomialFeatures` and why scaling is essential.  
- Implement polynomial regression with `scikit‑learn`, including regularization (Ridge/Lasso) to control over‑fitting.  
- Evaluate model fit using metrics such as RMSE, MAE, R², and visual diagnostics (residual plots).  
- Perform hyper‑parameter tuning for polynomial degree and regularization strength via cross‑validation.  
- Apply polynomial regression to a real‑world dataset (e.g., housing prices or energy consumption) and interpret feature interactions in a cyber‑physical context.

## Notebook Overview
| Section | Description |
|---------|-------------|
| **1️⃣ Imports & Setup** | Loads `numpy`, `pandas`, `matplotlib`, `seaborn`, and `sklearn`; sets plot style. |
| **2️⃣ Data Loading & Exploration** | Reads a dataset (e.g., `energy_dataset.csv`), shows basic statistics, histograms, and pairwise relationships. |
| **3️⃣ Data Preprocessing** | Handles missing values, encodes categorical variables if present, and scales numeric columns with `StandardScaler`. |
| **4️⃣ Polynomial Feature Engineering** | Uses `PolynomialFeatures` to create expanded feature sets (e.g., degree 2, degree 3). |
| **5️⃣ Baseline Linear Model** | Fits a simple linear regression for comparison. |
| **6️⃣ Polynomial Regression Models** | Trains models of varying degree (1‑5) with/without regularization, records performance. |
| **7️⃣ Model Evaluation & Diagnostics** | Computes RMSE/MAE/R² on train‑test splits, plots predicted vs. actual, residual plots, and learning curves. |
| **8️⃣ Hyper‑parameter Tuning** | Systematic search over `degree` and regularization parameter `alpha` using `GridSearchCV`. |
| **9️⃣ Feature Interaction Visualization** | Generates interaction plots to highlight which original features contribute most to the polynomial model. |
| **🔟 Summary & Next Steps** | Recap of key takeaways, ideas for extending the analysis (e.g., polynomial degree selection, interaction penalties). |

## Mathematical Foundations
- **Polynomial Expansion**: For a feature vector **x** = `[x₁, x₂, …, xₙ]`, a degree‑d polynomial creates all possible combinations of terms up to degree d, including interactions (e.g., `x₁²`, `x₁·x₂`).  
- **Bias‑Variance Trade‑off**: Higher‑degree polynomials can fit training data more closely (low bias) but may capture noise, leading to high variance and over‑fitting. Regularization adds a penalty to control complexity.  
- **Regularization**: Ridge (L2) adds `α·||w||²` to the loss; Lasso (L1) can shrink some coefficients to zero, performing feature selection.  
- **Scaling Importance**: Polynomial features multiply original values, so unscaled data can cause numerical overflow or make some terms dominate. `StandardScaler` (zero mean, unit variance) is applied before expansion.

## Implementation Details
- **Key API Calls**:  
  ```python
  from sklearn.preprocessing import PolynomialFeatures, StandardScaler
  from sklearn.linear_model import Ridge, Lasso, LinearRegression
  from sklearn.pipeline import Pipeline
  from sklearn.model_selection import train_test_split, GridSearchCV
  from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
  ```  
- **Pipeline Construction**:  
  ```python
  pipeline = Pipeline([
      ('scaler', StandardScaler()),
      ('poly', PolynomialFeatures(degree=2, include_bias=False)),
      ('regressor', Ridge(alpha=1.0))
  ])
  ```  
- **Model Evaluation Metrics**:  
  - **RMSE** = √(mean((y_true‑y_pred)²))  
  - **MAE** = mean(|y_true‑y_pred|)  
  - **R²** = 1 − (SS_res / SS_tot)  
- **Cross‑Validation**: Uses `StratifiedKFold` for regression (i.e., plain `KFold`) to preserve data distribution across folds.

## Hands‑On Labs & Exercises
1. **Lab 1 – Load & Visualize**  
   - Run data‑exploration cells.  
   - Produce histograms of each feature; note any skewness.  

2. **Lab 2 – Preprocess & Scale**  
   - Apply `StandardScaler` to all numeric columns.  
   - Verify that each column’s mean ≈ 0 and std ≈ 1 (use `np.mean`/`np.std`).  

3. **Lab 3 – Generate Polynomial Features**  
   - Create degree‑2 features (`PolynomialFeatures(degree=2)`).  
   - Inspect the transformed matrix shape; note the increase in dimensionality.  

4. **Lab 4 – Train Baseline Linear Model**  
   - Fit a simple `LinearRegression` on the original features.  
   - Record train and test RMSE/MAE/R².  

5. **Lab 5 – Fit Polynomial Models**  
   - Loop over `degree` in `[2,3,4]` and `alpha` in `[0.1, 1, 10]`.  
   - Store validation scores for each combination.  

6. **Lab 6 – Model Evaluation**  
   - Plot predicted vs. actual values for the best model.  
   - Generate a residual histogram and a residual‑vs‑predicted scatter plot.  

7. **Lab 7 – Hyper‑parameter Tuning**  
   - Use `GridSearchCV` with `cv=5` to select the optimal `degree` and `alpha`.  
   - Print the best parameters and corresponding CV score.  

8. **Lab 8 – Feature Interaction Visualization**  
   - Extract coefficients from the final model.  
   - Plot a bar chart of coefficient magnitudes, grouped by original feature.  

## Verification Steps
1. **Execute Notebook Conversion**  
   ```bash
   jupyter nbconvert --execute notebooks/PolinomialRegression.ipynb --to pdf
   ```  
   Expected: PDF generation completes without errors; all cells run sequentially.

2. **Check Output Artifacts**  
   ```bash
   ls -l study-guide/PolinomialRegression/*.png study-guide/PolinomialRegression/*.csv
   ```  
   Expected: Files such as `model_report.png`, `residual_plot.png`, `coefficients.png`, and `gridsearch_results.csv` exist and are non‑empty.

3. **Run Provided Verification Script**  
   ```bash
   bash scripts/verify-notebook.sh notebooks/PolinomialRegression.ipynb
   ```  
   Expected output includes “All verification steps passed”.

4. **Import Sanity Check**  
   ```bash
   python - <<'PY'
   import pandas as pd, numpy as np, sklearn
   from sklearn.preprocessing import PolynomialFeatures
   print('PolynomialFeatures imports OK, sklearn version:', sklearn.__version__)
   PY
   ```  
   Expected: No import errors; prints `PolynomialFeatures imports OK, sklearn version: X.Y.Z`.

## Common Pitfalls
- **Skipping Scaling**: Unscaled data leads to poorly conditioned polynomial expansions, causing numerical instability or dominant features. Always scale before `PolynomialFeatures`.  
- **Choosing Too High a Degree**: Degrees > 4 often produce over‑fitted models that perform poorly on unseen data. Use validation performance to select an appropriate degree.  
- **Ignoring Multicollinearity**: High‑degree polynomials can create highly correlated features, destabilizing coefficient estimates. Regularization (Ridge/Lasso) mitigates this.  
- **Misinterpreting Coefficients**: Coefficients in expanded polynomial space are not directly comparable to original feature coefficients; always transform back or use interaction plots for interpretation.  
- **Memory Exhaustion**: Degree‑d expansions grow combinatorially; on large datasets, degree 3+ may require excessive RAM. Consider iterative or incremental approaches for very wide data.  
- **Regularization Mismatch**: Using L1 (`alpha`) with solvers that don’t support it (e.g., `solver='lbfgs'`) raises an error; choose `solver='saga'` for L1/L2 flexibility.

## Further Reading
- **Books**:  
  - “The Elements of Statistical Learning” – Hastie, Tibshirani, & Friedman (Chapter 3 on polynomial regression).  
  - “Pattern Recognition and Machine Learning” – Christopher Bishop (Section 4.2 on ridge regression).  
- **Articles**:  
  - “Polynomial Regression: When and How to Use It” – Towards Data Science (online).  
  - “Feature Engineering for Machine Learning” – Machine Learning Mastery (tutorial on polynomial features).  
- **Documentation**:  
  - scikit‑learn polynomial features guide: <https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.PolynomialFeatures.html>  
  - Model evaluation metrics: <https://scikit-learn.org/stable/modules/model_evaluation.html>  

---

*Generated by the **study‑guide‑preparer** skill for the notebook `notebooks/PolinomialRegression.ipynb`.*