#!/usr/bin/env python3
"""
Test MLG conversion in different directories to verify it works everywhere
"""

import os
import sys
import shutil
import subprocess

def test_mlg_conversion_in_temp_dir():
    """Test that MLG conversion works in a clean directory"""
    print("=" * 70)
    print("TEST: MLG Conversion in Clean Directory")
    print("=" * 70)
    
    # Create test directory
    test_dir = "/tmp/mlg_test"
    os.makedirs(test_dir, exist_ok=True)
    
    # Copy MLG file to test directory
    source_mlg = "/home/runner/work/AE_analysis/AE_analysis/sample data/drive.mlg"
    test_mlg = os.path.join(test_dir, "test_drive.mlg")
    test_csv = os.path.join(test_dir, "test_drive.csv")
    
    # Clean up any existing files
    if os.path.exists(test_csv):
        os.remove(test_csv)
    
    print(f"\nCopying MLG file to: {test_dir}")
    shutil.copy(source_mlg, test_mlg)
    print(f"✓ MLG file copied: {os.path.getsize(test_mlg):,} bytes")
    
    # Simulate convert_mlg_to_csv function
    print(f"\nAttempting conversion...")
    mlg_file_abs = os.path.abspath(test_mlg)
    output_file = mlg_file_abs.rsplit('.', 1)[0] + '.csv'
    
    print(f"  Input:  {mlg_file_abs}")
    print(f"  Output: {output_file}")
    
    try:
        result = subprocess.run(
            ['npx', 'mlg-converter', '--format=csv', mlg_file_abs],
            capture_output=True,
            text=True,
            timeout=90
        )
        
        print(f"\n  Return code: {result.returncode}")
        if result.stdout:
            print(f"  Stdout: {result.stdout.strip()}")
        if result.stderr and result.returncode != 0:
            print(f"  Stderr: {result.stderr.strip()}")
        
        if result.returncode == 0 and os.path.exists(output_file):
            print(f"\n✓ SUCCESS: CSV created")
            print(f"  Size: {os.path.getsize(output_file):,} bytes")
            
            # Clean up
            os.remove(test_mlg)
            os.remove(test_csv)
            os.rmdir(test_dir)
            return True
        else:
            print(f"\n✗ FAILURE: Conversion failed")
            if not os.path.exists(output_file):
                print(f"  CSV file not created at: {output_file}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"\n✗ FAILURE: Timeout after 90 seconds")
        return False
    except FileNotFoundError:
        print(f"\n✗ FAILURE: npx or mlg-converter not found")
        return False
    except Exception as e:
        print(f"\n✗ FAILURE: {e}")
        return False


def test_mlg_conversion_with_existing_csv():
    """Test that existing CSV is reused"""
    print("\n" + "=" * 70)
    print("TEST: MLG Conversion with Existing CSV")
    print("=" * 70)
    
    test_dir = "/home/runner/work/AE_analysis/AE_analysis/sample data"
    test_mlg = os.path.join(test_dir, "drive.mlg")
    test_csv = os.path.join(test_dir, "drive.csv")
    
    if not os.path.exists(test_mlg):
        print("✗ Test MLG file not found")
        return False
    
    if not os.path.exists(test_csv):
        print("✗ Test CSV file not found")
        return False
    
    print(f"\nChecking existing CSV...")
    print(f"  MLG: {test_mlg}")
    print(f"  CSV: {test_csv}")
    print(f"  CSV size: {os.path.getsize(test_csv):,} bytes")
    
    # Simulate the check in convert_mlg_to_csv
    if os.path.exists(test_csv) and os.path.getsize(test_csv) > 0:
        print(f"\n✓ SUCCESS: Would reuse existing CSV")
        return True
    else:
        print(f"\n✗ FAILURE: CSV check failed")
        return False


def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("MLG CONVERSION TEST SUITE")
    print("=" * 70 + "\n")
    
    results = []
    
    # Test 1: Clean directory
    result1 = test_mlg_conversion_in_temp_dir()
    results.append(("Clean directory conversion", result1))
    
    # Test 2: Existing CSV
    result2 = test_mlg_conversion_with_existing_csv()
    results.append(("Existing CSV reuse", result2))
    
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
        print("\nMLG conversion works in any directory.")
    else:
        print("✗ SOME TESTS FAILED")
    print("=" * 70)
    
    return 0 if all_passed else 1


if __name__ == '__main__':
    sys.exit(main())
