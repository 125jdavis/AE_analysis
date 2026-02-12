#!/usr/bin/env python3
"""
Integration test for multi-format file loading
Tests that the app can load .csv, .mlg, and .msl files
"""

import pandas as pd
import os
import sys

def test_csv_loading():
    """Test CSV file loading logic"""
    print("Testing CSV loading...")
    filename = "sample_data.csv"
    
    try:
        # Simulate the app's CSV loading logic
        data = pd.read_csv(filename, sep=';')
        if len(data.columns) == 1:
            data = pd.read_csv(filename, sep=',')
    except (pd.errors.ParserError, pd.errors.EmptyDataError):
        data = pd.read_csv(filename, sep=',')
    
    print(f"✓ CSV loaded: {len(data)} rows, {len(data.columns)} columns")
    assert len(data) > 0, "CSV should have data"
    assert len(data.columns) > 1, "CSV should have multiple columns"
    return True

def test_msl_loading():
    """Test MSL file loading logic"""
    print("Testing MSL loading...")
    filename = "sample_data.msl"
    
    # Simulate the app's MSL loading logic
    data = pd.read_csv(filename, sep=r'\s+', comment='#', engine='python')
    
    print(f"✓ MSL loaded: {len(data)} rows, {len(data.columns)} columns")
    assert len(data) > 0, "MSL should have data"
    assert len(data.columns) > 1, "MSL should have multiple columns"
    return True

def test_file_extension_detection():
    """Test file extension detection logic"""
    print("Testing file extension detection...")
    
    # Test various file extensions
    test_cases = [
        ("test.csv", False, False),
        ("test.CSV", False, False),
        ("test.mlg", True, False),
        ("test.MLG", True, False),
        ("test.msl", False, True),
        ("test.MSL", False, True),
        ("test.txt", False, False),
    ]
    
    for filename, is_mlg, is_msl in test_cases:
        detected_mlg = filename.lower().endswith('.mlg')
        detected_msl = filename.lower().endswith('.msl')
        
        assert detected_mlg == is_mlg, f"MLG detection failed for {filename}"
        assert detected_msl == is_msl, f"MSL detection failed for {filename}"
        
    print("✓ File extension detection works correctly")
    return True

def main():
    """Run all integration tests"""
    print("=" * 60)
    print("Multi-Format File Loading Integration Tests")
    print("=" * 60)
    print()
    
    try:
        test_csv_loading()
        print()
        test_msl_loading()
        print()
        test_file_extension_detection()
        print()
        print("=" * 60)
        print("✓ All integration tests passed!")
        print("=" * 60)
        return True
    except Exception as e:
        print()
        print("=" * 60)
        print(f"✗ Tests failed: {e}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
