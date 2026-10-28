# Experimental Data Automation & Analysis Pipeline

A Python pipeline built to automate experimental research: from creating balanced test sheets to aggregating participant data and generating statistical performance reports.

---

## 📌 The Problem
Manual workflows in multi-subject experiments introduce two primary bottlenecks:
1. **Time-consuming setup:** Manually generating randomized and balanced test sheets for each participant is slow and prone to human errors.
2. **Repetitive data collection:** Merging results from dozens of separate spreadsheets and calculating metrics by hand is tedious and inefficient.

---

## ⚙️ Pipeline Architecture

### 1. Test Sheet Generator (`generate_experiment_sheets.py`)
- **Automated Balancing:** Randomizes stimuli, topics, and speaker positions without human bias.
- **Excel Formatting:** Uses `openpyxl` to automatically build clean, structured Excel sheets for testing.

### 2. Data Processing & Metrics (`data_analysis_pipeline.py`)
- **Data Ingestion:** Automatically reads and merges data from 20 participant spreadsheets along with demographic metadata.
- **Performance Evaluation:** Calculates Accuracy, Precision, Recall, and F1-scores across global and specific subgroups.
- **Automated Visualization:** Generates confusion matrices, ROC-AUC curves, and box plots, exporting reports directly to PDF and structured folders.

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
   python3 generate_experiment_sheets.py
   python3 data_analysis.py
