# NSIN — SUAS Detection from DOD Sensor Data

A machine learning pipeline for detecting Small Unmanned Aerial Systems (SUAS/drones) from Department of Defense sensor telemetry data. The system parses raw C2 device files, engineers flight-characteristic features including a novel trajectory smoothness metric based on B-spline interpolation, and trains classification models to distinguish drones from other airborne objects.

## Overview

The core hypothesis is that drone flight paths exhibit a characteristic **smoothness signature** in their trajectory (distance over time), distinguishable from non-drone objects like birds. This smoothness is quantified using B-spline interpolation and custom metrics applied to the distance-vs-time curve of each tracked threat.

## Models

| Model | Library |
|-------|---------|
| Decision Tree | scikit-learn |
| XGBoost Random Forest | xgboost |
| Random Forest | scikit-learn |

## Per-Threat Aggregated Results

Choose Model: Random Forest

| Metric | Score |
|--------|-------|
| Precision | 0.769 |
| Recall | 0.952 |
| F1 Score | 0.851 |
| Accuracy | 0.965 |


## Project Structure

```
NSIN/
├── UIImplementation/       # Main pipeline — notebook + all Python modules
│   ├── UIImplementation.ipynb  # End-to-end workflow notebook
│   ├── ParseData.py            # Data ingestion from raw DOD files
│   ├── FeatureEngineering.py   # Feature engineering + smoothness metric
│   ├── TrainingMLAlgorithm.py  # Model training (DT, XGBoost, Random Forest)
│   ├── PredictSUAS.py          # Single-threat prediction
│   ├── Prediction_Accuracy.py  # Evaluation, confusion matrix, precision/recall
│   ├── distance.py             # Haversine distance calculation
│   ├── metric1.py              # Smoothness metric m1
│   └── metric2.py              # Smoothness metric m2
├── Parsing/                # Standalone parsing utilities
│   ├── parseHeaders.py         # Extracts JSON keys into dot-notation headers
│   ├── getalldata.py           # Batch-parses all DOD files to CSV
│   ├── parseDeviceCoords.py    # Extracts device emplacement coordinates
│   ├── parseThreatCoords.py    # Extracts threat locations and detection times
│   └── pandasEpochToDT.py      # Epoch microseconds → datetime conversion
├── Metrics/                # Reusable smoothness metric package
│   ├── metric1.py              # Variance of successive differences (jitter)
│   ├── metric2.py              # Scale-invariant normalized smoothness
│   └── metric3.py              # Conservative composite metric
├── Algorithms/             # B-spline fitting prototypes
│   ├── b-spline.py             # Quantile-based knot approach
│   └── b-spline-part-two.py    # Simplified splrep/splev approach
├── Graphs/                 # Visualization notebooks
│   ├── BirdDataGraph.ipynb     # Bird trajectory analysis
│   ├── SimulationDataGraph.ipynb
│   ├── CoordinatesGraph.ipynb
│   └── Squashing.ipynb
├── datasets/               # Raw + processed data (not tracked in git)
│   └── DODData/Default/        # Raw Mil.Airforce.Mc2.Sdk device files
├── requirements.txt
└── .gitignore
```

## Pipeline

```
Raw DOD Files → Parse → Feature Engineering → Smoothness Metric → Train → Predict → Evaluate → MLflow
```

1. **Parse**: Ingests raw DOD `DeviceAdds` files, extracts nested key-value pairs into a flat DataFrame with 113+ columns, and converts epoch detection times to datetime.
2. **Feature Engineering**: Adds `Signal Persistence` (frequent detections within 6s), `Altitude Consistent`, speed conversion (m/s → mph), and a binary `Drone` label derived from the `Ninja` field.
3. **Smoothness Metric**: For each threat, builds a time-series of 3D distance from a reference point using Haversine, fits a B-spline, evaluates at 60 pts/sec, and computes metric m2 over sliding windows. Average m2 in range (0.2, 0.5) indicates drone-like smoothness.
4. **Training**: Trains three classifiers — Decision Tree, XGBoost Random Forest, and Random Forest — using SelectKBest (k=30) feature selection with forced inclusion of priority features.
5. **Prediction**: Applies the same impute → scale → feature-select pipeline to predict on individual threat IDs.
6. **Evaluation**: Aggregates predictions per ThreatId, computes confusion matrix, precision, recall, and F1 score.
7. **MLflow**: Logs parameters, metrics, and model artifacts to a local MLflow server for experiment tracking and model registry.

## Smoothness Metrics

| Metric | Description |
|--------|-------------|
| **m1** | Variance of successive differences around the mean step — measures trajectory jitter |
| **m2** | m1 normalized by average absolute step — scale-invariant smoothness measure |
| **m3** | min(m1, 0.5 · m2) — conservative combination |

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install xgboost mlflow
```

## Usage

1. Place raw DOD data files in `datasets/DODData/Default/`.
2. (Optional) Start the MLflow server:
   ```bash
   mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns --host 127.0.0.1 --port 5000
   ```
3. Open `UIImplementation/UIImplementation.ipynb` and run cells sequentially.

## Dependencies

- Python 3.x
- pandas, numpy, scipy, scikit-learn, matplotlib
- xgboost
- mlflow
