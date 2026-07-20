# False Data Injection Attacks on Sensors

## Executive Summary
This notebook explores how adversaries can maliciously alter sensor readings—known as False Data Injection (FDI) attacks—and demonstrates techniques to detect and mitigate such attacks using a Kalman filter and a machine‑learning classifier. It walks through a realistic scenario where temperature sensor data is spoofed, showing both the attack and the defensive analyses in a controlled environment.

## Core Learning Objectives
- Understand the threat model behind FDI attacks on cyber‑physical systems.  
- Identify common FDI attack techniques (replay, spoofing, scaled manipulation, coordinated injection, timestamp tampering).  
- Learn to apply statistical and model‑based detection methods (residual analysis, anomaly detection, cryptographic integrity).  
- Implement and evaluate a Kalman‑filter-based filter and a supervised ML classifier to flag malicious sensor data.  
- Gain practical insights into mitigation strategies such as redundancy, secure communication, and robust estimation.

## Notebook Overview
The notebook simulates a sensor stream via WebSocket, injects false temperature readings, processes the data with a Kalman filter, and trains a machine‑learning model to distinguish normal from injected readings. Visualizations illustrate filtered vs. raw signals, distribution comparisons, outlier detection, and classification performance. Code cells cover data acquisition, preprocessing, filtering, model training, and evaluation.

## Threat Model
- **Attacker Goals**: Disrupt control loops, bias analytics, trigger unsafe actions, conceal events, or cause physical damage.  
- **Attacker Capabilities**: Network access, man‑in‑the‑middle position, compromised sensor nodes, ability to replay or synthesize messages.  
- **Constraints**: Varying knowledge of system dynamics, timing fidelity, authentication mechanisms, and sensor fusion algorithms.

## Attack Techniques Covered
- **Replay Attacks**: Re‑broadcast previously captured legitimate sensor values to mask malicious modifications.  
- **Saturation / Spoofing**: Inject extreme outlier values to force alarms or saturate filters.  
- **Scaled / Biased Manipulation**: Apply constant offsets or scaling factors to bias sensor readings.  
- **Coordinated Multi‑Sensor Injection**: Modify several correlated sensors simultaneously to evade simple plausibility checks.  
- **Time‑Shift / Timestamp Tampering**: Alter message ordering or timestamps to break temporal correlation checks.

## Typical Impact
- Incorrect state estimation leading to unsafe actuator commands.  
- False alarms or suppression of legitimate alarms.  
- Long‑term model drift and degraded machine‑learning performance.  
- Potential physical damage, safety hazards, operational downtime, or loss of trust.

## Detection Strategies Demonstrated
- **Redundancy & Cross‑Checks**: Use multiple independent sensor measurements for plausibility verification.  
- **Consistency Checks**: Apply physics‑based invariants and model residuals (e.g., Kalman filter residuals).  
- **Statistical / Anomaly Detection**: Monitor residuals for abnormal behavior using thresholding or clustering techniques.  
- **Time‑Series Correlation**: Detect replay or timing anomalies via entropy, autocorrelation, and sequence uniqueness analyses.  
- **Cryptographic Integrity**: Validate messages with MACs or digital signatures to prevent spoofing.

## Mitigation & Hardening Techniques
- **Authentication & Encryption**: Secure sensor‑to‑controller communications with TLS/DTLS and mutual authentication.  
- **Secure Boot & Device Attestation**: Ensure firmware authenticity and integrity before accepting sensor data.  
- **Rate Limiting & Freshness Checks**: Reject stale or duplicated messages; employ nonces or sequence numbers.  
- **Diversity & Sensor Fusion**: Combine heterogeneous sensors and integrate physics‑based models into fusion algorithms.  
- **Robust Estimators**: Use outlier‑resistant filtering (e.g., Huber‑loss Kalman filters) and attack‑aware state estimation.  
- **Monitoring & Logging**: Maintain end‑to‑end telemetry for forensic analysis and post‑incident review.

## Practical Recommendations
1. **Threat‑Model Your Deployment**: Identify high‑impact sensors and plausible attack vectors.  
2. **Apply Defense‑in‑Depth**: Combine cryptography, redundancy, statistical detection, and operational policies.  
3. **Test Adversarial Scenarios**: Simulate replay, spoofing, and coordinated injections during development and drills.  
4. **Manage Firmware & Keys**: Rotate keys, apply patches, and use secure provisioning pipelines.  
5. **Document & Train**: Keep security documentation up‑to‑date and train operators on detection procedures.

## Example Scenario (Concise)
A temperature sensor in an industrial process is spoofed by adding a constant offset. The control loop reduces cooling because readings appear higher, leading to overheating. Detection occurs via residuals from a Kalman‑filter estimator, which trigger a fail‑safe when thresholds are exceeded. Mitigation switches to a redundant sensor and activates a safe‑shutdown protocol.

## Further Reading
- Research on attack‑aware state estimation and resilient control.  
- Industry guidance on ICS/SCADA security and IoT device hardening.  
- Papers on robust Kalman filtering and sparse attack detection techniques.

## Labs & Hands‑On Exercises
1. **Exercise 1 – Simulate a Replay Attack**:  
   - Replay captured sensor values and observe residual behavior.  
   - Verify that the detection script raises an alert when replay exceeds a threshold.  

2. **Exercise 2 – Implement a Consistency Check**:  
   - Create a simple physics‑based invariant (e.g., temperature cannot exceed a known bound) and integrate it into the data pipeline.  
   - Confirm that the check flags injected outliers.  

3. **Exercise 3 – Train a Binary Classifier**:  
   - Use the provided `MLPRegressor` pipeline to differentiate normal vs. injected sensor readings.  
   - Evaluate precision/recall on a held‑out test set and discuss trade‑offs.  

## Verification Steps
- **Run the Notebook**: Execute `jupyter nbconvert --execute FalseDataInjection.ipynb --to pdf` or run the notebook interactively.  
  - Expected: Plots of raw, filtered, and attacked signals appear without errors; `kelman_response.png` and related figures are generated.  

- **Check Output Files**:  
  ```bash
  ls -l study-guide/FalseDataInjection/*.png study-guide/FalseDataInjection/*.csv
  ```  
  - Expected: Files such as `kelman_response.png`, `test_signal.csv`, `filtered_signal.csv`, and model checkpoint `TemperatureSensorModel.pkl` exist and have non‑zero size.  

- **Validate Detection Logic**:  
  ```bash
  python -c "import numpy as np; \
  from scipy import signal; \
  b = np.array([1, -0.9, 0.81, -0.729]); \
  a = np.array([1]); \
  x = np.random.randn(100); \
  y = signal.lfilter(b, a, x); \
  print('filter ran, output length:', len(y))"
  ```  
  - Expected output includes `filter ran, output length: 100`.  

- **Inspect Model Artifacts**:  
  ```bash
  file study-guide/FalseDataInjection/TemperatureSensorModel.pkl
  ```  
  - Expected: A non‑empty pickle file indicating successful model serialization.

## Pitfalls & Common Issues
- **File Path Accuracy**: Ensure all relative paths (`datasets/`, `models/`, `libs/`) resolve correctly from the notebook's working directory.  
- **Dependency Versions**: Inconsistent library versions (e.g., older `scipy` or `sklearn`) may produce different filter coefficients; re‑install required packages if results diverge.  
- **Over‑filtering**: Aggressive filter cutoffs can distort genuine sensor dynamics; validate trade‑offs between noise suppression and signal fidelity.  
- **Placeholder Replacement**: Replace placeholder coefficient arrays (`b`, `a`) with values generated by your actual filter design; stale placeholders cause runtime errors.  
- **Model Overwrite**: Re‑training the ML model overwrites `TemperatureSensorModel.pkl`; back up previous models if comparative analysis is needed.  
- **Plot Generation**: If plots fail to render in headless environments, add `plt.switch_backend('Agg')` at the top of the notebook or export figures using `plt.savefig()`.

---

*Generated by the study‑guide‑preparer skill for the topic “False Data Injection Attacks on Sensors (Notebook: FalseDataInjection.ipynb)”.*