# sales-data-visualization

==============================================================
  PROJECT 1 – TIME SERIES & CATEGORY CHARTS  |  SUMMARY
==============================================================

DATASET
  • Records   : 3,655  (daily sales per category, 2023–2024)
  • Categories: Electronics, Clothing, Furniture, Sports, Books
  • Regions   : North, South, East, West

KEY METRICS
  • Total Revenue (2yr)  : $1.35 Million
  • Best Month           : 2023-05  ($72.2K)
  • Year-over-Year Growth: -0.3%
  • Top Category         : Furniture (37.9% share)

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
     → Exploded wedges + % labels show Furniture leads at ~38%
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
