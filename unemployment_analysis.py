"""
CodeAlpha Task 2: Unemployment Analysis with Python

Performs data cleaning, exploratory analysis, COVID-period comparison,
month-of-year pattern exploration, and creates visualizations in outputs/.

Important limitation:
The supplied dataset covers only about 13 months. Month-of-year averages are
exploratory comparisons, not reliable evidence of recurring annual seasonality.
The COVID-period comparison is descriptive and does not prove causation.
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
RATE = "Estimated Unemployment Rate (%)"

# 1. Load and validate data
df = pd.read_csv(DATA_PATH)
df.columns = df.columns.str.strip()

required_columns = [
    "Region", "Date", "Frequency", RATE, "Estimated Employed",
    "Estimated Labour Participation Rate (%)", "Area",
]
missing_columns = [column for column in required_columns if column not in df.columns]
if missing_columns:
    raise ValueError(f"Dataset is missing required columns: {missing_columns}")

# 2. Clean data
df = df.dropna(how="all").copy()
for column in ["Region", "Frequency", "Area"]:
    df[column] = df[column].astype("string").str.strip()

df["Date"] = pd.to_datetime(
    df["Date"].astype("string").str.strip(),
    format="%d-%m-%Y",
    errors="coerce",
)

numeric_columns = [RATE, "Estimated Employed", "Estimated Labour Participation Rate (%)"]
for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

rows_before_required_cleanup = len(df)
df = df.dropna(subset=required_columns).copy()
df["Region"] = df["Region"].str.title()
df["Area"] = df["Area"].str.title()
df = df.sort_values("Date")
df["Month"] = df["Date"].dt.month
df["Month Name"] = df["Date"].dt.strftime("%b")
df["Year-Month"] = df["Date"].dt.to_period("M").astype(str)

print("\n" + "=" * 68)
print("DATA CLEANING SUMMARY")
print("=" * 68)
print(f"Rows before required-field cleanup: {rows_before_required_cleanup}")
print(f"Rows retained for analysis: {len(df)}")
print(f"Rows dropped due to missing/invalid required values: {rows_before_required_cleanup - len(df)}")
print(f"Date range: {df['Date'].min():%d %b %Y} to {df['Date'].max():%d %b %Y}")
print(f"Number of regions: {df['Region'].nunique()}")
print(f"Areas included: {', '.join(sorted(df['Area'].dropna().unique()))}")

print("\nDATASET PREVIEW")
print(df.head().to_string(index=False))
print("\nDESCRIPTIVE STATISTICS")
print(df[numeric_columns].describe().round(2).to_string())

print("\n" + "=" * 68)
print("OVERALL FINDINGS")
print("=" * 68)
mean_rate = df[RATE].mean()
median_rate = df[RATE].median()
print(f"Mean estimated unemployment rate: {mean_rate:.2f}%")
print(f"Median estimated unemployment rate: {median_rate:.2f}%")

highest_row = df.loc[df[RATE].idxmax()]
lowest_row = df.loc[df[RATE].idxmin()]
print(
    f"Highest row-level rate: {highest_row[RATE]:.2f}% — "
    f"{highest_row['Region']}, {highest_row['Area']}, {highest_row['Date']:%B %Y}"
)
print(
    f"Lowest row-level rate: {lowest_row[RATE]:.2f}% — "
    f"{lowest_row['Region']}, {lowest_row['Area']}, {lowest_row['Date']:%B %Y}"
)

# 3. Monthly trend averaged across regions and areas
monthly = (
    df.groupby("Year-Month", as_index=False)[RATE]
    .mean()
)
monthly["Date"] = pd.to_datetime(monthly["Year-Month"] + "-01")
monthly = monthly.sort_values("Date")

plt.figure(figsize=(11, 6))
sns.lineplot(data=monthly, x="Date", y=RATE, marker="o", linewidth=2)
plt.axvline(pd.Timestamp("2020-03-01"), linestyle="--", color="red",
            label="March 2020 marker")
plt.title("Average Estimated Unemployment Rate Over Time")
plt.xlabel("Month")
plt.ylabel("Estimated unemployment rate (%)")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "monthly_unemployment_trend.png", dpi=160)
plt.close()

# 4. Average unemployment rate by region
region_avg = (
    df.groupby("Region", as_index=False)[RATE]
    .mean()
    .sort_values(RATE, ascending=False)
)
plt.figure(figsize=(11, 8))
sns.barplot(data=region_avg, x=RATE, y="Region", color="steelblue")
plt.title("Average Estimated Unemployment Rate by Region")
plt.xlabel("Average unemployment rate (%)")
plt.ylabel("Region")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "unemployment_by_region.png", dpi=160)
plt.close()

# 5. Rural vs Urban distribution
plt.figure(figsize=(9, 6))
sns.boxplot(data=df, x="Area", y=RATE, color="skyblue")
plt.title("Unemployment Rate Distribution: Rural vs Urban")
plt.xlabel("Area")
plt.ylabel("Estimated unemployment rate (%)")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "rural_vs_urban.png", dpi=160)
plt.close()

# 6. Region-by-month heatmap
pivot = df.pivot_table(
    index="Region",
    columns="Year-Month",
    values=RATE,
    aggfunc="mean",
)
plt.figure(figsize=(14, 9))
sns.heatmap(pivot, cmap="YlOrRd", linewidths=0.2,
            cbar_kws={"label": "Unemployment rate (%)"})
plt.title("Monthly Estimated Unemployment Rate by Region")
plt.xlabel("Month")
plt.ylabel("Region")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "regional_monthly_heatmap.png", dpi=160)
plt.close()

# 7. Month-of-year comparison (exploratory only)
# This is not proof of recurring seasonality because the dataset spans only ~13 months.
month_order = list(range(1, 13))
month_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
month_pattern = (
    df.groupby("Month")[RATE]
    .agg(["mean", "median", "count"])
    .reindex(month_order)
)
month_pattern["Month Name"] = month_labels

plt.figure(figsize=(11, 6))
sns.barplot(
    data=month_pattern.reset_index(),
    x="Month Name",
    y="mean",
    color="slateblue",
)
plt.title("Average Unemployment Rate by Calendar Month (Exploratory)")
plt.xlabel("Calendar month")
plt.ylabel("Average unemployment rate (%)")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "calendar_month_pattern_exploratory.png", dpi=160)
plt.close()

print("\n" + "=" * 68)
print("COVID-PERIOD COMPARISON")
print("=" * 68)
pre_covid = df.loc[df["Date"] < "2020-03-01", RATE]
covid_period = df.loc[df["Date"] >= "2020-03-01", RATE]

if not pre_covid.empty and not covid_period.empty:
    pre_mean = pre_covid.mean()
    covid_mean = covid_period.mean()
    difference = covid_mean - pre_mean
    relative_change = difference / pre_mean * 100 if pre_mean else float("nan")
    print(f"Mean rate before March 2020: {pre_mean:.2f}%")
    print(f"Mean rate from March 2020 onward: {covid_mean:.2f}%")
    print(f"Difference: {difference:+.2f} percentage points")
    print(f"Relative change: {relative_change:+.2f}%")
    print(
        "Caution: this is a descriptive comparison of the supplied dataset; "
        "it does not prove that COVID-19 alone caused the change."
    )
else:
    print("Not enough records on both sides of March 2020 for comparison.")

print("\nRURAL VS URBAN SUMMARY")
area_summary = df.groupby("Area")[RATE].agg(["mean", "median", "count"]).round(2)
print(area_summary.to_string())

print("\nHIGHEST AND LOWEST REGIONAL AVERAGES")
print("\nHighest average unemployment rates:")
print(region_avg.head(5).round(2).to_string(index=False))
print("\nLowest average unemployment rates:")
print(region_avg.tail(5).sort_values(RATE).round(2).to_string(index=False))

print("\nCALENDAR-MONTH PATTERN — EXPLORATORY")
print(month_pattern[["Month Name", "mean", "median", "count"]].round(2).to_string(index=False))
print(
    "\nSeasonality limitation: the dataset covers only about 13 months, "
    "so it is not long enough to establish a recurring annual seasonal pattern. "
    "The calendar-month chart is exploratory; several years of comparable data "
    "would be needed for stronger seasonal conclusions."
)

# 8. Policy-relevant observations, framed as implications to investigate—not causal claims
highest_regions = region_avg.head(5)["Region"].tolist()
lowest_regions = region_avg.tail(5).sort_values(RATE)["Region"].tolist()
urban_mean = df.loc[df["Area"].str.lower() == "urban", RATE].mean()
rural_mean = df.loc[df["Area"].str.lower() == "rural", RATE].mean()

print("\n" + "=" * 68)
print("POTENTIAL POLICY-RELEVANT OBSERVATIONS")
print("=" * 68)
print(
    f"1. Regional targeting: the highest average rates in this dataset occur in "
    f"{', '.join(highest_regions)}. These regions may warrant closer labour-market "
    "assessment and targeted employment-support evaluation."
)
print(
    f"2. Lower-rate comparison group: the lowest regional averages occur in "
    f"{', '.join(lowest_regions)}. Investigating differences in sector mix, "
    "infrastructure, skills and labour-market conditions could help identify "
    "questions for further study; this analysis alone cannot explain the causes."
)
if pd.notna(urban_mean) and pd.notna(rural_mean):
    higher_area = "Urban" if urban_mean > rural_mean else "Rural"
    gap = abs(urban_mean - rural_mean)
    print(
        f"3. Area-level monitoring: the mean rate is {urban_mean:.2f}% in Urban "
        f"observations and {rural_mean:.2f}% in Rural observations. The {higher_area} "
        f"mean is higher by {gap:.2f} percentage points in this dataset; "
        "employment programmes should be designed using more detailed local and "
        "sector-level evidence rather than this aggregate comparison alone."
    )
print(
    "4. Crisis preparedness: the observed rise around the COVID-19 period supports "
    "monitoring timely labour indicators and evaluating temporary worker-support "
    "measures during major economic disruptions. The before/after comparison is "
    "not a causal impact estimate."
)
print(
    "5. Data improvement: use several years of consistent monthly observations, "
    "along with sector, age, gender and employment-status breakdowns where available, "
    "to assess seasonality and design more precise policy responses."
)

print(f"\nAll charts saved to: {OUTPUT_DIR}")
print("Analysis completed successfully.")
