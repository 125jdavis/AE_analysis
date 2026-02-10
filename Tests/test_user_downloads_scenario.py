#!/usr/bin/env python3
"""
Test MLG loading from different directory (simulates user's Downloads folder scenario)
"""

import os
import sys
import shutil
import subprocess

def test_user_scenario():
    """
    Simulate user's exact scenario:
    1. File in Downloads folder (no CSV exists)
    2. Try to load the MLG file
    3. Should convert automatically
    """
    print("=" * 70)
    print("USER SCENARIO TEST: Loading MLG from Downloads-like folder")
    print("=" * 70)
    
    # Create a Downloads-like directory
    downloads_dir = "/tmp/user_downloads"
    os.makedirs(downloads_dir, exist_ok=True)
    
    # Copy MLG file (without CSV)
    source_mlg = "/home/runner/work/AE_analysis/AE_analysis/sample data/drive.mlg"
    downloads_mlg = os.path.join(downloads_dir, "drive.mlg")
    downloads_csv = os.path.join(downloads_dir, "drive.csv")
    
    # Clean up any existing files
    if os.path.exists(downloads_mlg):
        os.remove(downloads_mlg)
    if os.path.exists(downloads_csv):
        os.remove(downloads_csv)
    
    print(f"\n1. Copying MLG to Downloads folder: {downloads_dir}")
    shutil.copy(source_mlg, downloads_mlg)
    print(f"   ✓ MLG copied: {os.path.getsize(downloads_mlg):,} bytes")
    print(f"   ✗ CSV does not exist (as expected)")
    
    print(f"\n2. Simulating convert_mlg_to_csv function...")
    
    # This is exactly what the app does
    mlg_file_abs = os.path.abspath(downloads_mlg)
    output_file = mlg_file_abs.rsplit('.', 1)[0] + '.csv'
    
    print(f"   Input:  {mlg_file_abs}")
    print(f"   Output: {output_file}")
    
    # Check if CSV exists (it shouldn't)
    if os.path.exists(output_file):
        print(f"   ! CSV already exists (unexpected)")
        return False
    
    print(f"   ✓ CSV doesn't exist, will attempt conversion")
    
    # Try conversion
    print(f"\n3. Running mlg-converter...")
    try:
        result = subprocess.run(
            ['npx', 'mlg-converter', '--format=csv', mlg_file_abs],
            capture_output=True,
            text=True,
            timeout=90
        )
        
        print(f"   Return code: {result.returncode}")
        if result.stdout:
            print(f"   Stdout: {result.stdout.strip()}")
        if result.stderr and result.returncode != 0:
            print(f"   Stderr: {result.stderr.strip()}")
        
        if result.returncode == 0 and os.path.exists(output_file):
            print(f"\n4. ✓ SUCCESS: CSV created")
            print(f"   Size: {os.path.getsize(output_file):,} bytes")
            print(f"   Location: {output_file}")
            
            # Verify CSV is readable
            import pandas as pd
            df = pd.read_csv(output_file, sep=';', nrows=5, low_memory=False)
            print(f"   ✓ CSV is readable: {len(df.columns)} columns")
            
            # Clean up
            print(f"\n5. Cleaning up...")
            os.remove(downloads_mlg)
            os.remove(downloads_csv)
            os.rmdir(downloads_dir)
            print(f"   ✓ Test files removed")
            
            return True
        else:
            print(f"\n4. ✗ FAILURE: Conversion failed")
            if not os.path.exists(output_file):
                print(f"   CSV file not created")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"\n4. ✗ FAILURE: Timeout after 90 seconds")
        return False
    except FileNotFoundError:
        print(f"\n4. ✗ FAILURE: npx not found")
        print(f"   This means Node.js is not installed or not in PATH")
        return False
    except Exception as e:
        print(f"\n4. ✗ FAILURE: {e}")
        return False


def main():
    print("\n" + "=" * 70)
    print("SIMULATING USER'S EXACT SCENARIO")
    print("=" * 70)
    print("\nUser reports:")
    print("  - Loading from repo folder (with CSV) works ✓")
    print("  - Loading from Downloads (no CSV) fails ✗")
    print("\nThis test simulates the Downloads scenario...")
    print()
    
    success = test_user_scenario()
    
    print("\n" + "=" * 70)
    if success:
        print("✓ TEST PASSED!")
        print("\nThe MLG conversion works correctly from any directory.")
        print("If user still sees error, possible causes:")
        print("  1. Node.js not installed on user's system")
        print("  2. npx not in PATH when GUI app runs")
        print("  3. Network issue preventing package download")
        print("  4. Disk space or permissions issue")
    else:
        print("✗ TEST FAILED!")
        print("\nSomething is preventing MLG conversion.")
    print("=" * 70)
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
