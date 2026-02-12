#!/usr/bin/env python3
"""
End-to-end test for MLG file loading through the complete workflow
"""

import os
import sys
import pandas as pd
import subprocess

def test_mlg_workflow():
    """Test complete MLG loading workflow"""
    
    print("=" * 70)
    print("End-to-End MLG File Loading Test")
    print("=" * 70)
    
    mlg_file = "sample data/drive.mlg"
    csv_file = "sample data/drive.csv"
    
    # Step 1: Check MLG file exists
    if not os.path.exists(mlg_file):
        print(f"✗ MLG file not found: {mlg_file}")
        return False
    print(f"\n✓ Step 1: MLG file found")
    print(f"  File: {mlg_file}")
    print(f"  Size: {os.path.getsize(mlg_file):,} bytes")
    
    # Step 2: Convert MLG to CSV (simulate convert_mlg_to_csv function)
    print(f"\n✓ Step 2: Converting MLG to CSV...")
    output_file = mlg_file.rsplit('.', 1)[0] + '.csv'
    
    # Check if CSV already exists
    if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
        print(f"  CSV already exists from previous conversion")
    else:
        try:
            result = subprocess.run(
                ['npx', 'mlg-converter', '--format=csv', mlg_file],
                capture_output=True,
                text=True,
                timeout=60
            )
            if result.returncode != 0:
                print(f"✗ Conversion failed")
                return False
        except Exception as e:
            print(f"✗ Conversion error: {e}")
            return False
    
    print(f"✓ CSV file available: {output_file}")
    print(f"  Size: {os.path.getsize(output_file):,} bytes")
    
    # Step 3: Load CSV with units row handling (simulate load_file logic)
    print(f"\n✓ Step 3: Loading CSV...")
    try:
        data = pd.read_csv(output_file, sep=';', low_memory=False)
        print(f"  Initial rows: {len(data)}")
        print(f"  Columns: {len(data.columns)}")
        
        # Check for units row
        if len(data) > 0:
            first_row_str = data.iloc[0].astype(str)
            has_letters = first_row_str.str.contains('[a-zA-Z°%]', regex=True, na=False).any()
            
            if has_letters:
                print(f"  Detected units row, removing...")
                data = data.iloc[1:].reset_index(drop=True)
                # Convert to numeric
                for col in data.columns:
                    data[col] = pd.to_numeric(data[col], errors='coerce')
        
        print(f"✓ Final data ready")
        print(f"  Rows: {len(data)}")
        print(f"  Columns: {len(data.columns)}")
        
    except Exception as e:
        print(f"✗ Loading error: {e}")
        return False
    
    # Step 4: Verify data is usable
    print(f"\n✓ Step 4: Verifying data...")
    
    # Check for common column names
    columns_lower = {col.lower(): col for col in data.columns}
    
    found_columns = []
    for pattern in ['time', 'rpm', 'tps', 'afr']:
        for col_lower, col in columns_lower.items():
            if pattern in col_lower:
                found_columns.append(col)
                break
    
    print(f"  Found potential data columns:")
    for col in found_columns:
        if col in data.columns and len(data) > 0:
            first_val = data[col].iloc[0]
            print(f"    {col}: {first_val}")
    
    # Check for numeric data
    numeric_cols = sum(1 for col in data.columns if pd.api.types.is_numeric_dtype(data[col]))
    print(f"  Numeric columns: {numeric_cols}/{len(data.columns)}")
    
    if numeric_cols > 0 and len(data) > 0:
        print(f"\n✓ Step 5: Data verification successful!")
        return True
    else:
        print(f"\n✗ Data verification failed")
        return False

if __name__ == '__main__':
    success = test_mlg_workflow()
    
    print("\n" + "=" * 70)
    if success:
        print("✓ END-TO-END TEST PASSED!")
        print("The MLG file can be successfully opened and processed.")
    else:
        print("✗ END-TO-END TEST FAILED!")
    print("=" * 70)
    
    sys.exit(0 if success else 1)
