# Study Guide: K-Nearest Neighbors (KNN)

## Executive Summary
This notebook provides a hands‑on introduction to the k‑nearest neighbors (k‑NN) algorithm, a simple yet powerful instance‑based machine learning technique. It walks through the theory behind k‑NN, demonstrates how to prepare data, train a model, evaluate its performance, and tune hyper‑parameters. The guide is tailored for beginners who are new to classification algorithms but are familiar with basic Python and pandas data structures.

## Core Learning Objectives
- Understand the intuition behind instance‑based learning and how k‑NN uses proximity to make predictions.  
- Learn the key steps in preparing data for k‑NN (scaling, train‑test splitting, handling categorical variables).  
- Implement a k‑NN classifier using `scikit‑learn`, generate predictions, and evaluate accuracy, precision, recall, and confusion matrices.  
- Practice hyper‑parameter tuning (choosing *k*, distance metric, weighting) and understand the trade‑off between bias and variance.  
- Apply k‑NN to a real‑world dataset (e.g., iris or a synthetic toy dataset) and interpret the results in a cyber‑physical context.

## Notebook Overview
The notebook is organized into the following sections:

| Section | Description |
|---------|-------------|
| **1️⃣ Imports & Setup** | Loads required libraries (`numpy`, `pandas`, `matplotlib`, `sklearn`). Sets up plotting style. |
| **2️⃣ Data Loading & Exploration** | Reads a dataset (e.g., `iris.csv`), shows basic statistics, and visualizes pairwise relationships. |
| **3️⃣ Data Preprocessing** | Handles missing values, encodes categorical features, and scales numeric columns using `StandardScaler`. |
| **4️⃣ Train‑Test Split** | Splits data into training (70 %) and test (30 %) sets with stratified sampling. |
| **5️⃣ Baseline k‑NN Model** | Instantiates a `KNeighborsClassifier`, fits it on the training set, and produces predictions on the test set. |
| **6️⃣ Model Evaluation** | Computes accuracy, confusion matrix, classification report, and ROC curve. |
| **7️⃣ Hyper‑parameter Tuning** | Experiments with different values of *k* (1‑15) and evaluates performance; selects the best *k* using cross‑validation. |
| **8️⃣ Feature Engineering (Optional)** | Demonstrates how to experiment with distance metrics (Euclidean vs. Manhattan) and weighted voting. |
| **9️⃣ Summary & Next Steps** | Recap of key take‑aways, ideas for extending the analysis (e.g., adding more features, trying other classifiers). |

## Mathematical Foundations
- **Distance Metrics**: k‑NN relies on a distance function to measure similarity. The default is **Euclidean distance** `d(p,q)=√∑(p_i‑q_i)²`. For categorical or mixed data, alternatives like **Manhattan** (`∑|p_i‑q_i|`) or **Cosine similarity** may be more appropriate.  
- **Choice of *k***: A small *k* (e.g., 1) yields low bias and high variance; a large *k* does the opposite. The optimal *k* is often an odd number to avoid ties.  
- **Decision Rule**: The class assigned to a query point is the mode of the *k* nearest neighbors. Some implementations weight contributions inversely by distance to reduce the influence of distant points.

## Implementation Details
- **Scaling**: k‑NN is sensitive to feature scale, so `StandardScaler` (zero mean, unit variance) is applied to numeric columns.  
- **Train‑Test Split**: Uses `train_test_split` with `stratify=y` to preserve class distribution.  
- **scikit‑learn API**:  
  ```python
  from sklearn.neighbors import KNeighborsClassifier
  from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
  from sklearn.preprocessing import StandardScaler
  ```
- **Hyper‑parameter Search**: Loop over `k` values, fit each model, record validation score, and pick the best.

## Hands‑On Labs & Exercises
1. **Lab 1 – Load & Visualize**  
   - Run the data‑exploration cells.  
   - Produce a pair‑plot of the first three features; note any class separability.  

2. **Lab 2 – Preprocess & Scale**  
   - Apply `StandardScaler` to all numeric columns.  
   - Verify that the scaled data has mean ≈ 0 and std ≈ 1.  

3. **Lab 3 – Train a Baseline Model**  
   - Use `KNeighborsClassifier(n_neighbors=5)`.  
   - Generate predictions on the test set and compute accuracy.  

4. **Lab 4 – Tune *k***  
   - Iterate `k` from 1 to 15, store accuracy, and plot a “k vs. accuracy” curve.  
   - Identify the *k* with the highest cross‑validated score.  

5. **Lab 5 – Confusion & Error Analysis**  
   - Plot the confusion matrix heatmap.  
   - Identify the most confused classes and hypothesize why.  

## Verification Steps
1. **Check Notebook Execution**  
   ```bash
   jupyter nbconvert --execute notebooks/KNN.ipynb --to pdf
   ```  
   Expected: PDF generation completes without errors; all cells run from start to finish.

2. **Validate Output Files**  
   ```bash
   ls -l study-guide/KNN/*.png study-guide/KNN/*.csv
   ```  
   Expected: Files such as `confusion_matrix.png`, `k_vs_accuracy.png`, and `metrics.json` exist and are non‑empty.

3. **Run Verification Script** (provided in the repo)  
   ```bash
   bash scripts/verify-notebook.sh notebooks/KNN.ipynb
   ```  
   Expected output includes “All verification steps passed”.

4. **Quick Code Check**  
   ```bash
   python - <<'PY'
   import pandas as pd, numpy as np, sklearn
   from sklearn.neighbors import KNeighborsClassifier
   from sklearn.model_selection import train_test_split
   from sklearn.metrics import accuracy_score
   # Minimal sanity‑check that imports succeed
   print('kNN imports OK, sklearn version:', sklearn.__version__)
   PY
   ```  
   Expected: No import errors; prints `kNN imports OK, sklearn version: X.Y.Z`.

## Common Pitfalls
- **Feature Scaling**: Skipping scaling leads to features with larger numeric ranges dominating distance calculations. Always apply `StandardScaler` to numeric columns.  
- **High‑Dimensional Data**: In very high dimensions, Euclidean distance may become less discriminative (“curse of dimensionality”). Consider dimensionality reduction (PCA) before k‑NN.  
- **Imbalanced Classes**: Accuracy can be misleading; use precision, recall, and F1‑score, especially when minority classes are critical.  
- **Choosing *k***: Using an even *k* may cause tie‑breaking ambiguity; prefer odd numbers or rely on weighted voting.  
- **Data Leakage**: Ensure that any preprocessing (e.g., scaling) is fitted only on the training set and then applied to the test set.

## Further Reading
- **Books**:  
  - “Pattern Recognition and Machine Learning” – Christopher Bishop (Chapter 12 on nearest neighbors).  
  - “Hands‑On Machine Learning with Scikit‑Learn, Keras & TensorFlow” – Aurélien Géron (Section on classification).  
- **Articles**:  
  - “A Simple Introduction to k‑Nearest Neighbors” – Towards Data Science (online).  
  - “When to Use k‑NN” – Machine Learning Mastery (tutorial).  
- **Documentation**:  
  - scikit‑learn user guide: <https://scikit-learn.org/stable/modules/neighbors.html>  
  - Cross‑validation with scikit‑learn: <https://scikit-learn.org/stable/modules/cross_validation.html>

---

*Generated by the **study‑guide‑preparer** skill for the notebook `notebooks/KNN.ipynb`.*