# K-Means

## Executive Summary
This notebook demonstrates unsupervised clustering of temperature sensor data using the K‑means algorithm. It walks through data loading, preprocessing (handling nulls and duplicates), feature scaling, model training, cluster visualization, and evaluation using multiple clustering quality metrics (Silhouette Score, Davies‑Bouldin Index, Calinski‑Harabasz Index). The guide highlights how to interpret cluster centroids and assess clustering performance.

## Core Learning Objectives
- Understand the K‑means algorithm, its assumptions, and limitations.  
- Learn preprocessing steps for clustering: handling missing data, removing duplicates, and standardizing features.  
- Apply scikit‑learn’s `KMeans` to train a clustering model, extract cluster assignments and centroids, and visualize results.  
- Evaluate clustering quality using Silhouette Score, Davies‑Bouldin Index, and Calinski‑Harabasz Index, and use these metrics to choose an appropriate number of clusters.  
- Interpret the output metrics to diagnose over‑ or under‑clustering.

## 🔍 Section‑by‑Section Breakdown
### Goal
Build and evaluate a K‑means clustering model on temperature sensor data.

### Key Code Blocks Explained
- **Import & Setup** – Loads required libraries, adds the project’s `libs` directory to `PYTHONPATH`, and defines paths for data and models.  
- **Data Loading & Exploration** – Reads `temperature_sensor_data.csv`, displays the first rows, checks data types, and examines null/duplicate entries.  
- **Preprocessing** – Drops completely empty rows, removes duplicate records, and applies `StandardScaler` to scale numeric features for distance‑based clustering.  
- **Feature Matrix Creation** – Converts the cleaned DataFrame into a NumPy array (`X`) that serves as input to the clustering algorithm.  
- **Model Training** – Instantiates `KMeans(n_clusters=3, random_state=42, n_init="auto")`, fits it to `X`, and stores cluster assignments (`cls.labels_`) and centroid coordinates (`cls.cluster_centers_`).  
- **Visualization** – Plots the scaled data points colored by assigned cluster and overlays the centroids as red X markers; includes axis labels, title, grid, and legend.  
- **Evaluation** – Computes and prints:  
  - *Silhouette Score* (cluster cohesion vs. separation, range ‑1 → 1)  
  - *Inertia* (within‑cluster sum of squares)  
  - *Davies‑Bouldin Index* (inter‑cluster similarity, lower is better)  
  - *Calinski‑Harabasz Index* (between‑cluster dispersion vs. within‑cluster dispersion, higher is better).  
- **Results Interpretation** – Reviews printed scores to assess clustering quality and discusses implications (e.g., whether 3 clusters is appropriate).

## 📚 Mathematical/Logical Concept
K‑means seeks to partition data into *k* clusters by minimizing the within‑cluster sum of squared distances (the inertia). Each iteration alternates between **assignment** (assigning points to the nearest centroid) and **update** (recomputing centroids as the mean of assigned points). The algorithm converges when assignments no longer change; however, it may settle in a local optimum depending on initial centroid placement. Key parameters:  
- `n_clusters`: number of clusters to form.  
- `random_state`: seed for reproducible initialization.  
- `n_init`: number of different initial centroid seeds to try (higher values increase chance of better optimum).  

### Assumptions
- Clusters are convex and roughly spherical.  
- Features are numeric and measured on similar scales; hence the need for standardization (`StandardScaler`).  
- The appropriate number of clusters must be specified a priori or inferred via evaluation metrics.

## ✅ Verification
1. **Run the notebook end‑to‑end** – expect successful execution of all cells with printed scores and displayed plots.  
2. **Validate output shapes** – `cls.labels_` length must equal `X.shape[0]`; `cls.cluster_centers_` shape must be `(k, n_features)`.  
3. **Check metric ranges** – Silhouette Score should be within `[-1, 1]`; DBI should be non‑negative; CH Index should be non‑negative.  
4. **Confirm no runtime errors** – especially around path construction, file I/O, or missing modules.  
5. **Inspect visualizations** – ensure the scatter plot renders with distinct colors and that centroids appear as red ‘X’ markers.

## 📎 Resources & References
- scikit‑learn KMeans documentation: https://scikit‑learn.org/stable/modules/generated/sklearn.cluster.KMeans.html  
- Original notebook: `notebooks/K-Means.ipynb`  
- “Clustering: Theory & Practice” – Chapter 4, *Data Mining: Concepts & Algorithms*  
- Internal project README (for dataset description and sensor details)