"""Verify that all Excel tags are in the JSON file."""

import pandas as pd
import json
from pathlib import Path

EXCEL_FILE = Path("Taxonomy_BRSR_31-05-2025.xlsx")
JSON_FILE = Path("lib/brsr-taxonomy.json")

# Read Excel tags
excel_df = pd.read_excel(EXCEL_FILE, sheet_name='Element')
excel_tags = set(excel_df['id'].dropna().astype(str).str.strip())

# Read JSON tags
with open(JSON_FILE) as f:
    json_data = json.load(f)
json_tags = set(json_data['tags'])

# Compare
missing_in_json = excel_tags - json_tags
missing_in_excel = json_tags - excel_tags

print(f"Excel tags: {len(excel_tags)}")
print(f"JSON tags: {len(json_tags)}")
print(f"\nTags in Excel but not in JSON: {len(missing_in_json)}")
print(f"Tags in JSON but not in Excel: {len(missing_in_excel)}")

if missing_in_json:
    print(f"\nMissing tags (first 20):")
    for tag in list(missing_in_json)[:20]:
        print(f"  - {tag}")
else:
    print("\nAll Excel tags are present in JSON!")
