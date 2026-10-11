"""
Step 5: What explains biodiversity credit prices?

Hedonic regression of log real price per credit, built up in steps, then robustness checks.
Standard errors are clustered by the seller's credit record.

Demand pressure at sale = credits of the same like-for-like unit retired in the 36 months
before the sale (time-varying, so it avoids using the export-date snapshot).

Input : data/clean/sales.csv, retirements.csv; outputs/scarcity_like_for_like.csv
Output: outputs/model_ladder.csv, robustness.csv, models_full.txt
"""
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parents[1]
CLEAN, OUT = ROOT / "data" / "clean", ROOT / "outputs"
REFORM_DATE = pd.Timestamp("2025-03-07")   # Biodiversity Conservation Amendment Act commenced

sales = pd.read_csv(CLEAN / "sales.csv", parse_dates=["date"])
ret = pd.read_csv(CLEAN / "retirements.csv", parse_dates=["date"])
scarcity = pd.read_csv(OUT / "scarcity_like_for_like.csv")

m = sales[sales["price"] > 1].copy()

# Demand pressure: same like-for-like unit, 36 months before each sale
ret_by_unit = {unit: g[["date", "n"]].sort_values("date") for unit, g in ret.groupby("l4l_unit")}
def demand_36m(row):
    g = ret_by_unit.get(row["l4l_unit"])
    if g is None:
        return 0.0
    window = (g["date"] >= row["date"] - pd.DateOffset(months=36)) & (g["date"] < row["date"])
    return float(g.loc[window, "n"].sum())
m["demand_36m"] = m.apply(demand_36m, axis=1)

# Variables
m["log_price"] = np.log(m["real_price"])
m["log_lot"] = np.log(m["n"])
m["log_demand"] = np.log1p(m["demand_36m"])
m["species"] = (m["credit_class"] == "Species").astype(int)
m["post_reform"] = (m["date"] >= REFORM_DATE).astype(int)
m["years"] = (m["date"] - m["date"].min()).dt.days / 365.25
m = m.merge(scarcity[["l4l_unit", "scarcity_index"]], on="l4l_unit", how="left")
m["scarcity_index"] = m["scarcity_index"].fillna(m["scarcity_index"].min())
# pool small groups so every category has at least 10 sales
counts = m["subregion"].value_counts()
m["subregion_g"] = m["subregion"].where(m["subregion"].map(counts) >= 10, "Other")
counts = m["formation"].value_counts()
m["formation_g"] = m["formation"].where(m["formation"].map(counts) >= 10, "Other ecosystem")

F = "C(formation_g, Treatment('Species credit'))"
ladder = {
    "M1 Credit class + year": "log_price ~ species + C(financial_year)",
    "M2 + Vegetation formation": f"log_price ~ {F} + C(financial_year)",
    "M3 + IBRA subregion": f"log_price ~ {F} + C(financial_year) + C(subregion_g)",
    "M4 + Demand pressure, lot size, BCT, bundle":
        f"log_price ~ {F} + C(financial_year) + C(subregion_g) + log_demand + log_lot + sold_to_bct + bundled",
    "M5 Trend + post-reform":
        f"log_price ~ {F} + years + post_reform + C(subregion_g) + log_demand + log_lot + sold_to_bct + bundled",
}
KEY = ["species", "log_demand", "scarcity_index", "log_lot", "sold_to_bct", "bundled", "post_reform", "years"]


def clustered(data, formula):
    return smf.ols(formula, data=data).fit(cov_type="cluster",
                                           cov_kwds={"groups": pd.factorize(data["From"])[0]})


def summarise(name, res, n=None):
    row = {"model": name, "n": int(n or res.nobs),
           "adj_r2": round(getattr(res, "rsquared_adj", np.nan), 3)}
    for v in KEY:
        if v in res.params:
            row[v] = round(res.params[v], 4)
            row[v + "_p"] = round(res.pvalues[v], 4)
    return row


rows, text = [], []
for name, formula in ladder.items():
    res = clustered(m, formula)
    rows.append(summarise(name, res))
    text.append(f"===== {name}\n{res.summary()}\n")
pd.DataFrame(rows).to_csv(OUT / "model_ladder.csv", index=False)

# Robustness checks on M4
f4 = ladder["M4 + Demand pressure, lot size, BCT, bundle"]
rob = [
    summarise("R0 Main model (M4)", clustered(m, f4)),
    summarise("R1 Exclude prices below $100", clustered(m[~m["flag_low_price"]], f4)),
    summarise("R2 Exclude bundled sales", clustered(m[m["bundled"] == 0], f4.replace(" + bundled", ""))),
    summarise("R3 Exclude sales to the BCT", clustered(m[m["sold_to_bct"] == 0], f4.replace(" + sold_to_bct", ""))),
    summarise("R4 Weighted by credits sold",
              smf.wls(f4, data=m, weights=m["n"]).fit(cov_type="cluster",
                                                      cov_kwds={"groups": pd.factorize(m["From"])[0]})),
    summarise("R5 Static scarcity index instead", clustered(m, f4.replace("log_demand", "scarcity_index"))),
    summarise("R6 Median (quantile) regression",
              smf.quantreg(f4, data=m).fit(q=0.5, max_iter=5000), n=len(m)),
]
pd.DataFrame(rob).to_csv(OUT / "robustness.csv", index=False)
(OUT / "models_full.txt").write_text("Dependent variable: log real price per credit\n\n" + "\n".join(text))

show = ["model", "n", "adj_r2", "log_demand", "log_demand_p", "log_lot", "log_lot_p", "bundled", "bundled_p"]
print(pd.DataFrame(rows).reindex(columns=show + ["post_reform", "post_reform_p", "years", "years_p"]).to_string(index=False))
print()
print(pd.DataFrame(rob).reindex(columns=show + ["scarcity_index", "scarcity_index_p"]).to_string(index=False))