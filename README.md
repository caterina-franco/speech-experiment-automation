# Speech Experiment Automation & Operational Sheet Generator

An automated Python pipeline built to handle trial randomization, multi-factor experimental balancing, and styled Excel sheet generation for psychoacoustic speech testing sessions.

## 📌 Context & The Operational Problem
Conducting controlled acoustic and perception experiments across multiple participants requires rigorous procedural consistency:
- **Combinatorial Balancing:** Randomizing real vs. virtual stimuli, topics, and speaker positions without introducing human bias.
- **Manual Overhead:** Structuring multi-tab spreadsheets manually for test conductors is slow, error-prone, and visually inconsistent.
- **Trial Integrity:** Ensuring identical split-half breaks and structured response tracking forms for session conductors.

## ⚙️ Solution Architecture
This tool replaces manual trial design with an automated script:

1. **Combinatorial Experiment Logic (`crea_esperimento`):**
   - Extracts balanced subsets of topics from category databases (`DB_VIRTUALI`, `DB_REALI`).
   - Balances physical speaker outputs (positions 1–4) uniformly across real and virtual sound modes.
   - Shuffles visual participant placements dynamically while ensuring exact target speaker alignment.
2. **Operational Spreadsheet Automation (`openpyxl` & `pandas`):**
   - Automatically generates multi-sheet workbooks partitioned by participant ID.
   - Embeds standardized answer matrices (Yes/No validation, confidence ratings, and conductor notes).
   - Applies automated styling: dynamic row heights, header fills, soft-colored highlighting for virtual trials, and distinct border demarcation marking trial milestones (e.g., halfway break at trial 16).

## 🛠️ Tech Stack
- **Python 3**
- **Pandas:** Data modeling and tabular structuring.
- **OpenPyXL:** Advanced spreadsheet formatting (fills, borders, column widths, font scaling).

## 🚀 How to Run

1. Clone this repository:
   ```bash
   git clone [https://github.com/YOUR-USERNAME/speech-experiment-automation.git](https://github.com/YOUR-USERNAME/speech-experiment-automation.git)
   cd speech-experiment-automation
