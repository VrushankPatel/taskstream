#!/usr/bin/env python3
import json
from pathlib import Path

def validate_json_files():
    """Validate all JSON files in decisions directory"""
    decisions_dir = Path('decisions/')
    json_files = list(decisions_dir.glob('*.json'))
    total_files = len(json_files)
    error_files = []

    print("=== JSON VALIDATION SCAN ===")
    print(f"Checking {total_files} decision files for syntax errors...")

    for json_file in json_files:
        try:
            with open(json_file, 'r') as f:
                json.load(f)
        except json.JSONDecodeError as e:
            print(f"ERROR in: {json_file}")
            print(f"  {e}")
            error_files.append(str(json_file))

    print(f"\nTotal JSON files: {total_files}")
    print(f"Files with errors: {len(error_files)}")
    if error_files:
        print("Files with errors identified above")
    else:
        print("All JSON files are valid!")

    return total_files, len(error_files), error_files

if __name__ == "__main__":
    validate_json_files()