# What Drives Biodiversity Credit Prices?

A spatial and statistical analysis of supply–demand mismatch in the NSW Biodiversity Offsets Scheme (BOS).

## Research questions
1. Which factors (credit type, vegetation, location, scarcity, time) explain biodiversity credit prices?
2. Do scarce credit types trade at a premium?
3. Where are supply gaps most severe?

## Data
Public registers from the NSW Department of Climate Change, Energy, the Environment and Water (CC BY 4.0):
- [Credit Transactions Register](https://customer.lmbc.nsw.gov.au/application/BOAMCreditTransactionSaleRegisterExport)
- [Credit Supply Register](https://customer.lmbc.nsw.gov.au/application/BOAMCreditSupplyRegisterExport)
- [Credit Demand Register](https://customer.lmbc.nsw.gov.au/application/BOAMCreditDemandRegisterExport)
- Consumer Price Index: [RBA Table G1](https://www.rba.gov.au/statistics/tables/csv/g1-data.csv)

Raw files are not included in this repository because the Supply Register contains personal contact details. Download them into `data/raw/` to reproduce the analysis.

## Project structure
- `data/raw/` original downloads (not tracked)
- `data/interim/` converted files (not tracked)
- `data/clean/` cleaned analysis datasets
- `src/` analysis code
- `outputs/` result tables and figures
- `docs/` paper and notes

## How to run
1. Download the three registers and `g1-data.csv` into `data/raw/` (links above)
2. `pip install -r requirements.txt`
3. Run in order: `python src/parse_raw.py`, `python src/clean.py`, `python src/describe.py`, `python src/scarcity.py`, `python src/models.py`

## Key findings (registers exported 11 Oct 2026)
- **Market:** 1,284 sales worth $788M (June 2026 dollars) across 332 credit types, Nov 2019 to Oct 2026. Trade is thin: 41% of credit types sold only once.
- **Prices:** credit class, vegetation and location explain most price variation (adjusted R² 0.71). Location adds the most.
- **Scarcity is not priced:** across seven robustness checks, credit types in short supply do not sell for more.
- **Supply gaps:** 78 of 318 like-for-like credit types that developers have retired have no issued supply left, across 34 subregions.
- **Hidden shortage:** the BCT retires scarce credits less often (22% vs 37%, p = 0.03), so the public registers understate the gap.
- **Data quality:** the Demand Register is empty, Supply Register site area is 99% blank, and 328 transaction rows had garbled text.
- **Reconciliation:** 2024-25 retirements match IPART's published figures within 0.6%.

## Author
Likitha Vankadoth