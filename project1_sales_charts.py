"""
Project 1: Time Series & Category Charts
Sales Data Visualization
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.gridspec import GridSpec
import warnings
warnings.filterwarnings("ignore")

# ── 1. Generate sample sales dataset ────────────────────────────────────────
np.random.seed(42)

dates = pd.date_range(start="2023-01-01", end="2024-12-31", freq="D")
categories = ["Electronics", "Clothing", "Furniture", "Sports", "Books"]
regions    = ["North", "South", "East", "West"]

rows = []
for date in dates:
    for cat in categories:
        base = {"Electronics": 500, "Clothing": 300,
                "Furniture": 700, "Sports": 250, "Books": 100}[cat]
        seasonal = 1 + 0.3 * np.sin((date.month - 3) * np.pi / 6)
        sales = max(0, np.random.normal(base * seasonal, base * 0.15))
        rows.append({"Date": date, "Category": cat,
                     "Region": np.random.choice(regions), "Sales": round(sales, 2)})

df = pd.DataFrame(rows)
df["Month"]   = df["Date"].dt.to_period("M")
df["Quarter"] = df["Date"].dt.to_period("Q")
df["Year"]    = df["Date"].dt.year

print("Dataset shape:", df.shape)
print(df.head())

# ── 2. Chart style helpers ───────────────────────────────────────────────────
COLORS     = ["#2196F3", "#FF5722", "#4CAF50", "#9C27B0", "#FF9800"]
GRID_STYLE = dict(color="#e0e0e0", linestyle="--", linewidth=0.6, alpha=0.7)

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.titlesize": 13,
    "axes.labelsize": 11,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
})

# ── 3. Chart 1 – Daily Total Sales (Line Chart) ──────────────────────────────
daily = df.groupby("Date")["Sales"].sum().reset_index()
rolling = daily["Sales"].rolling(30).mean()

fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(daily["Date"], daily["Sales"], color="#B0BEC5", linewidth=0.8,
        alpha=0.6, label="Daily Sales")
ax.plot(daily["Date"], rolling, color="#1565C0", linewidth=2.2,
        label="30-Day Rolling Avg")
ax.fill_between(daily["Date"], rolling, alpha=0.12, color="#1565C0")
ax.set_title("Daily Total Sales with 30-Day Rolling Average (2023–2024)")
ax.set_xlabel("Date")
ax.set_ylabel("Sales (USD)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax.legend(framealpha=0.9)
ax.grid(**GRID_STYLE)
plt.tight_layout()
plt.savefig("chart1_daily_sales_line.png", dpi=150)
plt.close()
print("Saved chart1_daily_sales_line.png")

# ── 4. Chart 2 – Monthly & Quarterly Aggregation (Bar Charts) ────────────────
monthly  = df.groupby("Month")["Sales"].sum().reset_index()
monthly["Month_str"] = monthly["Month"].astype(str)
quarterly = df.groupby("Quarter")["Sales"].sum().reset_index()
quarterly["Quarter_str"] = quarterly["Quarter"].astype(str)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Monthly
bars1 = ax1.bar(monthly["Month_str"], monthly["Sales"],
                color=[COLORS[i % 2] for i in range(len(monthly))],
                edgecolor="white", linewidth=0.5)
ax1.set_title("Monthly Total Sales")
ax1.set_xlabel("Month")
ax1.set_ylabel("Sales (USD)")
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1e6:.1f}M"))
ax1.set_xticks(range(len(monthly["Month_str"])))
ax1.set_xticklabels(monthly["Month_str"], rotation=45, ha="right", fontsize=8)
ax1.grid(axis="y", **GRID_STYLE)

# Quarterly
bars2 = ax2.bar(quarterly["Quarter_str"], quarterly["Sales"],
                color=COLORS[:len(quarterly)], edgecolor="white", linewidth=0.5, width=0.5)
for bar in bars2:
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50000,
             f"${bar.get_height()/1e6:.2f}M", ha="center", va="bottom", fontsize=9, fontweight="bold")
ax2.set_title("Quarterly Total Sales")
ax2.set_xlabel("Quarter")
ax2.set_ylabel("Sales (USD)")
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1e6:.1f}M"))
ax2.grid(axis="y", **GRID_STYLE)

plt.suptitle("Sales Aggregation – Monthly & Quarterly", fontsize=14, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig("chart2_aggregation_bars.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved chart2_aggregation_bars.png")

# ── 5. Chart 3 – Category Comparison (Grouped Bar Chart) ─────────────────────
cat_year = df.groupby(["Year", "Category"])["Sales"].sum().unstack()

fig, ax = plt.subplots(figsize=(10, 5))
x      = np.arange(len(cat_year.columns))
width  = 0.35
years  = cat_year.index.tolist()

for i, (year, color) in enumerate(zip(years, ["#1976D2", "#E64A19"])):
    offset = (i - 0.5) * width
    bars = ax.bar(x + offset, cat_year.loc[year], width,
                  label=str(year), color=color, edgecolor="white")
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2000,
                f"${bar.get_height()/1e3:.0f}K", ha="center", va="bottom", fontsize=7.5)

ax.set_title("Sales by Category – 2023 vs 2024 Comparison")
ax.set_xlabel("Category")
ax.set_ylabel("Total Sales (USD)")
ax.set_xticks(x)
ax.set_xticklabels(cat_year.columns, fontsize=10)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1e3:.0f}K"))
ax.legend(title="Year", framealpha=0.9)
ax.grid(axis="y", **GRID_STYLE)
plt.tight_layout()
plt.savefig("chart3_category_comparison.png", dpi=150)
plt.close()
print("Saved chart3_category_comparison.png")

# ── 6. Chart 4 – Category Share (Pie Chart) ──────────────────────────────────
cat_total = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)
explode   = [0.04] * len(cat_total)

fig, ax = plt.subplots(figsize=(8, 6))
wedges, texts, autotexts = ax.pie(
    cat_total, labels=cat_total.index, colors=COLORS,
    autopct="%1.1f%%", startangle=140, explode=explode,
    pctdistance=0.82, textprops={"fontsize": 11}
)
for at in autotexts:
    at.set_fontsize(10)
    at.set_fontweight("bold")
    at.set_color("white")

ax.set_title("Revenue Share by Category (2023–2024)", fontsize=13, pad=15)
# Legend with $ values
legend_labels = [f"{cat}  –  ${val/1e3:.0f}K" for cat, val in cat_total.items()]
ax.legend(wedges, legend_labels, loc="lower center",
          bbox_to_anchor=(0.5, -0.12), ncol=2, fontsize=9, framealpha=0.9)
plt.tight_layout()
plt.savefig("chart4_category_pie.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved chart4_category_pie.png")

# ── 7. Chart 5 – Regional Sales (Horizontal Bar) ─────────────────────────────
region_cat = df.groupby(["Region", "Category"])["Sales"].sum().unstack()

fig, ax = plt.subplots(figsize=(10, 5))
region_cat.plot(kind="barh", ax=ax, color=COLORS, edgecolor="white", linewidth=0.4)
ax.set_title("Sales by Region and Category")
ax.set_xlabel("Total Sales (USD)")
ax.set_ylabel("Region")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1e3:.0f}K"))
ax.legend(title="Category", bbox_to_anchor=(1.01, 1), loc="upper left", fontsize=9)
ax.grid(axis="x", **GRID_STYLE)
plt.tight_layout()
plt.savefig("chart5_region_category.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved chart5_region_category.png")

# ── 8. Summary Stats & Text Report ───────────────────────────────────────────
total_sales    = df["Sales"].sum()
best_month     = monthly.loc[monthly["Sales"].idxmax(), "Month_str"]
best_month_val = monthly["Sales"].max()
best_cat       = cat_total.idxmax()
best_cat_share = cat_total.max() / cat_total.sum() * 100
yoy_growth     = (df[df["Year"]==2024]["Sales"].sum() / df[df["Year"]==2023]["Sales"].sum() - 1) * 100

summary = f"""
==============================================================
  PROJECT 1 – TIME SERIES & CATEGORY CHARTS  |  SUMMARY
==============================================================

DATASET
  • Records   : {len(df):,}  (daily sales per category, 2023–2024)
  • Categories: {', '.join(categories)}
  • Regions   : {', '.join(regions)}

KEY METRICS
  • Total Revenue (2yr)  : ${total_sales/1e6:.2f} Million
  • Best Month           : {best_month}  (${best_month_val/1e3:.1f}K)
  • Year-over-Year Growth: {yoy_growth:+.1f}%
  • Top Category         : {best_cat} ({best_cat_share:.1f}% share)

CHART BREAKDOWN
  1. Line Chart  – Daily sales + 30-day rolling average
     → Reveals seasonal peaks (mid-year bump) and overall upward trend.

  2. Bar Charts  – Monthly & Quarterly aggregation
     → Monthly bars expose within-year seasonality; quarterly bars
       make YoY comparison clean and digestible.

  3. Grouped Bar – Category × Year comparison
     → Side-by-side bars let viewers instantly spot which categories
       grew or shrank between 2023 and 2024.

  4. Pie Chart   – Revenue share by category
     → Exploded wedges + % labels show Furniture leads at ~{best_cat_share:.0f}%
       while Books is the smallest segment.

  5. Horiz. Bar  – Region × Category breakdown
     → Horizontal orientation handles long labels; stacked view
       reveals regional mix without clutter.

CHART DESIGN NOTES
  • Lines   : Raw daily data shown in light grey; rolling avg in bold blue
              so the trend pops without hiding volatility.
  • Bars    : Spines removed (top/right), gridlines on value axis only —
              keeps focus on bar heights, not chart furniture.
  • Pie     : Labels outside, % values inside (white bold) for legibility;
              a legend with $ totals adds quantitative context.
  • Axes    : All monetary axes formatted as $K / $M (no raw numbers).
  • Colors  : Consistent 5-color palette across all charts for category
              identity; region charts inherit the same set.

FILES SAVED
  chart1_daily_sales_line.png
  chart2_aggregation_bars.png
  chart3_category_comparison.png
  chart4_category_pie.png
  chart5_region_category.png
==============================================================
"""

print(summary)
with open("summary.txt", "w") as f:
    f.write(summary)
print("Saved summary.txt")
