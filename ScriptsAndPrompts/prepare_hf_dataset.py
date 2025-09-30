#!/usr/bin/env python3
"""
Prepare TaskStream dataset for Hugging Face upload
"""

import json
import yaml
from pathlib import Path
from collections import defaultdict

def analyze_dataset():
    """Analyze dataset quality and completeness"""
    stats = {
        'total_files': 0,
        'by_category': defaultdict(int),
        'by_industry': defaultdict(int),
        'format_valid': {'yaml': 0, 'json': 0, 'yaml_total': 0, 'json_total': 0},
        'quality_issues': []
    }
    
    categories = ['workflows', 'decisions', 'communications', 'org_structures', 'metrics', 'policies']
    
    for category in categories:
        cat_path = Path(category)
        if not cat_path.exists():
            continue
            
        for file in cat_path.glob('*'):
            if file.is_file():
                stats['total_files'] += 1
                stats['by_category'][category] += 1
                
                # Extract industry from filename
                industry = file.stem.split('_')[0]
                stats['by_industry'][industry] += 1
                
                # Validate format
                if file.suffix == '.yaml':
                    stats['format_valid']['yaml_total'] += 1
                    try:
                        yaml.safe_load(file.read_text())
                        stats['format_valid']['yaml'] += 1
                    except Exception as e:
                        stats['quality_issues'].append(f"YAML error in {file}: {str(e)[:50]}")
                
                elif file.suffix == '.json':
                    stats['format_valid']['json_total'] += 1
                    try:
                        json.loads(file.read_text())
                        stats['format_valid']['json'] += 1
                    except Exception as e:
                        stats['quality_issues'].append(f"JSON error in {file}: {str(e)[:50]}")
    
    return stats

def create_dataset_card(stats):
    """Create README.md for Hugging Face dataset card"""
    
    yaml_compliance = (stats['format_valid']['yaml'] / stats['format_valid']['yaml_total'] * 100) if stats['format_valid']['yaml_total'] > 0 else 0
    json_compliance = (stats['format_valid']['json'] / stats['format_valid']['json_total'] * 100) if stats['format_valid']['json_total'] > 0 else 0
    
    # Sort industries by count
    top_industries = sorted(stats['by_industry'].items(), key=lambda x: x[1], reverse=True)[:10]
    
    # Build industry table separately to avoid f-string issues
    industry_table = '\n'.join(f"| {ind} | {count} |" for ind, count in top_industries)
    
    card = f"""---
language:
- en
license: apache-2.0
task_categories:
- text-generation
- question-answering
- summarization
tags:
- business
- enterprise
- workflows
- decision-making
- processes
size_categories:
- 1K<n<10K
---

# TaskStream: Enterprise Workflow Dataset

TaskStream is a comprehensive dataset of enterprise business workflows, decision-making processes, organizational structures, and operational documentation. It captures how real businesses operate across industries, providing detailed examples of business processes, communications, metrics, and policies.

## Dataset Summary

- **Total Files:** {stats['total_files']:,}
- **Industries Covered:** {len(stats['by_industry'])}
- **Content Categories:** {len(stats['by_category'])}
- **Format Compliance:** YAML: {yaml_compliance:.1f}%, JSON: {json_compliance:.1f}%

## Content Categories

| Category | Files | Description |
|----------|-------|-------------|
| Workflows | {stats['by_category']['workflows']} | Step-by-step business process documentation (YAML) |
| Decisions | {stats['by_category']['decisions']} | Decision scenarios with stakeholders and outcomes (JSON) |
| Communications | {stats['by_category']['communications']} | Email threads, meeting notes, status reports (Markdown) |
| Org Structures | {stats['by_category']['org_structures']} | Team hierarchies, roles, and responsibilities (Markdown) |
| Metrics | {stats['by_category']['metrics']} | KPI dashboards and performance tracking (Markdown) |
| Policies | {stats['by_category']['policies']} | Company procedures and guidelines (Markdown) |

## Top Industries Represented

| Industry | Files |
|----------|-------|
{industry_table}

## Use Cases

1. **Training Business AI Assistants** - Teaching LLMs how enterprises actually operate
2. **Process Mining & Analysis** - Understanding common business workflow patterns
3. **Business Process Automation** - Identifying automation opportunities
4. **Organizational Design** - Learning from real company structures
5. **Decision Intelligence** - Analyzing how businesses make strategic decisions
6. **Enterprise Search & RAG** - Building business knowledge bases

## Dataset Structure

```
TaskStream/
├── workflows/              # YAML process documentation
├── decisions/              # JSON decision scenarios
├── communications/         # Markdown communication examples
├── org_structures/         # Markdown organizational charts
├── metrics/               # Markdown KPI dashboards
├── policies/              # Markdown policy documents
├── SPECIFICATION.md       # Dataset specification
└── README.md             # This file
```

## File Formats

### Workflows (YAML)
```yaml
workflow:
  id: "workflow_001"
  title: "Process Name"
  department: "Department"
  complexity: "simple|medium|complex"
  participants: ["Role1", "Role2"]
  temporal_data:
    typical_cycle_time: "X days"
    seasonal_variations: [...]
  steps:
    - step: 1
      actor: "Role"
      action: "Description"
      duration: "Time"
  performance_history:
    success_rate_trend: "..."
```

### Decisions (JSON)
```json
{{
  "scenario_id": "decision_001",
  "decision_date": "YYYY-MM-DD",
  "stakeholders": {{}},
  "decision_process": [],
  "business_impact": {{}},
  "outcome": "Approved|Rejected|Deferred"
}}
```

## Quality Standards

- ✅ All content based on realistic business scenarios
- ✅ Enterprise-appropriate language and terminology
- ✅ Validated file formats (YAML/JSON compliance: >{yaml_compliance:.0f}%)
- ✅ Temporal data included for trend analysis
- ✅ Numerical data in metrics for quantitative analysis
- ✅ Cross-category scenario coverage

## Data Quality

{'⚠️ **Quality Issues Found:** ' + str(len(stats['quality_issues'])) if stats['quality_issues'] else '✅ **No Format Errors Detected**'}

## Limitations

- Synthetic data generated by AI, not from real company records
- May not capture all nuances of specific industries or company cultures
- Temporal data is realistic but not from actual historical records
- No personally identifiable information (intentionally)

## Citation

If you use TaskStream in your research or applications, please cite:

```bibtex
@dataset{{taskstream2025,
  title={{TaskStream: Enterprise Workflow Dataset}},
  author={{TaskStream Project}},
  year={{2025}},
  publisher={{Hugging Face}},
  howpublished={{\\url{{https://huggingface.co/datasets/YOUR_USERNAME/taskstream}}}}
}}
```

## License

Apache 2.0 - See LICENSE file for details

## Maintenance

This dataset is continuously updated through an automated generation and quality control pipeline.

Last Updated: {Path('CHANGES.md').stat().st_mtime if Path('CHANGES.md').exists() else 'Unknown'}
"""
    
    return card

def main():
    print("Analyzing TaskStream dataset...")
    stats = analyze_dataset()
    
    print(f"\nDataset Statistics:")
    print(f"Total Files: {stats['total_files']}")
    print(f"Industries: {len(stats['by_industry'])}")
    print(f"\nBy Category:")
    for cat, count in stats['by_category'].items():
        print(f"  {cat}: {count}")
    
    print(f"\nFormat Validation:")
    if stats['format_valid']['yaml_total'] > 0:
        yaml_pct = stats['format_valid']['yaml'] / stats['format_valid']['yaml_total'] * 100
        print(f"  YAML: {stats['format_valid']['yaml']}/{stats['format_valid']['yaml_total']} ({yaml_pct:.1f}%)")
    if stats['format_valid']['json_total'] > 0:
        json_pct = stats['format_valid']['json'] / stats['format_valid']['json_total'] * 100
        print(f"  JSON: {stats['format_valid']['json']}/{stats['format_valid']['json_total']} ({json_pct:.1f}%)")
    
    if stats['quality_issues']:
        print(f"\n⚠️  Quality Issues Found: {len(stats['quality_issues'])}")
        print("First 5 issues:")
        for issue in stats['quality_issues'][:5]:
            print(f"  - {issue}")
    else:
        print("\n✅ No format errors detected!")
    
    # Create dataset card
    print("\nGenerating Hugging Face dataset card...")
    card = create_dataset_card(stats)
    
    # Save to root directory
    readme_path = Path('README_HF.md')
    readme_path.write_text(card)
    print(f"✅ Dataset card saved to {readme_path}")
    
    # Quality assessment
    print("\n" + "="*60)
    print("HUGGING FACE READINESS ASSESSMENT")
    print("="*60)
    
    checks = []
    
    # Check 1: Minimum file count
    if stats['total_files'] >= 100:
        checks.append(("✅", f"File count: {stats['total_files']} (minimum: 100)"))
    else:
        checks.append(("❌", f"File count: {stats['total_files']} (minimum: 100)"))
    
    # Check 2: Format compliance
    yaml_compliance = (stats['format_valid']['yaml'] / stats['format_valid']['yaml_total'] * 100) if stats['format_valid']['yaml_total'] > 0 else 100
    json_compliance = (stats['format_valid']['json'] / stats['format_valid']['json_total'] * 100) if stats['format_valid']['json_total'] > 0 else 100
    avg_compliance = (yaml_compliance + json_compliance) / 2
    
    if avg_compliance >= 95:
        checks.append(("✅", f"Format compliance: {avg_compliance:.1f}% (minimum: 95%)"))
    else:
        checks.append(("❌", f"Format compliance: {avg_compliance:.1f}% (minimum: 95%)"))
    
    # Check 3: Industry diversity
    if len(stats['by_industry']) >= 10:
        checks.append(("✅", f"Industry diversity: {len(stats['by_industry'])} industries (minimum: 10)"))
    else:
        checks.append(("⚠️ ", f"Industry diversity: {len(stats['by_industry'])} industries (recommended: 10+)"))
    
    # Check 4: Category coverage
    if len(stats['by_category']) >= 5:
        checks.append(("✅", f"Category coverage: {len(stats['by_category'])} categories (minimum: 5)"))
    else:
        checks.append(("❌", f"Category coverage: {len(stats['by_category'])} categories (minimum: 5)"))
    
    # Check 5: README exists
    if Path('README.md').exists():
        checks.append(("✅", "README.md exists"))
    else:
        checks.append(("⚠️ ", "README.md missing (will use README_HF.md)"))
    
    for status, msg in checks:
        print(f"{status} {msg}")
    
    passed = sum(1 for status, _ in checks if status == "✅")
    total = len(checks)
    
    print("\n" + "="*60)
    if passed >= 4:
        print("✅ READY FOR HUGGING FACE")
        print(f"   Score: {passed}/{total} checks passed")
    elif passed >= 3:
        print("⚠️  NEARLY READY - Address warnings before upload")
        print(f"   Score: {passed}/{total} checks passed")
    else:
        print("❌ NOT READY - Fix critical issues before upload")
        print(f"   Score: {passed}/{total} checks passed")
    print("="*60)

if __name__ == "__main__":
    main()
