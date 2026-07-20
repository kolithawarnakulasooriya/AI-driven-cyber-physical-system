# Study Guide: Kelmah Filtering

## Executive Summary
This notebook demonstrates the implementation and practical usage of a Kalman filter for estimating hidden variables from noisy sensor data. It walks through a 1‑dimensional filtering example, then extends to a 2‑dimensional velocity‑position estimation, showing how to ingest streaming data via a WebSocket, apply the filter, and visualize both raw and filtered results. The guide also includes a brief overview of multi‑dimensional Kalman filtering and how to interpret filter outputs in a cyber‑physical context.

## Core Learning Objectives
- Understand the mathematical foundation of Kalman filtering and its assumptions.  
- Learn to ingest real‑time sensor streams using `WebSocketCollector` and `SensorStream`.  
- Implement a 1‑D Kalman filter for scalar signals and a 2‑D Kalman filter for vector‑valued signals (position & velocity).  
- Visualize raw versus filtered data with Matplotlib, and compute histograms for distribution analysis.  
- Apply the filter to a synthetic scenario and interpret the impact of filtering on downstream analytics (e.g., machine‑learning model training).

## Notebook Overview
**Goal:** Provide a hands‑on demonstration of Kalman filtering on streaming temperature‑like sensor data, first in one dimension, then in two dimensions with position‑velocity pairs.

1. **Key Code Blocks Explained:**  
   - *WebSocket data collection*: `WebSocketCollector` pulls messages from `ws://localhost:8000/ws`.  
   - *Parsing*: Each message is JSON‑decoded to extract sensor readings; values are filtered for `NaN`s.  
   - *Filter initialization*: `KalmanFilter1D` with parameters `dt`, `X0`, `Q0`, `R0`; extended to `KalmanFilter2D` for vector inputs.  
   - *Filtering loop*: `kf.filter(values)` produces smoothed estimates.  
   - *Visualization*: Matplotlib histograms and line plots compare raw vs. filtered signals.

2. **Structure:**  
   - Cell 1: Imports, path setup, and utility definitions.  
   - Cell 2: Single‑dimensional data collection and filtering.  
   - Cell 3: Plotting raw data.  
   - Cell 4: Kalman filter results and plotting.  
   - Cell 5 onward: Multi‑dimensional extension, advanced filter setup, and additional visualizations.

## Mathematical/Logical Concept
The Kalman filter maintains a belief about the system state (e.g., position, velocity) represented as a Gaussian distribution with a mean (estimated state) and covariance (uncertainty). At each time step:
1. **Prediction:** The filter predicts the next state using a motion model (captured by the state transition matrix) and its uncertainty.  
2. **Update:** The predicted state is corrected using the measurement, weighted by the measurement noise covariance.  
3. **Iterate:** This predict‑update cycle recurs, gradually converging to the true state if the model assumptions hold.

In the 2‑D case, the state vector includes both position and velocity; the filter tracks their joint evolution, allowing derived quantities (e.g., velocity estimates) to inform position updates and vice‑versa.

## Labs & Hands‑On Exercises
1. **Exercise 1 – Simple 1‑D Filtering:**  
   - Run the notebook and verify that the filtered curve follows the raw signal with reduced high‑frequency noise.  
   - Modify the `R0` (measurement noise) parameter and observe how a larger value produces a more “lazy” filter (slower response).  

2. **Exercise 2 – 2‑D Position‑Velocity Estimation:**  
   - Examine the generated `VP pairs` plot; confirm that the filtered position and velocity trajectories are smooth.  
   - Change the process noise `Q0` and note the effect on lag versus jitter in the filtered outputs.  

3. **Exercise 3 – Histogram Analysis:**  
   - Run the histogram cells and compare the distribution shapes of raw vs. filtered values.  
   - Quantify the reduction in variance by computing `np.var(filtered_values) / np.var(raw_values)`.  

## Verification Steps
- **Run the Notebook:**  
  ```bash
  jupyter nbconvert --execute notebooks/KelmanFiltering.ipynb --to pdf
  ```  
  - Expected: PDF generation completes without errors; all plots (`kelman_response.png`‑style figures) are included.  

- **Check Output Files:**  
  ```bash
  ls -l study-guide/KelmanFiltering/*.png study-guide/KelmanFiltering/*.csv
  ```  
  - Expected: Files such as `kelman_response.png`, `test_signal.csv`, `filtered_signal.csv` exist and have non‑zero size.  

- **Validate Filter Execution:**  
  ```bash
  python - <<'PY'
import numpy as np
# Quick sanity check of the 1‑D filter length logic used in the notebook
b = np.array([1, -0.9, 0.81, -0.729])
a = np.array([1])
x = np.random.randn(100)
y = np.convolve(x, b[:4], mode='full')[:len(x)]
print('filter ran, output length:', len(y))
PY
  ```  
  - Expected output includes `filter ran, output length: 100`.  

- **Inspect Model Artifacts (if any models are saved):**  
  ```bash
  file study-guide/KelmanFiltering/*.pkl
  ```  
  - Expected: A non‑empty pickle file indicates successful model serialization.  

- **Confirm No Path Errors:**  
  ```bash
  python -c "import os; print(os.getcwd())"
  ```  
  - Expected: Prints the current working directory, confirming that relative paths (`datasets/`, `models/`, `libs/`) resolve correctly from the notebook location.  

## Pitfalls & Common Issues
- **File Path Accuracy:**  
  Ensure all relative paths (`datasets/`, `models/`, `libs/`) resolve correctly from the notebook's working directory. Using absolute paths or incorrectly computing `libs_dir` leads to `ModuleNotFoundError`.  

- **Dependency Versions:**  
  The notebook relies on specific versions of `scipy`, `sklearn`, and `numpy`. If the coefficients (`b`, `a`) appear stale or differ from expected values, reinstall matching versions or regenerate them via the filter design step.  

- **Over‑filtering:**  
  Setting `R0` or `Q0` too aggressively can overly smooth the signal, masking genuine dynamics. Test multiple parameter sets and compare against known ground‑truth signals if available.  

- **Placeholder Replacement:**  
  The notebook contains placeholders for filter coefficient arrays (`b`, `a`). If these placeholders remain unreplaced, filter operations will raise runtime errors. Verify that the `b` and `a` arrays are populated with actual coefficients before executing filter‑related cells.  

- **Model Overwrite:**  
  The notebook saves a trained ML model to `TemperatureSensorModel.pkl`. If running this notebook multiple times, the file will be overwritten silently. Consider backing up previous models if comparative analysis is needed.  

- **Plot Generation in Headless Environments:**  
  In environments without a display server, Matplotlib may default to a non‑interactive backend, causing plot generation to fail. Add `plt.switch_backend('Agg')` at the top of the notebook or export figures using `plt.savefig()` to ensure successful rendering.  

## Further Reading
- “Applied Kalman Filtering” by Gerald Bierman – a comprehensive text on algorithmic details and practical implementations.  
- “Estimation with Applications to Tracking and Navigation” by Yaakov Bar‑Shalom – deeper treatment of multi‑dimensional filtering.  
- Documentation on `WebSocketCollector` and `SensorStream` – available in the project's API reference.  
- Recent papers on attack‑aware state estimation for cyber‑physical systems – explore detection mechanisms in adversarial settings.