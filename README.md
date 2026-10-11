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

## Author
Likitha Vankadoth