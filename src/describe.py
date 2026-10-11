"""
Step 3: Describe the BOS credit market.

Input : data/clean/sales.csv, retirements.csv  (from clean.py)
Output: outputs/sales_by_year.csv, retirements_by_year.csv, prices_by_formation.csv,
        prices_by_subregion.csv, sales_by_credit_type.csv, market_summary.csv
Prices: 'real' columns are in the latest CPI quarter's dollars.
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CLEAN, OUT = ROOT / "data" / "clean", ROOT / "outputs"

sales = pd.read_csv(CLEAN / "sales.csv", parse_dates=["date"])
ret = pd.read_csv(CLEAN / "retirements.csv", parse_dates=["date"])

summary_cols = dict(
    sales_lines=("price", "size"),
    credits=("n", "sum"),
    value_nominal=("value", "sum"),
    value_real=("real_value", "sum"),
    median_real_price=("real_price", "median"),
    credit_types=("type_key", "nunique"),
)

# 1. Sales by financial year and credit class
by_year = sales.groupby(["financial_year", "credit_class"]).agg(**summary_cols).reset_index()
by_year.to_csv(OUT / "sales_by_year.csv", index=False)

# 2. Retirements by financial year, and the BCT's share
ret["n_bct"] = ret["n"] * ret["by_bct"]
ret_year = ret.groupby("financial_year").agg(
    credits_retired=("n", "sum"), credits_retired_by_bct=("n_bct", "sum")).reset_index()
ret_year["bct_share_pct"] = (ret_year["credits_retired_by_bct"] / ret_year["credits_retired"] * 100).round(1)
ret_year.to_csv(OUT / "retirements_by_year.csv", index=False)

# 3. Prices by vegetation formation (10+ sales)
by_form = sales.groupby("formation").agg(**summary_cols).reset_index()
by_form = by_form[by_form["sales_lines"] >= 10].sort_values("median_real_price", ascending=False)
by_form.to_csv(OUT / "prices_by_formation.csv", index=False)

# 4. Prices by IBRA subregion
by_sub = sales.groupby("subregion").agg(**summary_cols).reset_index().sort_values("value_real", ascending=False)
by_sub.to_csv(OUT / "prices_by_subregion.csv", index=False)

# 5. Sales by credit type
by_type = sales.groupby(["credit_class", "type_key"]).agg(
    credit_type=("credit_type", "first"), **summary_cols).reset_index().sort_values("value_real", ascending=False)
by_type.to_csv(OUT / "sales_by_credit_type.csv", index=False)

# 6. Price spread within the same credit type and subregion (cells with 5+ sales)
spread = sales[sales["price"] > 0].groupby(["type_key", "subregion"])["price"].agg(["size", "min", "max"])
spread = spread[spread["size"] >= 5]

# 7. Headline summary
summary = {
    "period": f"{sales['date'].min():%b %Y} to {sales['date'].max():%b %Y}",
    "sales_lines": len(sales),
    "credits_sold": round(sales["n"].sum()),
    "value_nominal_aud": round(sales["value"].sum()),
    "value_real_aud": round(sales["real_value"].sum()),
    "credit_types_sold": sales["type_key"].nunique(),
    "subregions_with_sales": sales["subregion"].nunique(),
    "median_real_price_ecosystem": round(sales.loc[sales["credit_class"] == "Ecosystem", "real_price"].median()),
    "median_real_price_species": round(sales.loc[sales["credit_class"] == "Species", "real_price"].median()),
    "top10_types_share_of_value_pct": round(by_type["value_real"].head(10).sum() / by_type["value_real"].sum() * 100, 1),
    "types_sold_only_once_pct": round((by_type["sales_lines"] == 1).mean() * 100, 1),
    "typical_max_to_min_price_same_type_and_subregion": round((spread["max"] / spread["min"]).median(), 1),
    "credits_retired": round(ret["n"].sum()),
    "credits_retired_by_bct_pct": round(ret["n_bct"].sum() / ret["n"].sum() * 100, 1),
}
pd.Series(summary, name="value").to_csv(OUT / "market_summary.csv")
print(pd.Series(summary).to_string())