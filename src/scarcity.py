"""
Step 4: Scarcity and supply gaps.

For each like-for-like unit (species anywhere in NSW; ecosystem trading group within an
IBRA subregion) compare credits retired in the last 36 months with issued credits still
on the Supply Register.

    scarcity index = ln((retired in last 36 months + 1) / (issued supply + 1))
    above 0 -> recent use exceeds what is left

Input : data/clean/retirements.csv, supply.csv, sales.csv
Output: outputs/scarcity_by_credit_type.csv, scarcity_like_for_like.csv,
        supply_gap_by_subregion.csv, scarcity_summary.csv
"""
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu, spearmanr

ROOT = Path(__file__).resolve().parents[1]
CLEAN, OUT = ROOT / "data" / "clean", ROOT / "outputs"
EXPORT_DATE = pd.Timestamp("2026-10-11")      # date the registers were downloaded
WINDOW_START = EXPORT_DATE - pd.DateOffset(months=36)

ret = pd.read_csv(CLEAN / "retirements.csv", parse_dates=["date"])
supply = pd.read_csv(CLEAN / "supply.csv")
sales = pd.read_csv(CLEAN / "sales.csv")
issued = supply[supply["Credit status"] == "Issued"]


def scarcity(level):
    """Retirements vs issued supply, grouped by `level`."""
    out = pd.concat([
        ret.groupby(level)["n"].sum().rename("retired_all"),
        ret[ret["date"] >= WINDOW_START].groupby(level)["n"].sum().rename("retired_36m"),
        ret[ret["by_bct"] == 1].groupby(level)["n"].sum().rename("retired_by_bct"),
        issued.groupby(level)["n"].sum().rename("issued_supply"),
    ], axis=1).fillna(0)
    out = out[out["retired_all"] > 0].copy()           # only units developers have needed
    out["scarcity_index"] = np.log((out["retired_36m"] + 1) / (out["issued_supply"] + 1))
    out["bct_share_pct"] = (out["retired_by_bct"] / out["retired_all"] * 100).round(1)
    out["no_supply_left"] = out["issued_supply"] == 0
    return out


# 1. By credit type (plant community type or species)
names = ret.drop_duplicates(["credit_class", "type_key"]).set_index(["credit_class", "type_key"])["credit_type"]
median_price = sales.groupby(["credit_class", "type_key"])["real_price"].median().rename("median_real_price")
by_type = scarcity(["credit_class", "type_key"]).join(names).join(median_price)
by_type = by_type.reset_index().sort_values("scarcity_index", ascending=False)
by_type.to_csv(OUT / "scarcity_by_credit_type.csv", index=False)

# 2. By like-for-like unit
l4l = scarcity(["l4l_unit"]).reset_index()
parts = l4l["l4l_unit"].str.split("|", expand=True)
l4l["credit_class"] = np.where(parts[0] == "SP", "Species", "Ecosystem")
l4l["subregion"] = np.where(parts[0] == "EC", parts[2], "NSW-wide")
group_names = ret.drop_duplicates("l4l_unit").set_index("l4l_unit")["Offset Trading Group"]
species_names = ret.drop_duplicates("l4l_unit").set_index("l4l_unit")["credit_type"]
l4l["unit_name"] = np.where(l4l["credit_class"] == "Species",
                            l4l["l4l_unit"].map(species_names), l4l["l4l_unit"].map(group_names))
l4l = l4l.sort_values("scarcity_index", ascending=False)
l4l.to_csv(OUT / "scarcity_like_for_like.csv", index=False)

# 3. Ecosystem supply gaps by IBRA subregion
eco = l4l[l4l["credit_class"] == "Ecosystem"].copy()
eco["shortfall_36m"] = (eco["retired_36m"] - eco["issued_supply"]).clip(lower=0)
gap = eco.groupby("subregion").agg(
    trading_groups_needed=("l4l_unit", "nunique"),
    groups_with_no_supply=("no_supply_left", "sum"),
    groups_demand_exceeds_supply=("shortfall_36m", lambda x: int((x > 0).sum())),
    retired_36m=("retired_36m", "sum"),
    issued_supply=("issued_supply", "sum"),
    shortfall_36m=("shortfall_36m", "sum"),
).reset_index().sort_values("shortfall_36m", ascending=False)
gap.to_csv(OUT / "supply_gap_by_subregion.csv", index=False)

# 4. Tests
#   (a) Is scarcity priced?  rank correlation of scarcity index with median price
priced = by_type.dropna(subset=["median_real_price"])
rho = spearmanr(priced["scarcity_index"], priced["median_real_price"])
#   (b) Does the BCT retire scarce credits less often? (it can only retire credits that exist)
none_left, some_left = l4l[l4l["no_supply_left"]], l4l[~l4l["no_supply_left"]]
mw = mannwhitneyu(none_left["bct_share_pct"], some_left["bct_share_pct"])

summary = {
    "credit_types_retired": len(by_type),
    "credit_types_no_supply_left": int(by_type["no_supply_left"].sum()),
    "credit_types_36m_demand_exceeds_supply": int((by_type["retired_36m"] > by_type["issued_supply"]).sum()),
    "l4l_units_retired": len(l4l),
    "l4l_units_no_supply_left": int(l4l["no_supply_left"].sum()),
    "l4l_units_36m_demand_exceeds_supply": int((l4l["retired_36m"] > l4l["issued_supply"]).sum()),
    "subregions_with_ecosystem_shortfall": int((gap["shortfall_36m"] > 0).sum()),
    "scarcity_vs_price_spearman_rho": round(rho.statistic, 3),
    "scarcity_vs_price_p": round(rho.pvalue, 3),
    "scarcity_vs_price_n": len(priced),
    "units_with_bct_retirement_no_supply_pct": round((none_left["retired_by_bct"] > 0).mean() * 100, 1),
    "units_with_bct_retirement_some_supply_pct": round((some_left["retired_by_bct"] > 0).mean() * 100, 1),
    "bct_share_difference_mannwhitney_p": round(mw.pvalue, 4),
}
pd.Series(summary, name="value").to_csv(OUT / "scarcity_summary.csv")
print(pd.Series(summary).to_string())
print("\nLargest ecosystem shortfalls by subregion:")
print(gap.head(8).to_string(index=False))