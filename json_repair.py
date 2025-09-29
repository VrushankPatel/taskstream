import json
import os
from pathlib import Path

def fix_json_formatting(file_path):
    """
    Load JSON file, fix formatting issues, and rewrite with proper indentation
    """
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Try to parse JSON
        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            print(f"JSON Error in {file_path}: {e}")
            
            # Common fixes for JSON issues
            # Fix 1: Trailing commas
            content = content.replace(',]', ']').replace(',}', '}')
            
            # Fix 2: Single quotes instead of double quotes
            # (This is risky, only do for simple cases)
            
            # Try parsing again
            try:
                data = json.loads(content)
            except json.JSONDecodeError as e2:
                print(f"Still cannot parse {file_path} after fixes: {e2}")
                return False
        
        # Rewrite with proper JSON formatting (2-space indentation)
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"FIXED: {file_path}")
        return True
        
    except Exception as e:
        print(f"ERROR fixing {file_path}: {e}")
        return False

# Process all JSON files
decisions_dir = Path('decisions/')
fixed_count = 0
error_count = 0

for json_file in decisions_dir.glob('*.json'):
    if fix_json_formatting(json_file):
        fixed_count += 1
    else:
        error_count += 1

print(f"\nJSON Repair Summary:")
print(f"Files fixed: {fixed_count}")
print(f"Files with persistent errors: {error_count}")