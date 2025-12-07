#!/usr/bin/env python3
"""
Script to compare the two CICIDS2017 datasets:
1. GeneratedLabelledFlows
2. MachineLearningCSV/MachineLearningCVE
"""

import pandas as pd
import os
from pathlib import Path
import json

def analyze_datasets():
    """Compare the two datasets and generate a comprehensive report."""
    
    base_path = Path("/home/tesfayh/Artificial inteligence/ML/CICDS/ML-CICIDS-project")
    
    # Define paths
    flow_path = base_path / "GeneratedLabelledFlows" / "TrafficLabelling "
    ml_path = base_path / "MachineLearningCSV" / "MachineLearningCVE"
    
    # Get all CSV files
    flow_files = sorted([f for f in flow_path.glob("*.csv")])
    ml_files = sorted([f for f in ml_path.glob("*.csv")])
    
    print("=" * 80)
    print("CICIDS2017 DATASET COMPARISON ANALYSIS")
    print("=" * 80)
    print()
    
    # 1. File-level comparison
    print("1. FILE-LEVEL COMPARISON")
    print("-" * 80)
    print(f"GeneratedLabelledFlows files: {len(flow_files)}")
    print(f"MachineLearningCSV/MachineLearningCVE files: {len(ml_files)}")
    print()
    
    # 2. Column structure comparison (using first file as sample)
    print("2. COLUMN STRUCTURE COMPARISON")
    print("-" * 80)
    
    if flow_files and ml_files:
        # Read headers only
        flow_df = pd.read_csv(flow_files[0], nrows=0)
        ml_df = pd.read_csv(ml_files[0], nrows=0)
        
        flow_cols = list(flow_df.columns)
        ml_cols = list(ml_df.columns)
        
        print(f"GeneratedLabelledFlows columns: {len(flow_cols)}")
        print(f"MachineLearningCVE columns: {len(ml_cols)}")
        print()
        
        # Find differences
        print("COLUMNS ONLY IN GeneratedLabelledFlows:")
        flow_only = set(flow_cols) - set(ml_cols)
        for col in sorted(flow_only):
            idx = flow_cols.index(col)
            print(f"  [{idx+1}] {col}")
        print()
        
        print("COLUMNS ONLY IN MachineLearningCVE:")
        ml_only = set(ml_cols) - set(flow_cols)
        for col in sorted(ml_only):
            idx = ml_cols.index(col)
            print(f"  [{idx+1}] {col}")
        print()
        
        print("COMMON COLUMNS: {}/{}".format(len(set(flow_cols) & set(ml_cols)), 
                                             max(len(flow_cols), len(ml_cols))))
        print()
    
    # 3. Row count comparison
    print("3. ROW COUNT COMPARISON (per file)")
    print("-" * 80)
    print(f"{'File Name':<55} {'Flow':<12} {'ML':<12} {'Match':<8}")
    print("-" * 80)
    
    row_mismatches = []
    for flow_file in flow_files:
        ml_file = ml_path / flow_file.name
        if ml_file.exists():
            flow_rows = sum(1 for _ in open(flow_file)) - 1  # Exclude header
            ml_rows = sum(1 for _ in open(ml_file)) - 1
            match = "✓" if flow_rows == ml_rows else "✗"
            print(f"{flow_file.name:<55} {flow_rows:<12,} {ml_rows:<12,} {match:<8}")
            
            if flow_rows != ml_rows:
                row_mismatches.append({
                    'file': flow_file.name,
                    'flow_rows': flow_rows,
                    'ml_rows': ml_rows,
                    'difference': flow_rows - ml_rows
                })
    print()
    
    # 4. Detailed analysis for mismatched files
    if row_mismatches:
        print("4. DETAILED ANALYSIS OF MISMATCHED FILES")
        print("-" * 80)
        for mismatch in row_mismatches:
            print(f"\nFile: {mismatch['file']}")
            print(f"  GeneratedLabelledFlows: {mismatch['flow_rows']:,} rows")
            print(f"  MachineLearningCVE: {mismatch['ml_rows']:,} rows")
            print(f"  Difference: {abs(mismatch['difference']):,} rows")
            print(f"  Ratio: {mismatch['flow_rows']/mismatch['ml_rows']:.2f}x")
    print()
    
    # 5. Label distribution check (sample from one file)
    print("5. LABEL DISTRIBUTION (Monday-WorkingHours.pcap_ISCX.csv)")
    print("-" * 80)
    
    monday_flow = flow_path / "Monday-WorkingHours.pcap_ISCX.csv"
    monday_ml = ml_path / "Monday-WorkingHours.pcap_ISCX.csv"
    
    if monday_flow.exists() and monday_ml.exists():
        flow_labels = pd.read_csv(monday_flow, usecols=[' Label'])
        ml_labels = pd.read_csv(monday_ml, usecols=[' Label'])
        
        print("\nGeneratedLabelledFlows:")
        print(flow_labels[' Label'].value_counts())
        
        print("\nMachineLearningCVE:")
        print(ml_labels[' Label'].value_counts())
    
    print()
    print("=" * 80)
    print("SUMMARY & RECOMMENDATION")
    print("=" * 80)
    print("""
The two datasets represent different formats of the CICIDS2017 dataset:

1. GeneratedLabelledFlows (85 columns):
   - Contains full flow information including identifiers
   - Includes: Flow ID, Source IP, Source Port, Destination IP, Protocol, Timestamp
   - More suitable for network analysis and flow tracking
   - Original/raw labeled flows from traffic analysis

2. MachineLearningCSV/MachineLearningCVE (79 columns):
   - Preprocessed for machine learning
   - Removes identifying information (IPs, ports, timestamps)
   - Focuses only on flow statistical features
   - Privacy-preserving (no IP addresses)
   - Ready for ML model training

RECOMMENDATION:
- Use GeneratedLabelledFlows if you need complete flow information for analysis
- Use MachineLearningCSV/MachineLearningCVE for machine learning model training
- The MachineLearningCSV version is the standard for ML-based intrusion detection

NOTE: Thursday-WorkingHours-Morning-WebAttacks file has different row counts,
suggesting possible data cleaning/filtering in the ML version.
    """)

if __name__ == "__main__":
    analyze_datasets()
