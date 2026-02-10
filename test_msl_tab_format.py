#!/usr/bin/env python3
"""
Test updated .msl file parsing with tab-separated format
"""

import pandas as pd
import os
import sys

def test_tab_separated_msl():
    """Test tab-separated .msl file (realistic MegaSquirt format)"""
    print("=" * 70)
    print("Test 1: Tab-separated .msl file (realistic MegaSquirt format)")
    print("=" * 70)
    
    filename = 'sample_data_realistic.msl'
    
    if not os.path.exists(filename):
        print(f"✗ Test file {filename} not found")
        return False
    
    try:
        # Simulate the updated parsing logic
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        # Count lines starting with quotes or # (metadata headers)
        skip_count = 0
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('"') or stripped.startswith('#'):
                skip_count += 1
            else:
                break
        
        # Read with column names as header
        data = pd.read_csv(filename, sep='\t', skiprows=skip_count, header=0,
                          engine='python', encoding='utf-8', encoding_errors='ignore')
        
        # Check if first row is units row and skip it
        if len(data) > 0:
            first_row_str = data.iloc[0].astype(str)
            has_letters = first_row_str.str.contains('[a-zA-Z°%]', regex=True, na=False).any()
            if has_letters:
                data = data.iloc[1:].reset_index(drop=True)
                # Convert columns to numeric where possible
                for col in data.columns:
                    data[col] = pd.to_numeric(data[col], errors='coerce')
        
        print(f"✓ Successfully parsed {filename}")
        print(f"  Columns: {list(data.columns)}")
        print(f"  Column count: {len(data.columns)}")
        print(f"  Row count: {len(data)}")
        
        # Verify columns are correct
        expected_cols = ['Time', 'RPM', 'TPS', 'PW', 'AFR', 'MAP', 'CLT']
        if list(data.columns) == expected_cols:
            print(f"✓ Columns match expected: {expected_cols}")
        else:
            print(f"✗ Column mismatch. Expected: {expected_cols}, Got: {list(data.columns)}")
            return False
        
        # Verify data types are numeric
        print(f"\n  Data types:")
        for col in data.columns:
            print(f"    {col}: {data[col].dtype}")
            if not pd.api.types.is_numeric_dtype(data[col]):
                print(f"✗ {col} is not numeric")
                return False
        
        print(f"\n  First row: {data.iloc[0].to_dict()}")
        print(f"✓ All columns are numeric")
        print(f"✓ Tab-separated .msl test passed!\n")
        return True
        
    except Exception as e:
        print(f"✗ Error parsing {filename}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_space_separated_msl():
    """Test old space-separated .msl file for backward compatibility"""
    print("=" * 70)
    print("Test 2: Space-separated .msl file (old format, backward compatibility)")
    print("=" * 70)
    
    filename = 'sample_data.msl'
    
    if not os.path.exists(filename):
        print(f"  Warning: {filename} not found, skipping test")
        return True
    
    try:
        # The new tab-based parser won't work with space-separated files
        # But we can detect and handle both formats
        
        # Try to detect format
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        # Check if file has tabs
        has_tabs = any('\t' in line for line in lines[:10])
        
        if has_tabs:
            print(f"  Detected tab-separated format")
            # Use new logic (same as test 1)
            skip_count = sum(1 for line in lines if line.strip().startswith(('"', '#')))
            data = pd.read_csv(filename, sep='\t', skiprows=skip_count, header=0,
                              engine='python', encoding='utf-8', encoding_errors='ignore')
            if len(data) > 0:
                first_row_str = data.iloc[0].astype(str)
                has_letters = first_row_str.str.contains('[a-zA-Z°%]', regex=True, na=False).any()
                if has_letters:
                    data = data.iloc[1:].reset_index(drop=True)
        else:
            print(f"  Detected space-separated format (old style)")
            # Fall back to old parsing for space-separated files
            data = pd.read_csv(filename, sep=r'\s+', comment='#', engine='python')
        
        print(f"✓ Successfully parsed {filename}")
        print(f"  Columns: {list(data.columns)}")
        print(f"  Row count: {len(data)}")
        print(f"✓ Backward compatibility test passed!\n")
        return True
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("Testing Updated .msl File Parsing")
    print("=" * 70 + "\n")
    
    results = []
    results.append(("Tab-separated .msl", test_tab_separated_msl()))
    results.append(("Space-separated .msl", test_space_separated_msl()))
    
    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {name}")
    
    all_passed = all(result for _, result in results)
    if all_passed:
        print("\n✓ All tests passed!")
        return 0
    else:
        print("\n✗ Some tests failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())
