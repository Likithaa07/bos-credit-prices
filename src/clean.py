"""
Step 2: Clean the BOS registers and audit their quality.

Input : data/interim/transactions.csv, supply.csv, demand.csv  (from parse_raw.py)
        data/raw/g1-data.csv                                    (RBA Table G1, CPI)
Output: data/clean/sales.csv, retirements.csv, supply.csv
        outputs/audit_log.csv, outputs/completeness.csv

Every removed or flagged row is recorded in the audit log.
"""
import csv
import re
from pathlib import Path

import ftfy
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
INTERIM, RAW = ROOT / "data" / "interim", ROOT / "data" / "raw"
CLEAN, OUT = ROOT / "data" / "clean", ROOT / "outputs"
CLEAN.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)

LOW_PRICE = 100   # $/credit: prices above $1 but below this are likely lump sums
PERSONAL = ["Business Name", "Business Phone", "Business Email", "Contact First Name",
            "Contact Last Name", "Contact Email", "Contact Phone", "Contact Mobile", "Lot and Plan"]

audit = []
def log(step, rows_in, rows_out, note=""):
    audit.append({"step": step, "rows_in": rows_in, "rows_out": rows_out,
                  "removed": rows_in - rows_out, "note": note})


def fix(value):
    """Repair garbled text such as 'Blakelyâ€™s' -> 'Blakely's'."""
    return ftfy.fix_text(value) if isinstance(value, str) else value


def key(value):
    """Matching key: repaired, lower case, punctuation removed (keeps % < > =)."""
    if not isinstance(value, str):
        return np.nan
    value = ftfy.fix_text(value).lower()
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9%<>=]+", " ", value)).strip()


def financial_year(d):
    y = d.year + (d.month >= 7)
    return f"{y - 1}-{str(y)[2:]}"


def load_cpi():
    """Quarterly CPI (all groups, series GCPIAG) from RBA Table G1."""
    rows = list(csv.reader(open(RAW / "g1-data.csv", encoding="utf-8-sig")))
    r = next(i for i, x in enumerate(rows) if x and x[0].strip() == "Series ID")
    c = rows[r].index("GCPIAG")
    cpi = pd.DataFrame([(x[0], x[c]) for x in rows[r + 1:] if len(x) > c],
                       columns=["date", "cpi"])
    cpi["date"] = pd.to_datetime(cpi["date"], dayfirst=True, errors="coerce")
    cpi["cpi"] = pd.to_numeric(cpi["cpi"], errors="coerce")
    cpi = cpi.dropna()
    cpi["quarter"] = cpi["date"].dt.to_period("Q")
    return cpi.set_index("quarter")["cpi"]


# ---------------------------------------------------------------- transactions
t = pd.read_csv(INTERIM / "transactions.csv")
n0 = len(t)
log("Raw Credit Transactions Register", n0, n0, f"{t.shape[1]} fields")

garbled = t.astype(str).apply(lambda col: col.str.contains("â|Ã")).any(axis=1).sum()
t = t.map(fix)
t["txn_id"] = t["Transaction ID"].astype(str).str.extract(r"(\d+)", expand=False)
t["date"] = pd.to_datetime(t["Transaction Date"], format="%B %d, %Y", errors="coerce")
t["n"] = pd.to_numeric(t["Number Of Credits"], errors="coerce")
t["price"] = pd.to_numeric(t["Price Per Credit (Ex-Gst)"], errors="coerce")
t["credit_class"] = np.where(t["Plant Community Type"].notna(), "Ecosystem", "Species")
t["credit_type"] = np.where(t["credit_class"] == "Ecosystem",
                            t["Plant Community Type"], t["Scientific Name"])
t["type_key"] = t["credit_type"].map(key)
t["trading_group_key"] = t["Offset Trading Group"].map(key)
t["subregion"] = t["Sub Region"].astype(str).str.strip()
t["formation"] = np.where(t["credit_class"] == "Ecosystem",
                          t["Vegetation Formation"].fillna("Unknown"), "Species credit")

bad = t["date"].isna() | t["Transaction Type"].isna()
log("Remove rows with unreadable date or missing transaction type", len(t), int((~bad).sum()),
    f"text encoding repaired in {garbled} rows")
t = t[~bad].copy()
t["financial_year"] = t["date"].map(financial_year)

# Like-for-like unit (simplified BOS rules):
# species credits trade by species anywhere in NSW;
# ecosystem credits by offset trading group within the same IBRA subregion.
t["l4l_unit"] = np.where(t["credit_class"] == "Species",
                         "SP|" + t["type_key"].astype(str),
                         "EC|" + t["trading_group_key"].astype(str) + "|" + t["subregion"])

# ---------------------------------------------------------------- retirements
ret = t[t["Transaction Type"] == "Retire"].copy()
ret["by_bct"] = ret["Retirement Reason"].astype(str).str.contains("BCT").astype(int)
bct_retired_ids = set(ret.loc[ret["by_bct"] == 1, "From"])

# ---------------------------------------------------------------- sales
s = t[t["Transaction Type"] == "Transfer"].copy()
log("Keep market sales (transfers)", len(t), len(s),
    f"{(t['Transaction Type'] == 'Retire').sum()} retirements and "
    f"{(t['Transaction Type'] == 'Cancelled').sum()} cancellations kept separately")

s["flag_nominal"] = s["price"] <= 1
s["flag_philanthropic"] = s["Philanthropic Reason For Transfer Disclosed"].eq("Yes")
s["flag_low_price"] = (s["price"] > 1) & (s["price"] < LOW_PRICE)
s["sold_to_bct"] = s["To"].isin(bct_retired_ids).astype(int)
types_in_txn = s.groupby("txn_id")["type_key"].transform("nunique")
prices_in_txn = s.groupby("txn_id")["price"].transform("nunique")
s["bundled"] = ((types_in_txn > 1) & (prices_in_txn == 1)).astype(int)

for flag, label in [("sold_to_bct", "sold to the BCT (credits later retired for a BCT obligation)"),
                    ("bundled", "several credit types sold at one average price"),
                    ("flag_low_price", f"price above $1 but below ${LOW_PRICE} (likely lump sum)")]:
    log(f"Flag (kept): {label}", len(s), len(s), f"{int(s[flag].sum())} rows")

sales = s[~(s["flag_nominal"] | s["flag_philanthropic"])].copy()
log("Exclude transfers at $1 or less and philanthropic transfers", len(s), len(sales),
    f"{int(s['flag_nominal'].sum())} at $1 or less; {int(s['flag_philanthropic'].sum())} philanthropic")

# Real prices in the latest CPI quarter's dollars
cpi = load_cpi()
latest = cpi.index.max()
q = sales["date"].dt.to_period("Q")
sales["cpi"] = q.map(cpi).fillna(cpi[latest])      # sales after the latest quarter use its index
sales["real_price"] = sales["price"] * cpi[latest] / sales["cpi"]
sales["value"] = sales["n"] * sales["price"]
sales["real_value"] = sales["n"] * sales["real_price"]
log("Convert prices to real terms (RBA Table G1 CPI)", len(sales), len(sales),
    f"{latest} prices")

# ---------------------------------------------------------------- supply
sp = pd.read_csv(INTERIM / "supply.csv")
log("Raw Credit Supply Register", len(sp), len(sp), "personal contact fields removed")
sp = sp.drop(columns=[c for c in PERSONAL if c in sp.columns]).map(fix)
sp["credit_class"] = sp["Ecosystem or Species"]
sp["type_key"] = np.where(sp["credit_class"] == "Ecosystem",
                          sp["Plant Community Type Common Name"].map(key),
                          sp["Species Scientific Name"].map(key))
sp["trading_group_key"] = sp["Offset Trading Group"].map(key)
sp["subregion"] = sp["IBRA Subregion"].astype(str).str.strip()
sp["n"] = pd.to_numeric(sp["Number of credits"], errors="coerce").fillna(0)
sp["l4l_unit"] = np.where(sp["credit_class"] == "Species",
                          "SP|" + sp["type_key"].astype(str),
                          "EC|" + sp["trading_group_key"].astype(str) + "|" + sp["subregion"])

demand = pd.read_csv(INTERIM / "demand.csv")
log("Credit Demand Register", len(demand), len(demand),
    "no listings; retirements used as revealed demand")

# ---------------------------------------------------------------- completeness
comp = []
for col in ["Plant Community Type", "Scientific Name", "Sub Region", "Number Of Credits",
            "Price Per Credit (Ex-Gst)"]:
    comp.append({"register": "Transactions (sales)", "field": col,
                 "pct_missing": round(s[col].isna().mean() * 100, 1)})
for col in ["IBRA Subregion", "Date Credits Issued", "Listed Date", "Site Area (HA)", "LGA", "BSA ID"]:
    v = sp[col].astype(str).str.strip().replace({"": np.nan, "nan": np.nan})
    comp.append({"register": "Supply", "field": col, "pct_missing": round(v.isna().mean() * 100, 1)})

# ---------------------------------------------------------------- save
sales.to_csv(CLEAN / "sales.csv", index=False)
ret.to_csv(CLEAN / "retirements.csv", index=False)
sp.to_csv(CLEAN / "supply.csv", index=False)
pd.DataFrame(audit).to_csv(OUT / "audit_log.csv", index=False)
pd.DataFrame(comp).to_csv(OUT / "completeness.csv", index=False)

print(pd.DataFrame(audit)[["step", "rows_in", "rows_out", "note"]].to_string(index=False))