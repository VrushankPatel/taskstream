import os
from pathlib import Path
from collections import defaultdict

# Build coverage matrix by industry/topic
coverage = defaultdict(lambda: {
    'workflows': 0,
    'decisions': 0,
    'communications': 0,
    'org_structures': 0,
    'metrics': 0,
    'policies': 0
})

# Scan all directories
for category, directory in [
    ('workflows', 'workflows/'),
    ('decisions', 'decisions/'),
    ('communications', 'communications/'),
    ('org_structures', 'org_structures/'),
    ('metrics', 'metrics/'),
    ('policies', 'policies/')
]:
    files = list(Path(directory).glob('*'))
    for file in files:
        # Extract industry/topic from filename
        parts = file.stem.split('_')
        industry = parts[0] if parts else 'unknown'
        coverage[industry][category] += 1

# Generate coverage report
print("\n=== CROSS-CATEGORY COVERAGE ANALYSIS ===")
for industry in sorted(coverage.keys()):
    total = sum(coverage[industry].values())
    if total > 0:
        completeness = sum(1 for v in coverage[industry].values() if v > 0)
        print(f"\n{industry.upper()}:")
        print(f"  Total files: {total}")
        print(f"  Category coverage: {completeness}/6 ({completeness*100//6}%)")
        print(f"  Breakdown: W:{coverage[industry]['workflows']} D:{coverage[industry]['decisions']} "
              f"C:{coverage[industry]['communications']} O:{coverage[industry]['org_structures']} "
              f"M:{coverage[industry]['metrics']} P:{coverage[industry]['policies']}")

        # Flag incomplete coverage
        missing = [k for k, v in coverage[industry].items() if v == 0]
        if missing:
            print(f"  MISSING: {', '.join(missing)}")