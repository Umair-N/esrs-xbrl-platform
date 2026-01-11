"""
Extract BRSR taxonomy tags from Excel file and convert to JSON.
Run this script once to generate the taxonomy JSON file.

Usage:
    python scripts/extract-brsr-taxonomy.py
"""

import pandas as pd
import json
from pathlib import Path

# Input Excel file path
EXCEL_FILE = Path("Taxonomy_BRSR_31-05-2025.xlsx")
SHEET_NAME = "Element"
ID_COLUMN = "id"

# Output JSON file path
OUTPUT_JSON = Path("lib/brsr-taxonomy.json")

def extract_taxonomy():
    """Extract BRSR taxonomy tags from Excel."""

    if not EXCEL_FILE.exists():
        print(f"Error: Excel file not found: {EXCEL_FILE}")
        print("Please place the Excel file in the project root directory.")
        return

    print(f"Reading Excel file: {EXCEL_FILE}")

    # Read the Excel file
    df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)

    # Extract the Id column (tag names)
    if ID_COLUMN not in df.columns:
        print(f"Error: Column '{ID_COLUMN}' not found in sheet '{SHEET_NAME}'")
        print(f"Available columns: {', '.join(df.columns)}")
        return

    # Get unique tags and sort them
    tags = df[ID_COLUMN].dropna().unique().tolist()
    tags = sorted([str(tag).strip() for tag in tags if str(tag).strip()])

    print(f"Found {len(tags)} unique tags")

    # Create taxonomy data structure
    taxonomy_data = {
        "version": "2025-05-31",
        "source": "Taxonomy_BRSR_31-05-2025.xlsx",
        "total_tags": len(tags),
        "tags": tags,
        "tag_metadata": {}
    }

    # Extract additional metadata if available
    metadata_columns = [col for col in df.columns if col != ID_COLUMN]

    if metadata_columns:
        print(f"Extracting metadata from columns: {', '.join(metadata_columns)}")

        for _, row in df.iterrows():
            tag_id = str(row[ID_COLUMN]).strip()
            if not tag_id or pd.isna(row[ID_COLUMN]):
                continue

            metadata = {}
            for col in metadata_columns:
                value = row[col]
                if pd.notna(value):
                    metadata[col] = str(value)

            if metadata:
                taxonomy_data["tag_metadata"][tag_id] = metadata

    # Create output directory if it doesn't exist
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)

    # Write to JSON file
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(taxonomy_data, f, indent=2, ensure_ascii=False)

    print(f"\nTaxonomy data extracted successfully!")
    print(f"Output file: {OUTPUT_JSON}")
    print(f"Total tags: {len(tags)}")

    # Show sample tags
    print(f"\nSample tags (first 10):")
    for tag in tags[:10]:
        print(f"  - {tag}")

if __name__ == "__main__":
    extract_taxonomy()
