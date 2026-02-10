#!/usr/bin/env python3
"""
Test .msl file parsing functionality
"""

import pandas as pd
import os
import sys

def test_msl_parsing():
    """Test that .msl files can be parsed correctly"""
    test_file = 'sample_data.msl'
    
    if not os.path.exists(test_file):
        print(f"Error: Test file {test_file} not found")
        return False
    
    try:
        # Parse MSL file (space-separated with # comments)
        df = pd.read_csv(test_file, sep=r'\s+', comment='#', engine='python')
        
        print(f"✓ Successfully parsed {test_file}")
        print(f"  Rows: {len(df)}")
        print(f"  Columns: {list(df.columns)}")
        print(f"  Column count: {len(df.columns)}")
        
        # Verify we have the expected columns
        expected_columns = ['Time', 'RPM', 'TPS', 'PW', 'AFR']
        if list(df.columns) == expected_columns:
            print(f"✓ Columns match expected: {expected_columns}")
        else:
            print(f"✗ Column mismatch. Expected: {expected_columns}, Got: {list(df.columns)}")
            return False
        
        # Verify we have data rows
        if len(df) > 0:
            print(f"✓ Data loaded: {len(df)} rows")
            print(f"\nFirst 3 rows:")
            print(df.head(3))
        else:
            print(f"✗ No data rows loaded")
            return False
        
        # Check data types
        print(f"\nData types:")
        print(df.dtypes)
        
        # Verify numeric columns
        numeric_cols = ['Time', 'RPM', 'TPS', 'PW', 'AFR']
        for col in numeric_cols:
            if pd.api.types.is_numeric_dtype(df[col]):
                print(f"✓ {col} is numeric")
            else:
                print(f"✗ {col} is not numeric")
                return False
        
        print("\n✓ All tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Error parsing {test_file}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_msl_parsing()
    sys.exit(0 if success else 1)
