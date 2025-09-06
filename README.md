
# Assessment — Data Science(Intern)

This project solves the Junior Data Scientist assessment by Vanilla Steel, consisting of two main tasks:

---

## Project Structure

```
vanilla-steel-assessment/
│
├── data/                # Input Excel/CSV/TSV files
├── output/              # Final results (inventory_dataset.csv, top3.csv)
├── scripts/notebooks/   # Jupyter notebooks for cleaning and similarity
├── src/                 # Optional functions (to modularize code)
├── run.py               # Main pipeline script
├── README.md            # You are here
├── requirements.txt     # Dependencies
```

---

### Scenario A: Supplier Data Cleaning

- Loaded two messy Excel files (supplier_data1.xlsx, supplier_data2.xlsx)
- Standardized column names (e.g., Thickness (mm) → thickness_mm)
- Converted values like thickness, width, and weight into proper numeric format
- Handled missing values and unified the schema across both suppliers
- Added a data_source column to distinguish entries from each supplier
- Merged both datasets into a single DataFrame called inventory_dataset
- Saved the clean output as output/inventory_dataset.csv

### Scenario B: RFQ Similarity

- Loaded RFQ requests and reference steel grade properties
- Normalized grade keys (e.g., stripping spaces and converting to uppercase)
- Parsed string ranges like ≤0.12 or 500–700 into numerical min/max/mid values
- Engineered similarity features:
- IoU (intersection-over-union) for thickness and width
- Exact match flags for form and finish
- Numeric similarity for yield_strength and tensile_strength
- Used cosine similarity to compare each RFQ to all others
- Selected the top-3 most similar RFQs for each line (excluding self-matches)
- Saved results to output/top3.csv

---

## How to Run

### Option 1: Run script

```bash
python run.py
```

### ▶️ Option 2: Run notebooks step-by-step

- `scripts/notebooks/combine.ipynb` → Task A
- `scripts/notebooks/RFQ Similarity.ipynb` → Task B

---

## Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Similarity Logic

  - Uses a weighted average of:
  - IoU for thickness and width
  - Exact match for form/finish
  - Normalized yield & tensile midpoints
  - Top-3 most similar RFQs are selected using cosine similarity

---

## Submission Files

- `output/inventory_dataset.csv`
- `output/top3.csv`
