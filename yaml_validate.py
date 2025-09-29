#!/usr/bin/env python3
import subprocess
import sys
import os
from pathlib import Path

def ensure_dependencies():
    """Install required packages if not available"""
    try:
        import yaml
    except ImportError:
        print("Installing PyYAML...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyyaml"])
        print("PyYAML installed successfully")
        import yaml

ensure_dependencies()

import yaml

def validate_yaml_files():
    """Validate all YAML files in workflows directory"""
    workflow_dir = Path('workflows/')
    yaml_files = list(workflow_dir.glob('*.yaml'))
    total_files = len(yaml_files)
    error_files = []

    print("=== YAML VALIDATION SCAN ===")
    print(f"Checking {total_files} workflow files for syntax errors...")

    for yaml_file in yaml_files:
        try:
            with open(yaml_file, 'r') as f:
                yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"ERROR in: {yaml_file}")
            print(f"  {e}")
            error_files.append(str(yaml_file))

    print(f"\nTotal YAML files: {total_files}")
    print(f"Files with errors: {len(error_files)}")
    if error_files:
        print("Files with errors identified above")
    else:
        print("All YAML files are valid!")

    return total_files, len(error_files), error_files

if __name__ == "__main__":
    validate_yaml_files()