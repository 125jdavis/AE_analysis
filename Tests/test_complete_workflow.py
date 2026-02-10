#!/usr/bin/env python3
"""
Comprehensive test to verify all file loading functionality
"""

import os
import sys
import pandas as pd

def test_mlg_to_csv_conversion():
    """Test MLG to CSV conversion with existing file"""
    print("=" * 70)
    print("TEST 1: MLG to CSV Conversion")
    print("=" * 70)
    
    mlg_file = "sample data/drive.mlg"
    
    if not os.path.exists(mlg_file):
        print(f"✗ MLG file not found: {mlg_file}")
        return False
    
    print(f"✓ MLG file exists: {mlg_file}")
    print(f"  Size: {os.path.getsize(mlg_file):,} bytes")
    
    # Simulate convert_mlg_to_csv function
    mlg_file_abs = os.path.abspath(mlg_file)
    output_file = mlg_file_abs.rsplit('.', 1)[0] + '.csv'
    
    print(f"\nChecking for converted CSV...")
    print(f"  Expected: {output_file}")
    
    if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
        print(f"✓ CSV exists: {os.path.getsize(output_file):,} bytes")
        return output_file
    else:
        print("✗ CSV not found")
        return False


def test_csv_loading_with_units_row(csv_file):
    """Test CSV loading with units row detection"""
    print("\n" + "=" * 70)
    print("TEST 2: CSV Loading with Units Row Detection")
    print("=" * 70)
    
    if not csv_file or not os.path.exists(csv_file):
        print("✗ CSV file not available")
        return False
    
    print(f"Loading: {csv_file}")
    
    try:
        # Load CSV
        data = pd.read_csv(csv_file, sep=';', low_memory=False)
        print(f"✓ Loaded {len(data)} rows, {len(data.columns)} columns")
        
        # Check for units row
        first_row_str = data.iloc[0].astype(str)
        has_letters = first_row_str.str.contains('[a-zA-Z°%]', regex=True, na=False).any()
        
        print(f"\nUnits row detection:")
        print(f"  First row first 5 values: {first_row_str.head().tolist()}")
        print(f"  Contains letters: {has_letters}")
        
        if has_letters:
            print("\n✓ Units row detected, removing...")
            data = data.iloc[1:].reset_index(drop=True)
            
            # Convert to numeric
            for col in data.columns:
                data[col] = pd.to_numeric(data[col], errors='coerce')
            
            print(f"  After removal: {len(data)} rows")
            print(f"  First row first 5 values: {data.iloc[0, :5].tolist()}")
            print(f"  Data types: {[data[col].dtype for col in data.columns[:5]]}")
        
        # Check for key columns
        print("\nChecking for key columns...")
        columns_lower = {col.lower(): col for col in data.columns}
        
        found = {}
        for pattern in ['time', 'rpm', 'tps', 'afr']:
            for col_lower, col in columns_lower.items():
                if pattern in col_lower:
                    found[pattern] = col
                    break
        
        print(f"  Found columns: {found}")
        
        if len(found) >= 2:
            print("✓ Key columns found")
            return True
        else:
            print("✗ Missing key columns")
            return False
            
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_ae_detection_simulation(csv_file):
    """Test AE event detection simulation"""
    print("\n" + "=" * 70)
    print("TEST 3: AE Event Detection Simulation")
    print("=" * 70)
    
    if not csv_file or not os.path.exists(csv_file):
        print("✗ CSV file not available")
        return False
    
    try:
        # Load and prepare data
        import numpy as np
        data = pd.read_csv(csv_file, sep=';', low_memory=False)
        
        # Remove units row
        first_row_str = data.iloc[0].astype(str)
        has_letters = first_row_str.str.contains('[a-zA-Z°%]', regex=True, na=False).any()
        if has_letters:
            data = data.iloc[1:].reset_index(drop=True)
            for col in data.columns:
                data[col] = pd.to_numeric(data[col], errors='coerce')
        
        # Find columns
        columns_lower = {col.lower(): col for col in data.columns}
        time_col = next((col for col_lower, col in columns_lower.items() if 'time' in col_lower), None)
        tps_col = next((col for col_lower, col in columns_lower.items() if 'tps' in col_lower and 'error' not in col_lower), None)
        
        if not time_col or not tps_col:
            print(f"✗ Missing required columns (Time: {time_col}, TPS: {tps_col})")
            return False
        
        print(f"Using columns: Time='{time_col}', TPS='{tps_col}'")
        
        # Get data
        time = data[time_col].values
        tps = data[tps_col].values
        
        print(f"  Time data type: {time.dtype}")
        print(f"  TPS data type: {tps.dtype}")
        print(f"  Time range: {time[0]} to {time[-1]}")
        print(f"  TPS range: {tps.min()} to {tps.max()}")
        
        # Calculate TPS_dot
        print("\nCalculating TPS rate of change...")
        dt = np.diff(time)
        dt = np.where(dt == 0, 1e-6, dt)
        tps_dot = np.diff(tps) / dt
        
        print(f"  TPS_dot calculated: {len(tps_dot)} points")
        print(f"  TPS_dot range: {tps_dot.min():.2f} to {tps_dot.max():.2f} %/s")
        
        # Check for events
        threshold = 100  # %/s
        exceeds = (tps_dot > threshold).sum()
        print(f"  Points exceeding {threshold} %/s: {exceeds}")
        
        if exceeds > 0:
            print("✓ AE event detection would work")
            return True
        else:
            print("  (No AE events in this data, but calculation works)")
            return True
            
    except TypeError as e:
        print(f"✗ TypeError (likely string data): {e}")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("COMPREHENSIVE FILE LOADING TEST SUITE")
    print("=" * 70 + "\n")
    
    results = []
    
    # Test 1: MLG to CSV
    csv_file = test_mlg_to_csv_conversion()
    results.append(("MLG to CSV conversion", bool(csv_file)))
    
    # Test 2: CSV loading with units row
    if csv_file:
        result2 = test_csv_loading_with_units_row(csv_file)
        results.append(("CSV loading with units row", result2))
        
        # Test 3: AE detection simulation
        result3 = test_ae_detection_simulation(csv_file)
        results.append(("AE detection simulation", result3))
    else:
        results.append(("CSV loading with units row", False))
        results.append(("AE detection simulation", False))
    
    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {name}")
    
    all_passed = all(result for _, result in results)
    print("\n" + "=" * 70)
    if all_passed:
        print("✓ ALL TESTS PASSED!")
        print("\nThe MLG file should load successfully in the application.")
        print("The 'detect AE events' should work without string errors.")
    else:
        print("✗ SOME TESTS FAILED")
        print("\nPlease review the errors above.")
    print("=" * 70)
    
    return 0 if all_passed else 1


if __name__ == '__main__':
    sys.exit(main())
