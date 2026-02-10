#!/usr/bin/env python3
"""
Test the CSV parsing fix
"""

import pandas as pd

def test_csv_parsing_fix():
    """Test that the fixed parsing logic works correctly"""
    
    print("=" * 70)
    print("TESTING CSV PARSING FIX")
    print("=" * 70)
    
    filename = 'sample_data.csv'
    
    # Simulate the FIXED logic
    print("\nTesting FIXED parsing logic...")
    try:
        data = pd.read_csv(filename, sep=';')
        print(f"  Step 1: Read with sep=';'")
        print(f"    Columns found: {len(data.columns)}")
        print(f"    Column names: {list(data.columns)}")
        
        # If semicolon parse resulted in only 1 column, it's likely comma-separated
        if len(data.columns) == 1:
            print(f"  Step 2: Only 1 column found, trying comma separator...")
            data = pd.read_csv(filename, sep=',')
            print(f"    Columns found: {len(data.columns)}")
            print(f"    Column names: {list(data.columns)}")
    except (pd.errors.ParserError, pd.errors.EmptyDataError) as e:
        print(f"  Step 1 failed: {e}")
        print(f"  Step 2: Trying comma separator...")
        data = pd.read_csv(filename, sep=',')
        print(f"    Columns found: {len(data.columns)}")
        print(f"    Column names: {list(data.columns)}")
    
    print(f"\nFINAL RESULT:")
    print(f"  Columns: {list(data.columns)}")
    print(f"  Shape: {data.shape}")
    
    # Test with semicolon-separated file
    print("\n" + "=" * 70)
    print("Creating and testing semicolon-separated CSV...")
    
    # Create a test semicolon-separated file
    semicolon_csv = 'test_semicolon.csv'
    with open(semicolon_csv, 'w') as f:
        f.write("Time;RPM;TPS;PW;AFR\n")
        f.write("0.00;1000;5.2;2.1;14.7\n")
        f.write("0.05;1020;5.5;2.1;14.6\n")
    
    print(f"Created {semicolon_csv}")
    
    # Test with the same logic
    try:
        data_semi = pd.read_csv(semicolon_csv, sep=';')
        print(f"  Step 1: Read with sep=';'")
        print(f"    Columns found: {len(data_semi.columns)}")
        print(f"    Column names: {list(data_semi.columns)}")
        
        if len(data_semi.columns) == 1:
            print(f"  Step 2: Only 1 column found, trying comma separator...")
            data_semi = pd.read_csv(semicolon_csv, sep=',')
            print(f"    Columns found: {len(data_semi.columns)}")
            print(f"    Column names: {list(data_semi.columns)}")
    except (pd.errors.ParserError, pd.errors.EmptyDataError) as e:
        print(f"  Step 1 failed: {e}")
        print(f"  Step 2: Trying comma separator...")
        data_semi = pd.read_csv(semicolon_csv, sep=',')
        print(f"    Columns found: {len(data_semi.columns)}")
        print(f"    Column names: {list(data_semi.columns)}")
    
    print(f"\nFINAL RESULT:")
    print(f"  Columns: {list(data_semi.columns)}")
    print(f"  Shape: {data_semi.shape}")
    
    # Cleanup
    import os
    os.remove(semicolon_csv)
    
    print("\n" + "=" * 70)
    print("CONCLUSION:")
    if len(data.columns) == 5:
        print("✓ Comma-separated CSV parsed correctly (5 columns)")
    else:
        print(f"✗ Comma-separated CSV FAILED ({len(data.columns)} columns)")
    
    if len(data_semi.columns) == 5:
        print("✓ Semicolon-separated CSV parsed correctly (5 columns)")
    else:
        print(f"✗ Semicolon-separated CSV FAILED ({len(data_semi.columns)} columns)")
    print("=" * 70)

if __name__ == "__main__":
    test_csv_parsing_fix()
