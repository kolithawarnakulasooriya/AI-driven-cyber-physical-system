# Decision Trees

## Executive Summary
This notebook explores decision tree classification for network security event prediction. It loads firewall label data, performs feature selection, trains a decision tree classifier, evaluates its performance, and provides detailed class‑by‑class analysis of the model’s behavior.

## Core Learning Objectives
- Understand how decision trees partition data using impurity metrics (Gini impurity, information gain).  
- Learn to train, visualize, and evaluate a `DecisionTreeClassifier` with scikit‑learn.  
- Interpret model predictions at the class level and diagnose strengths/weaknesses (e.g., high recall for “allow”, low sensitivity for “reset‑both”).  
- Apply best‑practice techniques such as depth limiting, pruning, and accuracy reporting.

## 🔍 Section‑by‑Section Breakdown
### Goal
**Build and interpret a decision tree model to classify network traffic as “allow”, “drop”, “deny”, or “reset‑both”.**

### Key Code Blocks Explained
- **Import & Setup**  
  - *Concept*: Import libraries (`pandas`, `numpy`, `matplotlib`, `seaborn`, `sklearn`).  
  - *Why*: Sets up the environment for data handling, visualization, and modeling.  
- **Data Loading & Exploration**  
  - *Concept*: Read `firewall_data.csv` into a DataFrame; display head, describe, info, null counts.  
  - *Why*: Ensures data integrity, uncovers missing values, and familiarizes with feature set.  
- **Correlation Analysis**  
  - *Concept*: Compute Cramér's V heatmap for numerical‑nonnumerical correlations.  
  - *Why*: Identifies which features are most predictive of the target.  
- **Feature Selection**  
  - *Concept*: Drop non‑informative columns (`Source Port`, `Destination Port`, …).  
  - *Why*: Reduces noise and focuses training on predictive features.  
- **Train‑Test Split**  
  - *Concept*: `train_test_split` with 20 % test size and random_state = 42.  
  - *Why*: Provides unbiased evaluation data.  
- **Model Training**  
  - *Concept*: Instantiate `DecisionTreeClassifier(max_depth=3, random_state=42)` and fit on training data.  
  - *Why*: Limits depth to improve interpretability and prevent overfitting.  
- **Visualization**  
  - *Concept*: Use `plot_tree` with feature names, class names, filled nodes, and proper formatting.  
  - *Why*: Produces a human‑readable tree diagram for model interpretation.  
- **Evaluation**  
  - *Concept*: Print `classification_report`, display confusion matrix, compute training/testing accuracy, and report tree depth/leaf count.  
  - *Why*: Quantifies predictive performance and inspects model complexity.  
- **Class‑by‑Class Breakdown**  
  - *Concept*: Detailed analysis of precision, recall, and F1‑score for each class (allow, drop, deny, reset‑both).  
  - *Why*: Highlights where the model excels (e.g., perfect recall for “allow”) and where it struggles (e.g., low F1 for “reset‑both” due to data scarcity).

### Structure
1. **Data Loading & Exploration** – cells 2‑4, 5‑6.  
2. **Correlation & Feature Selection** – cells 7‑9.  
3. **Train‑Test Split** – cell 10.  
3. **Model Training & Visualization** – cells 11‑13.  
4. **Evaluation & Reporting** – cells 14‑110.

## 📚 Mathematical/Logical Concept
Decision trees recursively split the feature space to create homogeneous subsets with respect to the target label. Each internal node tests a feature; branches represent observed outcomes; leaf nodes store class predictions.  
- **Gini impurity** measures class heterogeneity: \(G = \sum_{k}p_k(1-p_k)\).  
- **Information gain** prefers splits that reduce entropy the most.  
- The algorithm continues splitting until a stopping criterion (e.g., max depth, minimum samples per leaf) is met.  
- **Pruning** removes branches that contribute little to classification power, improving generalization.

## ✅ Verification
- Execute the notebook end‑to‑end; the training and test accuracy should print (e.g., `Training Accuracy: 0.96`, `Testing Accuracy: 0.92`).  
- Confirm that a confusion matrix heatmap appears and that the classification report lists per‑class metrics.  
- Verify that the tree plot renders and that the printed depth and leaf counts match the `max_depth=3` constraint.

## 📎 Resources & References
- scikit‑learn Documentation: https://scikit‑learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html  
- Internal project README: `README.md` (for dataset description).  
- For deeper insight into pruning strategies, see https://doi.org/10.1016/j.eswa.2018.09.018