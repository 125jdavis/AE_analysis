#!/usr/bin/env python3
"""
Test .mlg file conversion and loading
"""

import os
import sys
import pandas as pd

def test_mlg_conversion():
    """Test MLG to CSV conversion"""
    mlg_file = "sample data/drive.mlg"
    csv_file = "sample data/drive.csv"
    
    print("=" * 70)
    print("Testing .mlg File Conversion")
    print("=" * 70)
    
    if not os.path.exists(mlg_file):
        print(f"✗ MLG file not found: {mlg_file}")
        return False
    
    print(f"✓ MLG file exists: {mlg_file}")
    print(f"  Size: {os.path.getsize(mlg_file):,} bytes")
    
    # Test conversion function
    import subprocess
    output_file = mlg_file.rsplit('.', 1)[0] + '.csv'
    
    print(f"\nTesting conversion...")
    print(f"  Expected output: {output_file}")
    
    # Check if CSV already exists
    if os.path.exists(output_file):
        print(f"✓ CSV already exists from previous conversion")
        print(f"  Size: {os.path.getsize(output_file):,} bytes")
    else:
        print(f"  CSV doesn't exist yet, attempting conversion...")
        try:
            result = subprocess.run(
                ['npx', 'mlg-converter', '--format=csv', mlg_file],
                capture_output=True,
                text=True,
                timeout=60
            )
            print(f"  Return code: {result.returncode}")
            if result.returncode == 0:
                print(f"✓ Conversion successful")
            else:
                print(f"✗ Conversion failed")
                print(f"  Stderr: {result.stderr}")
                return False
        except Exception as e:
            print(f"✗ Conversion error: {e}")
            return False
    
    # Try to load the CSV
    print(f"\nTesting CSV loading...")
    try:
        df = pd.read_csv(csv_file, sep=';')
        print(f"✓ CSV loaded successfully")
        print(f"  Rows: {len(df)}")
        print(f"  Columns: {len(df.columns)}")
        print(f"  First 5 columns: {list(df.columns[:5])}")
        
        # Check for common columns
        time_col = df.columns[0] if len(df.columns) > 0 else None
        print(f"\n  Time column: {time_col}")
        
        if len(df) > 0:
            print(f"  First value: {df.iloc[0, 0]}")
            print(f"✓ Data is accessible")
        
        return True
        
    except Exception as e:
        print(f"✗ Error loading CSV: {e}")
        return False

if __name__ == '__main__':
    success = test_mlg_conversion()
    print("\n" + "=" * 70)
    if success:
        print("✓ All tests passed!")
    else:
        print("✗ Tests failed")
    print("=" * 70)
    sys.exit(0 if success else 1)
