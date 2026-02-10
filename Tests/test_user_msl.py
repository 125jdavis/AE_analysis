#!/usr/bin/env python3
"""
Test script for validating .msl file parsing
Usage: python test_user_msl.py <path_to_msl_file>
"""

import sys
import pandas as pd
import os

def test_msl_file(filename):
    """Test parsing of a user-provided .msl file"""
    
    if not os.path.exists(filename):
        print(f"✗ Error: File '{filename}' not found")
        return False
    
    print("=" * 70)
    print(f"Testing .msl file: {filename}")
    print("=" * 70)
    
    try:
        # Show first 10 lines
        print("\nFirst 10 lines of file:")
        print("-" * 70)
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            for i, line in enumerate(f):
                if i >= 10:
                    break
                # Show tabs as [TAB]
                display_line = line.rstrip().replace('\t', '[TAB]')
                print(f"{i+1:3d}: {display_line}")
        
        # Detect format
        print("\n" + "=" * 70)
        print("Format Detection:")
        print("-" * 70)
        
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        has_tabs = any('\t' in line for line in lines[:10] if line.strip() and not line.strip().startswith(('"', '#')))
        print(f"Format detected: {'TAB-separated' if has_tabs else 'SPACE-separated'}")
        
        # Count header lines
        skip_count = 0
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('"') or stripped.startswith('#'):
                skip_count += 1
            else:
                break
        print(f"Metadata header lines: {skip_count}")
        
        # Parse the file using the same logic as ae_analyzer.py
        print("\n" + "=" * 70)
        print("Parsing File:")
        print("-" * 70)
        
        if has_tabs:
            # Tab-separated format
            data = pd.read_csv(filename, sep='\t', skiprows=skip_count, header=0,
                              engine='python', encoding='utf-8', encoding_errors='ignore')
            
            print(f"Initial columns: {list(data.columns)}")
            print(f"Initial row count: {len(data)}")
            
            # Check if first row is units
            if len(data) > 0:
                first_row_str = data.iloc[0].astype(str)
                has_letters = first_row_str.str.contains('[a-zA-Z°%]', regex=True, na=False).any()
                
                if has_letters:
                    print(f"First row appears to be units: {data.iloc[0].to_dict()}")
                    print("  → Skipping units row")
                    data = data.iloc[1:].reset_index(drop=True)
                    # Convert to numeric
                    for col in data.columns:
                        data[col] = pd.to_numeric(data[col], errors='coerce')
        else:
            # Space-separated format
            data = pd.read_csv(filename, sep=r'\s+', comment='#', engine='python')
        
        print(f"\n✓ Successfully parsed file!")
        print(f"  Final columns: {list(data.columns)}")
        print(f"  Column count: {len(data.columns)}")
        print(f"  Row count: {len(data)}")
        
        # Show column data types
        print(f"\n  Column data types:")
        for col in data.columns:
            print(f"    {col:20s} : {str(data[col].dtype):10s} (sample: {data[col].iloc[0] if len(data) > 0 else 'N/A'})")
        
        # Show first few rows
        if len(data) > 0:
            print(f"\n  First 3 rows:")
            print(data.head(3).to_string(index=True))
        
        # Show statistics
        print(f"\n  Basic statistics:")
        print(f"    Rows with any NaN: {data.isna().any(axis=1).sum()}")
        print(f"    Columns with any NaN: {data.isna().any(axis=0).sum()}")
        
        print("\n" + "=" * 70)
        print("✓ Test completed successfully!")
        print("=" * 70)
        return True
        
    except Exception as e:
        print(f"\n✗ Error parsing file: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python test_user_msl.py <path_to_msl_file>")
        print("\nExample:")
        print("  python test_user_msl.py my_datalog.msl")
        sys.exit(1)
    
    filename = sys.argv[1]
    success = test_msl_file(filename)
    sys.exit(0 if success else 1)
