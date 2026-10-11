"""
Step 1: Convert the raw BOS register downloads into CSV tables.

The 'xls' files from the NSW registers are not real Excel files:
- the Transactions Register is an HTML web page containing a table
- the Supply and Demand Registers are XML spreadsheets (SpreadsheetML)

Input : data/raw/*.xls
Output: data/interim/transactions.csv, supply.csv, demand.csv
"""
import re
import xml.etree.ElementTree as ET
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
INTERIM = ROOT / "data" / "interim"
INTERIM.mkdir(parents=True, exist_ok=True)

NS = "{urn:schemas-microsoft-com:office:spreadsheet}"


def read_html_register(path):
    """Read the HTML export and return its largest table."""
    tables = pd.read_html(path)
    return max(tables, key=len)


def read_xml_register(path):
    """Read a SpreadsheetML export into a DataFrame."""
    text = Path(path).read_text(encoding="utf-8", errors="replace")
    # Some names contain a bare '&' (e.g. 'Smith & Co'), which breaks XML parsing
    text = re.sub(r"&(?!(amp|lt|gt|quot|apos|#\d+|#x[0-9a-fA-F]+);)", "&amp;", text)
    sheet = ET.fromstring(text).find(f"{NS}Worksheet")

    rows = []
    for row in sheet.iter(f"{NS}Row"):
        values, col = [], 0
        for cell in row.findall(f"{NS}Cell"):
            index = cell.get(f"{NS}Index")          # skipped empty cells
            if index:
                while col < int(index) - 1:
                    values.append(None)
                    col += 1
            data = cell.find(f"{NS}Data")
            values.append("".join(data.itertext()) if data is not None else None)
            col += 1
        rows.append(values)

    # The first rows are disclaimers; the header is the first row with 4+ filled cells
    width = max(len(r) for r in rows)
    rows = [r + [None] * (width - len(r)) for r in rows]
    for i, r in enumerate(rows):
        if sum(v is not None and str(v).strip() != "" for v in r) >= 4:
            header = [str(v).strip() for v in r]
            return pd.DataFrame(rows[i + 1:], columns=header)
    raise ValueError(f"No header row found in {path}")


if __name__ == "__main__":
    files = {
        "transactions": (read_html_register, "BOAMCreditTransactionSaleExport.xls"),
        "supply": (read_xml_register, "BOSCreditSupplyRegisterExport.xls"),
        "demand": (read_xml_register, "BOSCreditDemandRegisterExport.xls"),
    }
    for name, (reader, filename) in files.items():
        df = reader(RAW / filename)
        df.to_csv(INTERIM / f"{name}.csv", index=False)
        print(f"{name:13s} {len(df):6,d} rows  {df.shape[1]:3d} columns")