#!/bin/bash
# Script to compare the two CICIDS2017 datasets

echo "================================================================================"
echo "CICIDS2017 DATASET COMPARISON ANALYSIS"
echo "================================================================================"
echo ""

BASE_PATH="/home/tesfayh/Artificial inteligence/ML/CICDS/ML-CICIDS-project"
FLOW_PATH="${BASE_PATH}/GeneratedLabelledFlows/TrafficLabelling "
ML_PATH="${BASE_PATH}/MachineLearningCSV/MachineLearningCVE"

# Count columns in first file
echo "1. COLUMN STRUCTURE COMPARISON"
echo "--------------------------------------------------------------------------------"

FLOW_COLS=$(head -n 1 "${FLOW_PATH}/Monday-WorkingHours.pcap_ISCX.csv" | tr ',' '\n' | wc -l)
ML_COLS=$(head -n 1 "${ML_PATH}/Monday-WorkingHours.pcap_ISCX.csv" | tr ',' '\n' | wc -l)

echo "GeneratedLabelledFlows columns: ${FLOW_COLS}"
echo "MachineLearningCVE columns: ${ML_COLS}"
echo ""

echo "COLUMNS ONLY IN GeneratedLabelledFlows (first 6):"
echo "  [1] Flow ID"
echo "  [2] Source IP"
echo "  [3] Source Port"
echo "  [4] Destination IP"
echo "  [5] Destination Port (exists in both but different position)"
echo "  [6] Protocol"
echo "  [7] Timestamp"
echo ""

echo "MachineLearningCVE starts directly with:"
echo "  [1] Destination Port"
echo "  [2] Flow Duration"
echo "  ..."
echo ""

# Row count comparison
echo "2. ROW COUNT COMPARISON (per file)"
echo "--------------------------------------------------------------------------------"
printf "%-60s %-12s %-12s %-8s\n" "File Name" "Flow" "ML" "Match"
echo "--------------------------------------------------------------------------------"

for flow_file in "${FLOW_PATH}"/*.csv; do
    filename=$(basename "$flow_file")
    ml_file="${ML_PATH}/${filename}"
    
    if [ -f "$ml_file" ]; then
        flow_rows=$(($(wc -l < "$flow_file") - 1))
        ml_rows=$(($(wc -l < "$ml_file") - 1))
        
        if [ $flow_rows -eq $ml_rows ]; then
            match="✓"
        else
            match="✗"
        fi
        
        printf "%-60s %-12s %-12s %-8s\n" "$filename" "$flow_rows" "$ml_rows" "$match"
    fi
done
echo ""

# Total statistics
echo "3. TOTAL DATASET STATISTICS"
echo "--------------------------------------------------------------------------------"

TOTAL_FLOW=0
TOTAL_ML=0

for flow_file in "${FLOW_PATH}"/*.csv; do
    filename=$(basename "$flow_file")
    ml_file="${ML_PATH}/${filename}"
    
    if [ -f "$ml_file" ]; then
        flow_rows=$(($(wc -l < "$flow_file") - 1))
        ml_rows=$(($(wc -l < "$ml_file") - 1))
        
        TOTAL_FLOW=$((TOTAL_FLOW + flow_rows))
        TOTAL_ML=$((TOTAL_ML + ml_rows))
    fi
done

echo "Total GeneratedLabelledFlows records: $TOTAL_FLOW"
echo "Total MachineLearningCVE records: $TOTAL_ML"
echo "Difference: $((TOTAL_FLOW - TOTAL_ML))"
echo ""

# Label distribution for Monday file
echo "4. LABEL DISTRIBUTION (Monday-WorkingHours.pcap_ISCX.csv sample)"
echo "--------------------------------------------------------------------------------"
echo "GeneratedLabelledFlows:"
tail -n +2 "${FLOW_PATH}/Monday-WorkingHours.pcap_ISCX.csv" | awk -F',' '{print $NF}' | sort | uniq -c | sort -rn
echo ""

echo "MachineLearningCVE:"
tail -n +2 "${ML_PATH}/Monday-WorkingHours.pcap_ISCX.csv" | awk -F',' '{print $NF}' | sort | uniq -c | sort -rn
echo ""

echo "================================================================================"
echo "SUMMARY & RECOMMENDATION"
echo "================================================================================"
cat << 'EOF'

The two datasets represent different formats of the CICIDS2017 dataset:

1. GeneratedLabelledFlows (85 columns):
   ✓ Contains full flow information including identifiers
   ✓ Includes: Flow ID, Source IP, Source Port, Destination IP, Protocol, Timestamp
   ✓ More suitable for network analysis and flow tracking
   ✓ Original/raw labeled flows from traffic analysis
   ✓ Can be used for flow-level analysis and visualization

2. MachineLearningCSV/MachineLearningCVE (79 columns):
   ✓ Preprocessed specifically for machine learning
   ✓ Removes identifying information (IPs, ports, Flow IDs, timestamps)
   ✓ Focuses only on flow statistical features
   ✓ Privacy-preserving (no personal/network identifiable info)
   ✓ Ready for ML model training without additional preprocessing

KEY DIFFERENCES:
- 6 fewer columns in ML version (removed identifiers)
- Thursday-WorkingHours-Morning-WebAttacks has different row counts
  (458,969 vs 170,367) suggesting data cleaning/filtering in ML version

RECOMMENDATION FOR YOUR PROJECT:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

For Machine Learning / Intrusion Detection System:
→ Use MachineLearningCSV/MachineLearningCVE
  - Standard format for ML-based IDS
  - Privacy compliant
  - Feature-focused
  - No need to drop columns

For Network Traffic Analysis / Forensics:
→ Use GeneratedLabelledFlows
  - Complete flow information
  - Can track specific connections
  - Includes temporal information

SUGGESTED APPROACH:
Start with MachineLearningCSV/MachineLearningCVE for your ML model training.
Use GeneratedLabelledFlows only if you need to analyze specific flows or
perform network forensics.

EOF
