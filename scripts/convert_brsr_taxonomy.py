"""
Convert BRSR taxonomy Excel file to JSON format.
This creates a searchable JSON file with tag definitions and references.
"""
import pandas as pd
import json
from pathlib import Path

def convert_brsr_taxonomy_to_json():
    """Convert brsr_taxonomy (1).xlsx to JSON format."""

    # Read Excel file
    excel_path = Path(__file__).parent.parent / "brsr_taxonomy (1).xlsx"
    df = pd.read_excel(excel_path)

    print(f"Reading {excel_path}")
    print(f"Total rows: {len(df)}")
    print(f"Columns: {df.columns.tolist()}")

    # Create taxonomy dictionary
    taxonomy = {}

    for _, row in df.iterrows():
        tag = row['Tag']

        # Skip rows with empty tags
        if pd.isna(tag) or not tag:
            continue

        tag = str(tag).strip()
        reference = str(row['Reference']).strip() if pd.notna(row['Reference']) else ""
        tag_type = str(row['Type']).strip() if 'Type' in df.columns and pd.notna(row['Type']) else ""

        # Extract short name from tag (e.g., "in-capmkt_ABriefOnTypes..." -> "ABriefOnTypes...")
        short_name = tag.split('_', 1)[1] if '_' in tag else tag

        taxonomy[tag] = {
            "tag": tag,
            "reference": reference,
            "type": tag_type,
            "shortName": short_name,
            "searchText": f"{tag} {reference} {short_name}".lower()  # For faster searching
        }

    # Save to JSON
    output_path = Path(__file__).parent.parent / "lib" / "brsr_taxonomy.json"
    output_path.parent.mkdir(exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(taxonomy, f, indent=2, ensure_ascii=False)

    print(f"\nSuccessfully converted {len(taxonomy)} tags to {output_path}")
    print(f"File size: {output_path.stat().st_size / 1024:.2f} KB")

    # Print sample entries
    print("\nSample entries:")
    for i, (tag, data) in enumerate(list(taxonomy.items())[:3]):
        print(f"\n{i+1}. Tag: {tag}")
        print(f"   Reference: {data['reference'][:80]}...")
        print(f"   Type: {data['type']}")

if __name__ == "__main__":
    convert_brsr_taxonomy_to_json()
