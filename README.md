# Experimental Data Automation & Statistical Evaluation Pipeline

An end-to-end Python pipeline built for experimental acoustic research: from automated trial balancing and operational test-sheet generation, to automated multi-participant data aggregation and statistical performance modeling.

---

## 📌 The Operational Problem
Manual workflows in multi-subject experiments introduce two primary bottlenecks:
1. **Upstream manual overhead:** Generating randomized, balanced testing sheets manually across participants is slow, prone to human error, and creates formatting inconsistencies.
2. **Downstream analytical friction:** Aggregating trial data across dozens of spreadsheets, merging demographic metadata, and producing statistical performance reports by hand is repetitive and error-prone.

---

## ⚙️ Pipeline Architecture

### 1. Operational Sheet Generator (`generate_experiment_sheets.py`)
- **Combinatorial Balancing:** Randomizes stimuli, topics, and speaker positions (1–4) without constraint violations or human bias.
- **Automated Spreadsheet Styling:** Leverages `openpyxl` to build participant-specific Excel tabs with custom palettes, row heights, and distinct midpoint break borders.

### 2. Data Processing & Statistical Evaluation (`data_analysis_pipeline.py`)
- **Multi-Source Data Ingestion:** Automates reading and concatenation across 20 participant sheets, merging demographic metadata tables.
- **Classification Performance Metrics:** Computes Accuracy, Precision, Recall, and Macro F1-scores globally and segmented across demographic cohorts.
- **Statistical Curves & Visual Reporting:**
  - Normalized and absolute confusion matrices.
  - Global and parametric ROC-AUC and Precision-Recall (PRC) curves.
  - Inter-subject variability analysis via box plots.
- **Automated Export:** Outputs formatted evaluation reports and PDF figures directly into structured directories.

---

## 🛠️ Tech Stack
- **Language:** Python 3
- **Data Manipulation:** `pandas`, `numpy`
- **Statistical Modeling & Metrics:** `scikit-learn`
- **Visualization & Reporting:** `matplotlib`, `seaborn`, `openpyxl`

---

## 🚀 Execution Overview

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   python generate_experiment_sheets.py
   python data_analysis.py
