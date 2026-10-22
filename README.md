# Unemployment Analysis with Python — CodeAlpha Task 2

## Overview
This project explores the supplied **Unemployment in India** dataset using Python, pandas, Matplotlib, and Seaborn. It studies estimated unemployment rates over time, differences between regions and Rural/Urban areas, and changes around the COVID-19 period.

## Dataset
File: `Unemployment in India.csv`

Columns used:
- `Region`
- `Date`
- `Frequency`
- `Estimated Unemployment Rate (%)`
- `Estimated Employed`
- `Estimated Labour Participation Rate (%)`
- `Area`

The source CSV contains blank rows/missing values. The script removes fully blank rows, parses dates, converts numeric columns, and drops rows missing fields required for this analysis. It reports the number of retained and dropped rows.

## Analysis
- Dataset inspection and descriptive statistics
- Monthly average unemployment trend
- Average unemployment rate by region
- Rural vs Urban rate distribution
- Region-by-month heatmap
- Descriptive comparison before March 2020 and from March 2020 onward

**Interpretation note:** The COVID-period comparison is descriptive and does not establish that COVID-19 alone caused any observed change. Findings apply to the supplied dataset and its time range.

## Visualizations
Running the script creates these files in `outputs/`:
1. `monthly_unemployment_trend.png`
2. `unemployment_by_region.png`
3. `rural_vs_urban.png`
4. `regional_monthly_heatmap.png`

## Setup
Python 3.10+ is recommended.

```bash
python -m venv .venv
```

Activate the environment on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the analysis:

```bash
python unemployment_analysis.py
```

## Project Structure
```text
CodeAlpha_Unemployment_Analysis/
├── Unemployment in India.csv
├── unemployment_analysis.py
├── requirements.txt
├── README.md
└── outputs/
```

## Internship
Task 2 — Unemployment Analysis with Python, CodeAlpha Data Science Internship.
