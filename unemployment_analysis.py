"""
CodeAlpha Task 2: Unemployment Analysis with Python

Dataset: Unemployment in India.csv
Libraries: pandas, matplotlib, seaborn

This script cleans the supplied dataset, explores unemployment patterns,
compares Rural and Urban areas, examines the 2020 COVID-period change, and
saves visualizations in the outputs/ folder.
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "Unemployment in India.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

sns.set_theme(style="whitegrid")

# 1. Load data
df = pd.read_csv(DATA_PATH)
df.columns = df.columns.str.strip()

required_columns = [
    "Region",
    "Date",
    "Frequency",
    "Estimated Unemployment Rate (%)",
    "Estimated Employed",
    "Estimated Labour Participation Rate (%)",
    "Area",
]
missing_columns = [column for column in required_columns if column not in df.columns]
if missing_columns:
    raise ValueError(f"Dataset is missing required columns: {missing_columns}")

# 2. Clean data: remove fully blank rows, standardize text, parse dates,
# and drop rows missing fields required for this analysis.
df = df.dropna(how="all").copy()
for column in ["Region", "Frequency", "Area"]:
    df[column] = df[column].astype("string").str.strip()

df["Date"] = pd.to_datetime(df["Date"].astype("string").str.strip(),
                            format="%d-%m-%Y", errors="coerce")
numeric_columns = [
    "Estimated Unemployment Rate (%)",
    "Estimated Employed",
    "Estimated Labour Participation Rate (%)",
]
for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

before_rows = len(df)
df = df.dropna(subset=required_columns).copy()
df["Region"] = df["Region"].str.title()
df["Area"] = df["Area"].str.title()
df = df.sort_values("Date")

print("\n=== DATA CLEANING SUMMARY ===")
print(f"Rows after removing fully blank rows and before required-field cleanup: {before_rows}")
print(f"Rows retained for analysis: {len(df)}")
print(f"Rows dropped due to missing/invalid required values: {before_rows - len(df)}")
print(f"Date range: {df['Date'].min():%d %b %Y} to {df['Date'].max():%d %b %Y}")
print(f"Regions: {df['Region'].nunique()}")
print(f"Areas: {', '.join(sorted(df['Area'].dropna().unique()))}")

print("\n=== DATASET OVERVIEW ===")
print(df.head().to_string(index=False))
print("\nDescriptive statistics:")
print(df[numeric_columns].describe().round(2).to_string())

print("\n=== OVERALL FINDINGS ===")
print(f"Mean estimated unemployment rate: {df['Estimated Unemployment Rate (%)'].mean():.2f}%")
print(f"Median estimated unemployment rate: {df['Estimated Unemployment Rate (%)'].median():.2f}%")
print(f"Highest recorded row-level unemployment rate: {df['Estimated Unemployment Rate (%)'].max():.2f}%")
highest_row = df.loc[df["Estimated Unemployment Rate (%)"].idxmax()]
print(f"Highest-rate record: {highest_row['Region']}, {highest_row['Area']}, "
      f"{highest_row['Date']:%B %Y} ({highest_row['Estimated Unemployment Rate (%)']:.2f}%)")

# Aggregate observations to monthly averages across regions/areas.
monthly = (
    df.groupby(df["Date"].dt.to_period("M"))["Estimated Unemployment Rate (%)"]
      .mean()
      .reset_index()
)
monthly["Date"] = monthly["Date"].dt.to_timestamp()
monthly = monthly.sort_values("Date")

# Chart 1: monthly trend
plt.figure(figsize=(11, 6))
sns.lineplot(data=monthly, x="Date", y="Estimated Unemployment Rate (%)",
             marker="o", linewidth=2)
plt.axvline(pd.Timestamp("2020-03-01"), linestyle="--", color="red",
            label="COVID-19 period marker (March 2020)")
plt.title("Average Estimated Unemployment Rate Over Time")
plt.xlabel("Month")
plt.ylabel("Estimated unemployment rate (%)")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "monthly_unemployment_trend.png", dpi=160)
plt.close()

# Chart 2: region averages
region_avg = (
    df.groupby("Region", as_index=False)["Estimated Unemployment Rate (%)"]
      .mean()
      .sort_values("Estimated Unemployment Rate (%)", ascending=False)
)
plt.figure(figsize=(11, 8))
sns.barplot(data=region_avg, x="Estimated Unemployment Rate (%)", y="Region", color="steelblue")
plt.title("Average Estimated Unemployment Rate by Region")
plt.xlabel("Average unemployment rate (%)")
plt.ylabel("Region")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "unemployment_by_region.png", dpi=160)
plt.close()

# Chart 3: Rural vs Urban distribution
plt.figure(figsize=(9, 6))
sns.boxplot(data=df, x="Area", y="Estimated Unemployment Rate (%)", color="skyblue")
plt.title("Unemployment Rate Distribution: Rural vs Urban")
plt.xlabel("Area")
plt.ylabel("Estimated unemployment rate (%)")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "rural_vs_urban.png", dpi=160)
plt.close()

# Chart 4: month-by-region heatmap
pivot = df.pivot_table(
    index="Region",
    columns=df["Date"].dt.strftime("%Y-%m"),
    values="Estimated Unemployment Rate (%)",
    aggfunc="mean"
)
plt.figure(figsize=(14, 9))
sns.heatmap(pivot, cmap="YlOrRd", linewidths=0.2, cbar_kws={"label": "Unemployment rate (%)"})
plt.title("Monthly Estimated Unemployment Rate by Region")
plt.xlabel("Month")
plt.ylabel("Region")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "regional_monthly_heatmap.png", dpi=160)
plt.close()

# 3. COVID-period comparison. Use a transparent, descriptive comparison:
# pre-COVID = dates before March 2020; COVID period = March 2020 onward.
pre_covid = df[df["Date"] < "2020-03-01"]["Estimated Unemployment Rate (%)"]
covid_period = df[df["Date"] >= "2020-03-01"]["Estimated Unemployment Rate (%)"]

print("\n=== COVID-PERIOD COMPARISON ===")
if not pre_covid.empty and not covid_period.empty:
    pre_mean = pre_covid.mean()
    covid_mean = covid_period.mean()
    difference = covid_mean - pre_mean
    percent_change = (difference / pre_mean * 100) if pre_mean else float("nan")
    print(f"Mean rate before March 2020: {pre_mean:.2f}%")
    print(f"Mean rate from March 2020 onward: {covid_mean:.2f}%")
    print(f"Difference: {difference:+.2f} percentage points")
    print(f"Relative change: {percent_change:+.2f}%")
    print("Note: this is a descriptive comparison of the supplied data, not proof that COVID-19 alone caused the change.")
else:
    print("Not enough records on both sides of March 2020 for comparison.")

print("\n=== AREA COMPARISON ===")
print(df.groupby("Area")["Estimated Unemployment Rate (%)"].agg(["mean", "median", "count"]).round(2).to_string())

print("\n=== HIGHEST AND LOWEST REGIONAL AVERAGES ===")
print("Highest average:")
print(region_avg.head(5).round(2).to_string(index=False))
print("\nLowest average:")
print(region_avg.tail(5).sort_values("Estimated Unemployment Rate (%)").round(2).to_string(index=False))

print(f"\nCharts saved to: {OUTPUT_DIR}")
