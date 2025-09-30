#!/bin/bash
# Quick quality check script for TaskStream dataset

echo "======================================"
echo "TaskStream Quality Check"
echo "======================================"
echo ""

cd /Users/vrushankpatel/Desktop/WORKSPACE/TaskStream

# Run Python analysis
echo "Running comprehensive analysis..."
python3 /Users/vrushankpatel/Desktop/WORKSPACE/prepare_hf_dataset.py

echo ""
echo "======================================"
echo "Hugging Face Readiness Checklist"
echo "======================================"
echo ""
echo "Required for Public Dataset:"
echo "  ✓ 100+ files minimum"
echo "  ✓ 95%+ format compliance"
echo "  ✓ 10+ industries represented"
echo "  ✓ Multiple content categories"
echo "  ✓ README with proper documentation"
echo ""
echo "Nice to Have:"
echo "  • 500+ files (more comprehensive)"
echo "  • 25+ industries"
echo "  • Cross-category coverage"
echo "  • Temporal and numerical data"
echo "  • Clear use case documentation"
echo ""
