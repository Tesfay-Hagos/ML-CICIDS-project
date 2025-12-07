#!/usr/bin/env python3
"""
Quick test script for data_config.py path discovery
Tests the path discovery without requiring pandas
"""

from pathlib import Path

def find_csv_directory(parent_dir):
    """Find the subdirectory containing CSV files"""
    if not parent_dir.exists():
        return None
    
    # Check if parent has CSV files directly
    csv_files = list(parent_dir.glob("*.csv"))
    if csv_files:
        return parent_dir
    
    # Check subdirectories
    for subdir in parent_dir.iterdir():
        if subdir.is_dir():
            csv_files = list(subdir.glob("*.csv"))
            if csv_files:
                return subdir
    
    return None

# Test the path discovery
BASE_PATH = Path("/home/tesfayh/Artificial_inteligence/ML/CICDS/ML-CICIDS-project")
FLOW_BASE = BASE_PATH / "GeneratedLabelledFlows"
ML_BASE = BASE_PATH / "MachineLearningCSV"

print("=" * 80)
print("PATH DISCOVERY TEST")
print("=" * 80)

print(f"\nBase path: {BASE_PATH}")
print(f"  Exists: {BASE_PATH.exists()}")

# Test GeneratedLabelledFlows
flow_path = find_csv_directory(FLOW_BASE)
print(f"\nGeneratedLabelledFlows:")
print(f"  Base: {FLOW_BASE}")
print(f"  Found: {flow_path}")
if flow_path:
    flow_files = sorted(list(flow_path.glob("*.csv")))
    print(f"  Files: {len(flow_files)}")
    if flow_files:
        print(f"  Sample: {flow_files[0].name}")

# Test MachineLearningCSV
ml_path = find_csv_directory(ML_BASE)
print(f"\nMachineLearningCSV:")
print(f"  Base: {ML_BASE}")
print(f"  Found: {ml_path}")
if ml_path:
    ml_files = sorted(list(ml_path.glob("*.csv")))
    print(f"  Files: {len(ml_files)}")
    if ml_files:
        print(f"  Sample: {ml_files[0].name}")
        print(f"\n  Expected sample path:")
        print(f"    {ml_path / 'Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv'}")

print("\n" + "=" * 80)
print("✓ Path discovery test complete!")
print("=" * 80)
