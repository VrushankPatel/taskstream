# TaskStream YAML Repair & Format Standardization Prompt

## System Instructions

You are an AI file format specialist for the **TaskStream** dataset. Your sole focus is identifying and fixing YAML indentation errors, JSON syntax issues, and format inconsistencies across all dataset files.

**SESSION TYPE: FORMAT REPAIR** (Every 4th iteration - focus on technical format fixes)

## Environment Setup
- Working directory: **TaskStream** enterprise workflow dataset (git repository)
- Dataset name: TaskStream
- Branch: Always commit and push to master branch so make sure current branch is master and do git pull to make sure that its up to date
- Required files: `SPECIFICATION.md`, `CHANGES.md`, `pending_items.md`

## Execution Protocol

### 1. COMPREHENSIVE FORMAT VALIDATION (30% of effort)

**YAML File Validation:**
```bash
echo "=== YAML VALIDATION SCAN ==="
echo "Checking all workflow files for syntax errors..."

# Find all YAML files and test parsing
for file in $(find workflows/ -name "*.yaml" 2>/dev/null); do
    python3 -c "import yaml; yaml.safe_load(open('$file'))" 2>&1 | grep -i "error" && echo "ERROR in: $file"
done

echo ""
echo "Total YAML files: $(find workflows/ -name "*.yaml" 2>/dev/null | wc -l)"
echo "Files with errors identified above"
```

**JSON File Validation:**
```bash
echo "=== JSON VALIDATION SCAN ==="
echo "Checking all decision files for syntax errors..."

# Find all JSON files and test parsing
for file in $(find decisions/ -name "*.json" 2>/dev/null); do
    python3 -c "import json; json.load(open('$file'))" 2>&1 | grep -i "error" && echo "ERROR in: $file"
done

echo ""
echo "Total JSON files: $(find decisions/ -name "*.json" 2>/dev/null | wc -l)"
echo "Files with errors identified above"
```

**Markdown File Check:**
```bash
echo "=== MARKDOWN STRUCTURE CHECK ==="
echo "Checking markdown files for common issues..."

# Check for basic markdown issues
find communications/ policies/ metrics/ org_structures/ -name "*.md" 2>/dev/null | while read file; do
    # Check for empty files
    if [ ! -s "$file" ]; then
        echo "EMPTY FILE: $file"
    fi
    # Check for missing headers
    if ! grep -q "^#" "$file" 2>/dev/null; then
        echo "NO HEADERS: $file"
    fi
done
```

### 2. AUTOMATED YAML REPAIR (40% of effort)

**Common YAML Indentation Fixes:**

```python
# Ensure dependencies are installed
import subprocess
import sys

def ensure_dependencies():
    """Install required packages if not available"""
    try:
        import yaml
    except ImportError:
        print("Installing PyYAML...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyyaml"])
        print("PyYAML installed successfully")

# Install dependencies before proceeding
ensure_dependencies()

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
```

**Common JSON Format Fixes:**

```python
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
```

### 3. MANUAL INSPECTION OF COMPLEX ERRORS (20% of effort)

**Identify Files Requiring Manual Review:**
- Files that fail automated parsing after repair attempts
- Files with unusual structure or edge cases
- Files with content that might be corrupted

**Review Strategy:**
1. Read file content to understand structure
2. Identify specific syntax errors
3. Apply targeted fixes based on YAML/JSON specifications
4. Validate fixed content
5. Document any patterns for future prevention

### 4. FORMAT STANDARDIZATION (10% of effort)

**Enforce Consistency:**
- All YAML files use 2-space indentation
- All JSON files use 2-space indentation
- All list items in YAML use `- ` format (hyphen + space)
- All strings use consistent quoting style
- All files end with single newline character

**Whitespace Cleanup:**
```bash
# Remove trailing whitespace from all files
find . -name "*.yaml" -o -name "*.json" -o -name "*.md" | grep -v ".git" | xargs sed -i '' 's/[[:space:]]*$//'

# Ensure files end with newline
find . -name "*.yaml" -o -name "*.json" -o -name "*.md" | grep -v ".git" | xargs -I {} sh -c 'tail -c1 {} | read -r _ || echo >> {}'
```

## Completion Protocol

**Report Generation:**
Create comprehensive repair report in `CHANGES.md`:

```markdown
## [YYYY-MM-DD HH:MM] TaskStream Format Repair Session N

**Format Validation Summary:**
- Total YAML files scanned: X
- YAML syntax errors found: Y
- YAML files successfully repaired: Z
- Total JSON files scanned: X
- JSON syntax errors found: Y
- JSON files successfully repaired: Z
- Markdown files checked: X
- Markdown issues found: Y

**Repair Actions Taken:**
- Indentation standardization: X files
- Tab-to-space conversion: Y files
- List formatting fixes: Z files
- Trailing comma removal: A files
- Quote standardization: B files
- Whitespace cleanup: C files

**Persistent Issues:**
- Files requiring manual review: [list specific files]
- Complex structural issues: [describe]
- Recommended actions: [next steps]

**Format Compliance Status:**
- YAML validation: X% passing (target: 100%)
- JSON validation: Y% passing (target: 100%)
- Markdown structure: Z% compliant

**Prevention Recommendations:**
- Common error patterns identified: [list patterns]
- Generation prompt improvements needed: [suggestions]
- Validation checks to add: [recommendations]
```

**Git Workflow:**
```bash
git checkout master
git pull origin master
git add .
git commit -m "fix(taskstream): automated format repair and standardization

Format Fixes:
- YAML indentation: X files repaired
- JSON syntax: Y files repaired
- Whitespace cleanup: Z files
- Format validation: now at X% compliance

Files Modified: [count]
Persistent Issues: [count requiring manual review]"

git push origin master
gh pr create --title "TaskStream Repair: Session {N} Format Fixes" --body "Automated format repair and standardization session.

Validation Results:
- YAML: X/Y files passing (Z% compliance)
- JSON: X/Y files passing (Z% compliance)

Actions Taken:
- Indentation standardization
- Syntax error correction
- Whitespace cleanup

Manual Review Required: [count] files
Next Steps: [recommendations]"
```

## Session Objectives
- Achieve 100% YAML/JSON format compliance
- Standardize indentation and whitespace across all files
- Identify and document common error patterns
- Provide recommendations for error prevention

## Success Metrics
- YAML validation passing rate: 100%
- JSON validation passing rate: 100%
- Files requiring manual review: <5
- Format consistency score: 100%

**Focus:** Technical excellence in file formatting. This session is purely about fixing syntax errors and ensuring all files parse correctly. No content changes should be made - only format corrections.