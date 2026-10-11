What Drives Biodiversity Credit Prices? A Spatial and Statistical Analysis of Supply–Demand Mismatch in the NSW Biodiversity Offsets Scheme
Research progress report · 11 Oct 2026 · @likitha
Introduction
What the project is about. This project explains what sets the price of biodiversity credits in the NSW Biodiversity Offsets Scheme (BOS). Developers who clear native vegetation must retire credits. Landholders create credits by protecting and managing land under Biodiversity Stewardship Agreements. Every sale, retirement and credit listing is recorded in three public registers published by the NSW Department of Climate Change, Energy, the Environment and Water (DCCEEW): Transactions, Supply and Demand.
Why it matters. The scheme is now a market of about $788 million in real (inflation-adjusted) terms across 1,284 sales. It is also under active reform, with the Biodiversity Conservation Amendment Act commencing on 7 March 2025. Independent reviews by the NSW Audit Office (2023) and IPART (2026) raise concerns about thin trading, unclear prices and credit shortfalls. If prices do not respond to scarcity, the market cannot send a signal to landholders to supply the credits that are most needed. That weakens the scheme's goal of no net loss of biodiversity.
Research questions.
1. RQ1: Which credit attributes (credit class, vegetation formation, location, lot size, bundling, buyer type) explain the price of biodiversity credits in NSW?
2. RQ2: Do credit prices respond to scarcity, measured as recent demand relative to the supply still available for the same like-for-like credit?
3. RQ3: Where are the largest supply–demand gaps, and what do they mean for policy and for the quality of the public register data?
What I expect to achieve.
• An open, reproducible and audited data pipeline for the three BOS registers, published on GitHub (github.com/Likithaa07/bos-credit-prices).
• Hedonic price models that measure how much each credit attribute contributes to price, tested with robustness checks.
• A like-for-like scarcity index that maps where supply cannot meet demand, by credit type and IBRA subregion.
• Evidence-based recommendations for market design and data governance, written up as a working paper and later as a preprint.
How it will be done. The three public registers are cleaned and checked, then linked into one dataset. That dataset feeds three analyses, one for each research question: a price model, a scarcity index and a map of supply gaps.
Progress so far. The data pipeline, the price models and the scarcity index are complete. The clearest finding so far is that credit prices do not rise when credits become scarce. Location and the type of vegetation explain most of the price. Meanwhile 78 like-for-like credit units have no supply left, and 34 regions have a shortfall. In other words, the market is not sending the price signal that would encourage landholders to supply the credits most needed.
Reflections. The biggest surprise was the state of the public data. The Demand Register was empty, 98.8% of supply records had no site area, and names were spelled differently across registers. Cleaning and checking the data took more effort than planned. It also became a finding in its own right, and it shaped how demand is measured (from retirements instead of the empty Demand Register). The mapping stage is still to come and is the main focus for the remaining months.
Literature Review
Recent research shows that biodiversity offsets often fail to deliver no net loss and that offset markets are hard to see into. However, no study has modelled credit prices at transaction level in an Australian offset scheme. The literature falls into four strands.
1. Do offsets deliver ecological outcomes? Evidence from Australia since 2023 is mostly critical. zu Ermgassen et al. (2023) evaluated Victoria's native vegetation offsets and found little additional gain from offsets based on avoided loss. O'Brien and Gordon (2024) found that averted-loss gains in Victorian offset exchanges were overestimated by 3 to 240 times. For the current NSW scheme, Gordon et al. (2025) analysed 1,395 development and offset assessments from 2017 to 2023. Development sites were smaller and in poorer condition than offset sites, and active restoration made up less than a fifth of offset area. Relevance: if credits are cheap to create and over-credited, a low price may reflect generous crediting rather than low ecological value. Price models therefore need ecological variables, not only location and time.
2. How should offset markets be designed? Tradable-permit theory predicts a trade-off. Strict rules on type, place and time improve ecological equivalence but split demand into many small, thin markets (Wissel & Wätzold, 2010, foundational). England's Biodiversity Net Gain market, launched in 2024, offers a recent contrast. Its government sells statutory credits priced above the market as a last resort (UK Government, 2024), and only about 2% of listed off-site land had sold by May 2025 (Duffus et al., 2025). NSW does the opposite: the Biodiversity Conservation Fund (BCF) lets developers pay instead of buying credits, and IPART (2026) reports that this has absorbed much of the demand. Relevance: the payment option may put a ceiling on prices and weaken the scarcity signal.
3. What drives offset credit prices? Empirical price studies are rare and come mostly from US wetland and species banking (Vaissière & Levrel, 2015, foundational). Those studies link prices to land values, location and local competition. In NSW, prices have been described only in aggregate, through market monitoring reports (IPART, 2026) and a pricing guide (NSW DCCEEW, 2024). Neither tests which attributes explain price, or whether scarcity is priced.
4. Are the public registers fit for purpose? Kujala et al. (2022) showed that credible offsetting needs public registers that let outsiders confirm no net loss, and that most existing registers fail on access and transparency. The NSW Legislative Council (2022), the Audit Office of NSW (2023) and IPART (2026) all found NSW market data inadequate for participants and regulators. Relevance: a documented audit of register data quality is a contribution in its own right.
Research gap. The NSW scheme has been studied ecologically (strand 1) and reviewed administratively (strand 4), and offset prices have been modelled overseas (strand 3). What is missing is a reproducible, transaction-level analysis of how prices form in a strict like-for-like market where a state fund acts as the outside option, linked to where supply has run out. This project fills that gap.
Strand
Key recent works
What they found
What is still missing
Ecological outcomes
zu Ermgassen et al. (2023); O'Brien & Gordon (2024); Gordon et al. (2025)
Offsets over-credit averted loss; little restoration
Whether prices reflect ecological value
Market design
Duffus et al. (2025); IPART (2026)
Thin trade; government-priced alternatives shape demand
Evidence on the NSW fund's effect on prices
Price drivers
Vaissière & Levrel (2015); NSW DCCEEW (2024)
US prices follow land value and location
No transaction-level price model in Australia
Register data
Kujala et al. (2022); Audit Office of NSW (2023)
Registers lack transparency and key fields
No published audit of NSW register data quality
Research Methodology
All three research questions are answered from one audited dataset. It is built in open Python code from public registers, so every result can be rebuilt as the registers update.
Preliminary framework
Raw registers pass through one audited pipeline into a single linked dataset. Each research question is then answered by its own analysis.
Step 1: Data
• BOS Credit Transactions Register (NSW DCCEEW, 2026; CC BY 4.0): 2,591 records of sales, retirements and cancellations from November 2019 to October 2026. This gives the dependent variable, price per credit.
• BOS Credit Supply Register: 2,852 records of credits issued and available for sale.
• BOS Credit Demand Register: no listings at the 11 October 2026 export, so demand is measured from retirements.
• RBA Table G1 consumer price index (Reserve Bank of Australia, 2026) (quarterly, all groups), used to convert prices to June quarter 2026 dollars.
• IBRA 7.1 subregion boundaries, used for mapping supply gaps.
Step 2: Data audit and cleaning
The registers are kept for administration, not analysis, so they were audited for completeness, validity, uniqueness, consistency and reconciliation. Every exclusion is logged in an audit table.
1. Parse: the downloaded “.xls” files turned out to be an HTML table and SpreadsheetML XML. Each is parsed to a tidy table.
2. Repair: garbled text encoding is repaired in 328 rows. Trading group names are normalised (lower case, punctuation removed) so the registers can be joined; this matches 96% of names.
3. Protect privacy: personal name fields are removed before any data is saved.
4. Filter: only market sales are kept (1,295 transfers), then transfers at $1 or less and philanthropic transfers are excluded, leaving 1,284 priced sales.
5. Flag, not drop: 223 sales to the Biodiversity Conservation Trust (BCT), found by tracing credits to later BCT retirements; 278 bundled sales priced at one average; and 6 prices between $1 and $100.
6. Deflate: nominal prices are converted to real June quarter 2026 dollars with the CPI.
7. Reconcile: 2024-25 retirements are checked against IPART (2026) and agree within 0.6% (114,164 vs 114,856).
Step 3: Price model (RQ1)
A hedonic regression estimates how much each credit attribute adds to price:
\ln P_{i} = \alpha + \beta\,\text{Class}_{i} + \gamma_{F(i)} + \mu_{r(i)} + \tau_{t(i)} + \delta \ln D_{i} + \boldsymbol{\theta}'\mathbf{Z}_{i} + \varepsilon_{i}
P is the real price per credit for sale i. The model includes credit class (ecosystem or species), vegetation formation F, IBRA subregion r and financial year t. D is demand pressure, the credits of the same like-for-like unit retired in the 36 months before the sale. Z holds lot size, a BCT buyer flag and a bundle flag. Standard errors are clustered by seller credit record.
The model is built up in five steps (M1 to M5) so each factor's contribution is visible. M5 adds a post-reform indicator for sales on or after 7 March 2025. Results are tested with seven robustness checks: excluding prices under $100, excluding bundles, excluding BCT sales, weighting by credits sold, median (quantile) regression, and swapping in the static scarcity index.
Step 4: Scarcity index (RQ2)
Credits are grouped into like-for-like units that follow the scheme's trading rules in simplified form. Species credits are matched by species anywhere in NSW. Ecosystem credits are matched by offset trading group within the same IBRA subregion. For each unit u:
SI_{u} = \ln\left(\frac{R_{u} + 1}{S_{u} + 1}\right)
R is credits retired in the 36 months to the export date, and S is issued supply on the register. A value above 0 means recent use exceeds what is left. The index is related to price with a Spearman rank correlation, and to BCT activity with a Mann–Whitney test.
Step 5: Supply gap mapping (RQ3)
Unmet demand (retirements minus supply) is added up by IBRA subregion and mapped. Planned next steps are to:
• apply the adjoining-subregion trading rules
• overlay remaining native vegetation from the NSW State Vegetation Type Map
This separates ecological shortfalls, where the vegetation is largely cleared, from institutional shortfalls, where vegetation remains but no stewardship sites have formed.
Tools and reproducibility
The tools are Python (pandas, NumPy, statsmodels, SciPy, ftfy, lxml), version control with Git and GitHub through VS Code, and a pinned requirements file. Each stage is a separate script that reads the previous stage's output: parse_raw.py, clean.py, describe.py, scarcity.py and models.py. Raw data is kept read-only and out of version control. Code: github.com/Likithaa07/bos-credit-prices.
Status and timeline
Stage
Status
Target
Research design, literature review, data audit
Done
October 2026
Price models, robustness checks, scarcity index
Done
October 2026
Spatial gap mapping, adjoining-subregion rules
In progress
November 2026
Preprint (OSF or EarthArXiv)
Planned
December 2026
Journal submission (e.g. Ecological Economics)
Planned
Early 2027
Fallback strategies
Each sub-problem produces a usable result on its own, so the project still succeeds if a later stage slips. The price model (RQ1) and scarcity index (RQ2) are already complete, so the core contribution is secure.
Risk
Fallback
What is still delivered
Demand Register stays empty
Measure demand from credit retirements (already in use)
Scarcity index based on demand that was met, with the bias stated
BCF charges by credit type stay unpublished
Request them from DCCEEW or the BCT; otherwise leave the censored model as future work
Main price models and robustness checks
Vegetation map overlay too large or slow to process
Use IBRA subregion totals only; run the overlay on a sample of subregions
Subregion gap map without the ecological/institutional split
Adjoining-subregion rules too complex to code in time
Keep the simplified same-subregion rule and report it as a conservative lower bound
Scarcity index with a stated limitation
Registers updated or changed format
The pipeline reruns from raw files; parsers detect the header row automatically
Results refreshed from the latest export
Researcher unavailable for a period
All code, data steps and decisions are documented on GitHub and in an audit log, so work can resume or be handed over
Full reproducibility from the repository
Research Progress – Results, Analysis, and Discussion
Four of the five planned steps are complete. The central result is that prices reflect location and vegetation type, not scarcity, even though supply has run out for many credits. All results use the registers exported on 11 October 2026 and real June quarter 2026 dollars.
Status by sub-problem
Sub-problem
Status
Main result
Data audit and cleaning
Complete
1,284 priced sales; retirements match IPART within 0.6%
RQ1 Price drivers
Complete
Class, vegetation and location explain 71% of price variation
RQ2 Scarcity pricing
Complete
No robust scarcity premium across 7 checks
RQ3 Supply gaps (subregion level)
Complete
78 units with no supply; shortfalls in 34 subregions
RQ3 Ecological vs institutional split
Outstanding
Needs the vegetation map overlay
BCF price ceiling (censored model)
Deferred
BCF charges are not public
Result 1: The data needed substantial repair
The registers were not analysis-ready. The audit found that:
• the “spreadsheets” were really HTML and XML files
• 328 rows had garbled text
• the Demand Register held no listings
• site area was blank for 98.8% of supply records
• one in five sales was part of a bundle priced at a single average
• buyers are not identified, so 223 purchases by the BCT could only be found by tracing credits to later retirements
The cleaned data reconciles well with official figures:
2024-25
This study
IPART (2026)
Difference
Credits retired
114,164
114,856
−0.6%
Credits sold
93,550
about 82,000
+14%
Value of sales
$193m nominal
about $170m
+13%
Retirements match closely. Sales differ because IPART combines BOS credits with older BioBanking credits and defines a sale differently. This points to a reporting recommendation: one published definition of a market sale.
Result 2: What explains prices (RQ1)
The market recorded 1,284 sales worth $788 million from November 2019 to October 2026, across 332 credit types. Trade is thin: 41% of credit types sold only once, and the top ten types hold 52% of value. The median price was $4,268 per ecosystem credit and $813 per species credit.
Model
Adds
Adjusted R²
M1
Credit class and financial year
0.36
M2
Vegetation formation
0.45
M3
IBRA subregion
0.71
M4
Demand pressure, lot size, BCT buyer, bundle
0.72
• Location matters most. Adding subregion lifts explained variation from 45% to 71%. Cumberland (western Sydney) has a median above $31,000 per credit, about eight times the state median, which suggests land values set the cost of supply.
• Bulk buys are cheaper. A tenfold larger purchase is about 9% cheaper per credit (p = 0.002), and bundled sales are about 25% cheaper (p < 0.001).
• No real price trend and no reform effect. In real terms prices rose about 4% a year (p = 0.23), and there was no significant change after the March 2025 reform (−8%, p = 0.21). The apparent nominal rise was mostly inflation.
Result 3: Scarcity is not priced (RQ2)
Specification
Effect of demand pressure
p
Main model (M4)
−0.017
0.10
Excluding prices below $100
−0.022
0.02
Excluding bundled sales
−0.009
0.43
Excluding sales to the BCT
−0.025
0.02
Weighted by credits sold
+0.045
0.04
Median (quantile) regression
−0.009
0.05
Static scarcity index instead
+0.009
0.40
The effects are small and change sign, so there is no robust scarcity premium. At credit-type level, the rank correlation between scarcity and median price is only 0.12 (p = 0.06). Two explanations fit. The Biodiversity Conservation Fund gives buyers a way out when credits are scarce, which caps what they will pay. And sellers appear to price from their costs (land and management), not from scarcity.
Result 4: Where supply has run out (RQ3)
• Of 309 credit types retired since 2019, 50 have no supply left.
• At like-for-like level, 78 of 318 units have no supply, and in 130 units credits retired in the last three years exceed all remaining supply.
• Shortfalls are almost all ecosystem credits (118 of 130), because these can only be traded locally.
• 34 IBRA subregions have a shortfall. The largest are Murrumbidgee, Lower Slopes, Hill End, Northern Outwash and Kerrabee.
• The registers understate the shortage. Units with no supply are less likely to show BCT retirements (22% vs 37%, Mann–Whitney p = 0.03). The BCT can only retire credits it manages to buy, so the scarcest obligations never appear as retirements.
Changes to the original plan
Original plan (P)
What happened
Revised approach (P′)
Measure demand from the Demand Register
Register was empty
Demand measured from retirements in the previous 36 months; bias tested and reported (Result 4)
Track supply over time
Issue dates missing for 55% of supply records
Static supply snapshot at the export date
Model prices in nominal dollars
Nominal trend was mostly inflation
All prices converted to real dollars using RBA CPI
Full like-for-like trading rules
Rules too complex for the first pass
Simplified same-subregion rule; full rules planned
Censored model with BCF charges as a ceiling
Charges not published by credit type
Deferred; RQ2 reframed as whether scarcity is priced at all
The main lesson is that, in this market, data quality is part of the research problem and not only a preparation step. The audit findings are now a stand-alone contribution.
Individual Contributions
This is an individual project. Likitha Vankadoth is the sole researcher and is responsible for all stages:
Area
Contribution
Research design
Defined the research questions, scope and framework; reviewed recent literature and identified the research gap
Data acquisition
Sourced the three NSW BOS public registers, RBA CPI and IBRA boundaries; documented licences and attribution
Data engineering
Built the Python pipeline: parsed the HTML and XML exports, repaired encoding, normalised join keys, removed personal data, logged every exclusion
Data quality
Audited completeness, validity and consistency; reconciled totals against IPART (2026)
Analysis
Estimated the hedonic price models and robustness checks; built the like-for-like scarcity index and statistical tests
Version control
Set up and maintained the GitHub repository through VS Code, with staged commits for each stage of the pipeline
Writing
Drafted this proposal and the working paper, including policy and data governance recommendations
AI tools were used for coding support and drafting. All code was run, checked and committed by the author, and all results come from the author's own pipeline.
Planned contributions for the remaining stages. As sole researcher, Likitha Vankadoth will be responsible for:
Stage
Responsibility
Target
Spatial analysis
Overlay vegetation extent on supply gaps; code the adjoining-subregion rules; test clustering with Moran's I
November 2026
Further modelling
Multilevel and gradient-boosted (SHAP) models; censored model if BCF charges are obtained
November 2026
Stakeholder data requests
Request BCF charges and unmet obligations by credit type from DCCEEW and the BCT
November 2026
Reporting
Interactive dashboard and a plain-language policy brief
December 2026
Publication
Preprint (December 2026), then journal submission and responses to peer review
Early 2027
Maintenance
Rerun the pipeline on each new register export and keep the repository documented
Ongoing
Future Outlook
The next stage turns a price study into a tool regulators can use. It would track supply gaps over time and show where offsetting can and cannot deliver like-for-like outcomes.
Research extensions
1. Spatial typology. Overlay remaining vegetation from the NSW State Vegetation Type Map to separate ecological shortfalls (vegetation largely cleared) from institutional ones (vegetation remains but no stewardship sites). Test spatial clustering with Moran's I.
2. Full trading rules. Add the adjoining-subregion and 100 km like-for-like rules, so the scarcity index matches how credits can legally be traded.
3. Fund price ceiling. If BCF charges by credit type become available, estimate a censored (Tobit) model to test whether the payment option caps market prices.
4. Stronger models. Add a multilevel model with random effects for credit types, and a gradient-boosted model with SHAP values to check for non-linear effects.
5. Reform tracking. Use the October 2026 results as a baseline to measure how the 2025 Amendment Act and the 2026 Regulation change prices and supply.
6. Longer history. Link pre-2018 BioBanking registers to extend the price series back in time.
Expected impact
• For DCCEEW and the BCT: a scarcity index that updates with each register export. It could flag credit types and subregions where obligations are at risk of never being offset like-for-like, and show where supply funding or tenders would help most.
• For data governance: concrete fixes for the public registers, such as recording buyer type, flagging bundled and related-party sales at entry, completing site area and issue dates, and using one agreed definition of a market sale.
• For the market: clearer price signals for landholders deciding whether to set up stewardship sites.
• For research: an open, reproducible pipeline that other researchers and agencies can rerun and extend to other offset schemes, such as Victoria's or England's Biodiversity Net Gain.
Publication path. A preprint on OSF or EarthArXiv (December 2026), then submission to a peer-reviewed journal such as Ecological Economics or Conservation Science and Practice (early 2027), with a plain-language policy brief and an interactive dashboard alongside.
Challenges and most promising solutions
Challenge
Why it matters
Recommended solution
True demand is hidden
Obligations paid into the BCF but never matched with credits do not appear in any register
Request unmet obligations by credit type from the BCT; meanwhile report scarcity as a lower bound
The fund may cap prices
Without BCF charges, the ceiling effect cannot be measured directly
Obtain charges through a data request and estimate a censored (Tobit) model
Thin markets
41% of credit types sold only once, so type-level estimates are noisy
Multilevel models that borrow strength across similar credit types
Large spatial data
The 5 m vegetation map is heavy to process
Zonal statistics by subregion using cloud or tiled processing, starting with high-shortfall subregions
Changing rules and data
The 2025 reforms and register updates may change definitions
Keep the pipeline versioned and rerunnable, and treat October 2026 as a baseline for tracking reform effects
Bibliography
References use APA 7th edition. Most are from 2022 to 2026. Two older works, Wissel and Wätzold (2010) and Vaissière and Levrel (2015), are kept as the foundational theory of offset markets.
Audit Office of New South Wales. (2023). Effectiveness of the Biodiversity Offsets Scheme [Performance audit report]. Audit Office of NSW.
Duffus, N., zu Ermgassen, S., Lewis, O., & Grenyer, R. (2025). Early outcomes of England's new biodiversity offset market [Preprint]. bioRxiv. https://doi.org/10.1101/2025.06.22.660961
Gordon, A., Curtsdotter, A., Oliver, I., Hernandez, S., Cox, M., & Dorrough, J. (2025). Five years of offsetting native vegetation: The challenge of achieving no-net-loss. Ecological Indicators, 179, Article 114180. https://doi.org/10.1016/j.ecolind.2025.114180
Independent Pricing and Regulatory Tribunal of NSW. (2026). Biodiversity credits market monitoring: Annual report 2024-25. IPART.
Kujala, H., Maron, M., Kennedy, C. M., Evans, M. C., Bull, J. W., Wintle, B. A., et al. (2022). Credible biodiversity offsetting needs public national registers to confirm no net loss. One Earth, 5(6), 650–662.
NSW Department of Climate Change, Energy, the Environment and Water. (2024). Biodiversity credit pricing guide. NSW Government.
NSW Department of Climate Change, Energy, the Environment and Water. (2026). Biodiversity Offsets Scheme public registers: Credit transactions, credit supply and credit demand [Data sets, exported 11 October 2026]. NSW Government. Licensed under CC BY 4.0.
NSW Legislative Council. (2022). Integrity of the NSW Biodiversity Offsets Scheme (Report No. 16). Parliament of New South Wales.
O'Brien, A., & Gordon, A. (2024). Evaluation of averted loss gains under Victorian biodiversity offset policy. Conservation Science and Practice, 6(2).
Reserve Bank of Australia. (2026). Consumer price inflation – G1 [Data set]. RBA.
UK Government. (2024). Statutory biodiversity credit prices. GOV.UK.
Vaissière, A.-C., & Levrel, H. (2015). Biodiversity offset markets: What are they really? An empirical approach to wetland mitigation banking. Ecological Economics, 110, 81–88.
Wissel, S., & Wätzold, F. (2010). A conceptual analysis of the application of tradable permits to biodiversity conservation. Conservation Biology, 24(2), 404–411.
zu Ermgassen, S. O. S. E., Devenish, K., Simmons, B. A., Gordon, A., Jones, J. P. G., Maron, M., et al. (2023). Evaluating the impact of biodiversity offsetting on native vegetation. Global Change Biology, 29(15), 4397–4411.
