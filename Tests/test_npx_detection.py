#!/usr/bin/env python3
"""
Test npx detection logic to verify it correctly identifies when Node.js is installed
"""

import subprocess
import sys

def test_npx_detection():
    """Test the npx detection logic that's used in ae_analyzer.py"""
    print("=" * 70)
    print("Testing npx Detection Logic")
    print("=" * 70)
    
    print("\n1. Checking if npx is available...")
    
    npx_available = False
    try:
        result = subprocess.run(['npx', '--version'], 
                              capture_output=True, 
                              timeout=5,
                              text=True)
        
        print(f"   Command: npx --version")
        print(f"   Return code: {result.returncode}")
        print(f"   Stdout: {result.stdout.strip()}")
        if result.stderr:
            print(f"   Stderr: {result.stderr.strip()}")
        
        # Check if npx actually succeeded (returncode 0)
        if result.returncode == 0:
            npx_available = True
            print(f"\n✓ npx IS available (returncode = 0)")
        else:
            print(f"\n✗ npx command ran but returned error code: {result.returncode}")
            
    except FileNotFoundError:
        print(f"\n✗ npx command NOT FOUND - Node.js not installed")
    except subprocess.TimeoutExpired:
        print(f"\n✗ npx --version TIMED OUT")
    except Exception as e:
        print(f"\n✗ Error checking npx: {e}")
    
    print("\n" + "=" * 70)
    print("Detection Result:")
    print("=" * 70)
    
    if npx_available:
        print("✓ Node.js IS installed and npx is working")
        print("\nThe app should show:")
        print('  "Failed to convert .mlg file to CSV."')
        print('  "Check the console output for details."')
    else:
        print("✗ Node.js NOT detected or npx not working")
        print("\nThe app should show:")
        print('  "Cannot convert .mlg files - Node.js not found."')
        print('  "Please install Node.js from https://nodejs.org/"')
    
    print("\n" + "=" * 70)
    
    return npx_available


def test_node_version():
    """Also check node version for additional info"""
    print("\n" + "=" * 70)
    print("Additional Node.js Version Info")
    print("=" * 70)
    
    for cmd in [['node', '--version'], ['npm', '--version'], ['npx', '--version']]:
        try:
            result = subprocess.run(cmd, 
                                  capture_output=True, 
                                  timeout=5,
                                  text=True)
            if result.returncode == 0:
                print(f"✓ {cmd[0]}: {result.stdout.strip()}")
            else:
                print(f"✗ {cmd[0]}: Failed (returncode {result.returncode})")
        except FileNotFoundError:
            print(f"✗ {cmd[0]}: Not found")
        except Exception as e:
            print(f"✗ {cmd[0]}: Error - {e}")


def main():
    print("\n" + "=" * 70)
    print("NPX DETECTION TEST")
    print("=" * 70)
    print("\nThis test simulates the exact logic used in ae_analyzer.py")
    print("to detect if Node.js/npx is available.\n")
    
    # Run the detection test
    npx_available = test_npx_detection()
    
    # Show additional version info
    test_node_version()
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    if npx_available:
        print("\n✓ TEST PASSED!")
        print("\nNode.js is properly detected.")
        print("If MLG conversion still fails, the error is in the conversion")
        print("itself (not in Node.js detection).")
    else:
        print("\n✗ Node.js NOT DETECTED!")
        print("\nThis explains why the error message says 'Node.js not found'.")
        print("\nPossible causes:")
        print("  1. Node.js not in PATH")
        print("  2. npx command not available")
        print("  3. Permission issues")
    
    print("\n" + "=" * 70)
    
    return 0 if npx_available else 1


if __name__ == '__main__':
    sys.exit(main())
