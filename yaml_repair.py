import yaml
import os
from pathlib import Path

def fix_yaml_indentation(file_path):
    """
    Load YAML file, fix indentation, and rewrite with proper formatting
    """
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Try to parse the YAML
        try:
            data = yaml.safe_load(content)
        except yaml.YAMLError as e:
            print(f"YAML Error in {file_path}: {e}")
            
            # Common fixes for YAML issues
            # Fix 1: Inconsistent indentation (mix of tabs and spaces)
            content = content.replace('\t', '  ')
            
            # Fix 2: Incorrect list indentation
            lines = content.split('\n')
            fixed_lines = []
            for i, line in enumerate(lines):
                # If line starts with hyphen, ensure proper spacing
                if line.strip().startswith('-'):
                    # Count leading spaces
                    leading_spaces = len(line) - len(line.lstrip())
                    # Ensure hyphen has space after it
                    if not line.lstrip().startswith('- '):
                        line = ' ' * leading_spaces + '- ' + line.lstrip()[1:].lstrip()
                fixed_lines.append(line)
            
            content = '\n'.join(fixed_lines)
            
            # Try parsing again
            try:
                data = yaml.safe_load(content)
            except yaml.YAMLError as e2:
                print(f"Still cannot parse {file_path} after fixes: {e2}")
                return False
        
        # Rewrite with proper YAML formatting (2-space indentation)
        with open(file_path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False, indent=2, allow_unicode=True)
        
        print(f"FIXED: {file_path}")
        return True
        
    except Exception as e:
        print(f"ERROR fixing {file_path}: {e}")
        return False

# Process all YAML files
workflow_dir = Path('workflows/')
fixed_count = 0
error_count = 0

for yaml_file in workflow_dir.glob('*.yaml'):
    if fix_yaml_indentation(yaml_file):
        fixed_count += 1
    else:
        error_count += 1

print(f"\nYAML Repair Summary:")
print(f"Files fixed: {fixed_count}")
print(f"Files with persistent errors: {error_count}")