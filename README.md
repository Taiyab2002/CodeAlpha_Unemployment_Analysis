# Unemployment Analysis with Python — CodeAlpha Task 2

## Overview
This project explores the supplied **Unemployment in India** dataset using Python, Pandas, Matplotlib and Seaborn. It covers data cleaning, exploratory data analysis, unemployment trends, regional differences, Rural/Urban comparisons, an exploratory calendar-month pattern, and a descriptive comparison around the COVID-19 period.

## Objectives
- Clean and inspect the supplied unemployment dataset.
- Visualize changes in estimated unemployment rates over time.
- Compare average unemployment rates across regions and Rural/Urban areas.
- Compare observations before March 2020 with observations from March 2020 onward.
- Explore month-of-year variation while being transparent about the short time span.
- Present cautious, evidence-linked observations relevant to policy discussions.

## Dataset
File: `Unemployment in India.csv`

The analysis uses the Region, Date, Frequency, Estimated Unemployment Rate (%), Estimated Employed, Estimated Labour Participation Rate (%), and Area columns. The script parses dates, converts numeric columns, removes fully blank rows, and drops rows missing required fields. It prints how many rows are retained and dropped.

## Tools
- Python
- Pandas
- Matplotlib
- Seaborn

## Project structure
```text
CodeAlpha_Unemployment_Analysis/
├── Unemployment in India.csv
├── unemployment_analysis.py
├── requirements.txt
├── README.md
└── outputs/
    ├── monthly_unemployment_trend.png
    ├── unemployment_by_region.png
    ├── rural_vs_urban.png
    ├── regional_monthly_heatmap.png
    └── calendar_month_pattern_exploratory.png
```

## How to run (Windows PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python unemployment_analysis.py
```

The script writes charts to `outputs/` and prints descriptive statistics, COVID-period comparison, regional rankings, month-of-year summaries, limitations, and policy-relevant observations to the terminal.

## Visualizations
1. **Monthly unemployment trend** — monthly average rate with a March 2020 marker.
2. **Average unemployment by region** — compares regional averages.
3. **Rural vs Urban distribution** — compares the distribution of observed rates.
4. **Regional monthly heatmap** — shows month-by-month regional variation.
5. **Calendar-month pattern (exploratory)** — compares average rates by calendar month.

## Key findings from the current run
The current dataset run retained 740 rows across 28 regions, covering 31 May 2019 to 30 June 2020. The overall mean estimated unemployment rate was 11.79% and the median was 8.35%. The mean was 10.32% for Rural observations and 13.17% for Urban observations.

The mean rate before March 2020 was 9.51%, compared with 17.77% from March 2020 onward, a descriptive increase of 8.26 percentage points. The highest individual record was 76.74% for Puducherry, Urban, in April 2020. These figures describe the supplied dataset and should not be interpreted as national estimates without checking the dataset's methodology and representativeness.

## Interpretation and limitations
- **COVID-period comparison:** the before/after comparison is descriptive. It does not establish that COVID-19 alone caused the observed change.
- **Seasonality:** the dataset covers only about 13 months, so it cannot establish a recurring annual seasonal pattern. The calendar-month chart is exploratory; several years of consistent monthly data would be needed for stronger seasonality analysis.
- **Policy observations:** regional and Rural/Urban differences can identify areas for further investigation, but this analysis alone cannot explain their causes or justify a specific policy. More detailed and representative labour-market data would be needed.
- The results depend on the supplied dataset and its data quality.

## CodeAlpha task alignment
- [x] Analyze unemployment-rate data.
- [x] Use Python for data cleaning, exploration and visualization.
- [x] Investigate changes around the COVID-19 period with a transparent descriptive comparison.
- [x] Explore monthly patterns and state the limitation around recurring seasonality.
- [x] Present cautious, data-linked observations relevant to economic and social policy.

## Internship
CodeAlpha Data Science Internship — Task 2: Unemployment Analysis with Python.
