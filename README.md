# What Drives Biodiversity Credit Prices? 🌿

**A spatial and statistical analysis of supply–demand mismatch in the NSW Biodiversity Offsets Scheme**


> **In one line:** biodiversity credits in NSW are priced by *where* they are and *what vegetation* they protect, **not by how scarce they are**. Meanwhile supply has already run out for 78 like-for-like credit units across 34 regions.

---

## 🧭 The problem in 30 seconds

When a developer clears native vegetation in NSW, they must offset it by buying and retiring **biodiversity credits**. Landholders create these credits by protecting land. In a working market, scarce credits should cost more, and that price signal should encourage more landholders to supply them.

**Does that actually happen?** This project tests it using every public sale on record.

| Research question | Short answer so far |
| --- | --- |
| **RQ1** What explains credit prices? | Credit class, vegetation type and location explain **71%** of price variation |
| **RQ2** Do scarce credits sell for more? | **No.** There is no robust scarcity premium across 7 model checks |
| **RQ3** Where has supply run out? | **78** like-for-like units have zero supply, with shortfalls in **34** subregions |

---

## 📊 The market at a glance

| Metric | Value |
| --- | --- |
| Sales analysed | **1,284** (Nov 2019 – Oct 2026) |
| Credits sold | 379,055 |
| Total value | **$788M** real · $732M nominal |
| Credit types traded | 332 across 44 IBRA subregions |
| Median price, ecosystem credit | **$4,268** |
| Median price, species credit | **$813** |
| Credit types sold only once | 40.7% → a very thin market |
| Share of value in top 10 credit types | 51.8% → highly concentrated |

> 💡 **Why real prices?** Converting to June 2026 dollars adds **7.6%** to the total ($788M ÷ $732M). Most of the apparent price rise over time turned out to be inflation.

---

## 🔍 Key findings

### 1. Location matters most (RQ1)

Each model adds one group of factors. The jump in R² shows how much that group explains.

| Model | Adds | Adj. R² | Gain |
| --- | --- | --- | --- |
| M1 | Credit class + year | 0.36 | — |
| M2 | Vegetation formation | 0.45 | +0.09 |
| M3 | **IBRA subregion** | **0.71** | **+0.26** ⬅ biggest jump |
| M4 | Demand, lot size, BCT buyer, bundle | 0.72 | +0.01 |

**What the coefficients mean in plain terms.** The model is in log prices, so each effect is calculated as `% change = (e^β − 1) × 100`:

| Factor | β | Calculation | Effect on price |
| --- | --- | --- | --- |
| Species vs ecosystem credit | −1.654 | e^−1.654 − 1 | **−81%** |
| 10× larger purchase | −0.0434 × ln 10 | e^−0.100 − 1 | **−9.5%** per credit |
| Bundled sale (one average price) | −0.287 | e^−0.287 − 1 | **−25%** |
| Each extra year (real terms) | +0.040 | e^0.040 − 1 | +4.1% (not significant, p = 0.23) |
| After the March 2025 reform | −0.088 | e^−0.088 − 1 | −8.4% (not significant, p = 0.21) |

📍 **Cumberland (western Sydney)** has a median of **$34,005** per credit, which is $34,005 ÷ $4,268 ≈ **8×** the state ecosystem median. This points to land values setting the cost of supply.

### 2. Scarcity is *not* priced (RQ2)

If scarcity mattered, more recent demand should push prices up in every check. Instead the effect is tiny and **flips sign** between checks:

| Check | Effect of a 10× rise in recent demand | p |
| --- | --- | --- |
| Main model (M4) | −3.8% | 0.10 |
| Excluding prices < $100 | −4.9% | 0.02 |
| Excluding bundled sales | −2.1% | 0.43 |
| Excluding sales to the BCT | −5.5% | 0.02 |
| Weighted by credits sold | **+10.9%** | 0.04 |
| Median (quantile) regression | −2.2% | 0.05 |
| Static scarcity index instead | +0.9% per unit of index | 0.40 |

**Why?** Two explanations fit the evidence:
1. The **Biodiversity Conservation Fund** lets developers pay instead of buying credits, which caps what they will pay.
2. Sellers price from their **costs** (land and management), not from scarcity.

### 3. Supply has run out in many places (RQ3)

| | Credit types | Like-for-like units |
| --- | --- | --- |
| Retired since 2019 | 309 | 318 |
| **No supply left** | **50** | **78** |
| Last 3 years of demand > all remaining supply | 108 | 130 |

**Largest shortfalls by subregion** (credits retired in the last 36 months minus remaining supply, summed over trading groups):

| Subregion | Trading groups needed | With zero supply | Shortfall (credits) |
| --- | --- | --- | --- |
| Murrumbidgee | 17 | 3 | 15,335 |
| Lower Slopes | 12 | 3 | 14,898 |
| Hill End | 5 | 1 | 10,445 |
| Northern Outwash | 6 | 1 | 9,183 |
| Kerrabee | 14 | **10** | 8,799 |

⚠️ **The registers understate the shortage.** Units with no supply are *less* likely to show BCT retirements (**21.8% vs 36.7%**, Mann–Whitney p = 0.03). The BCT can only retire credits it manages to buy, so the scarcest obligations never appear in the data.

### 4. The public data needs fixing

- **Demand Register is empty**, so demand has to be inferred from retirements
- **98.8%** of supply records have no site area
- **328** transaction rows had garbled text encoding
- **1 in 5** sales is part of a bundle priced at a single average
- **Buyers aren't recorded**, so 223 BCT purchases were found only by tracing credit IDs

✅ Even so, after cleaning, 2024-25 retirements match IPART's official figures closely: (114,164 − 114,856) ÷ 114,856 = **−0.6%**.

---

## ⚙️ How it works

```
Transactions (2,591) ─┐
Supply (2,852) ───────┤
Demand (0 listings) ──┼──► Audit & cleaning ──► Linked like-for-like dataset ──┬──► RQ1 Price model
RBA CPI ──────────────┘                                                        ├──► RQ2 Scarcity index
                                                                               └──► RQ3 Supply gaps
```

**Price model (hedonic OLS, clustered by seller):**

```
ln(Price) = class + vegetation formation + subregion + year
            + δ·ln(recent demand) + lot size + BCT buyer + bundle + error
```

**Scarcity index for each like-for-like unit:**

```
Scarcity index = ln( (R + 1) / (S + 1) )
```

where *R* = credits retired in the last 36 months and *S* = credits still available.

| Example unit | R (retired) | S (supply) | SI | Meaning |
| --- | --- | --- | --- | --- |
| Sold out | 1,000 | 0 | ln(1001/1) = **+6.9** | Severe shortage |
| Plenty left | 100 | 1,000 | ln(101/1001) = **−2.3** | Well supplied |

---

## 🧹 Data audit trail

Every row removed is logged in [`outputs/audit_log.csv`](outputs/audit_log.csv).

| Step | Rows left |
| --- | --- |
| Raw transactions | 2,591 |
| Remove unreadable rows | 2,589 |
| Keep market sales only | 1,295 |
| Drop ≤ $1 and philanthropic transfers | **1,284** |

Flagged but kept: 223 BCT purchases, 278 bundled sales and 6 likely lump-sum prices. Each is tested in the robustness checks.

---

## 📁 Repository structure

```
bos-credit-prices/
├── src/
│   ├── parse_raw.py    # read HTML/XML register exports
│   ├── clean.py        # repair, flag, deflate, audit
│   ├── describe.py     # market overview tables
│   ├── scarcity.py     # like-for-like scarcity index and gaps
│   └── models.py       # hedonic models and robustness checks
├── outputs/            # all result tables (CSV) and model output
├── requirements.txt
└── README.md
```

## ▶️ How to run

```bash
pip install -r requirements.txt
# put the 3 register exports and g1-data.csv in data/raw/
python src/parse_raw.py
python src/clean.py
python src/describe.py
python src/scarcity.py
python src/models.py
```

## 📚 Data sources

| Data | Source | Licence |
| --- | --- | --- |
| [Credit Transactions Register](https://customer.lmbc.nsw.gov.au/application/BOAMCreditTransactionSaleRegisterExport) | NSW DCCEEW | CC BY 4.0 |
| [Credit Supply Register](https://customer.lmbc.nsw.gov.au/application/BOAMCreditSupplyRegisterExport) | NSW DCCEEW | CC BY 4.0 |
| [Credit Demand Register](https://customer.lmbc.nsw.gov.au/application/BOAMCreditDemandRegisterExport) | NSW DCCEEW | CC BY 4.0 |
| [Consumer Price Index, Table G1](https://www.rba.gov.au/statistics/tables/csv/g1-data.csv) | Reserve Bank of Australia | — |

🔒 Raw files are **not** stored in this repo because the Supply Register contains personal contact details. Personal fields are removed during cleaning.

## 🚧 Status

- [x] Data audit and cleaning pipeline
- [x] Hedonic price models with 7 robustness checks
- [x] Like-for-like scarcity index and subregion gaps
- [ ] Spatial overlay with the NSW vegetation map (ecological vs institutional shortfalls)
- [ ] Adjoining-subregion trading rules
- [ ] Preprint

## 👩‍💻 Author

**Likitha Vankadoth** · [GitHub](https://github.com/Likithaa07)
