#!/usr/bin/env python3
"""
Comprehensive diagnostic script for MLG conversion issues
Run this to identify exactly what's preventing MLG conversion
"""

import subprocess
import os
import sys

def check_node_installation():
    """Check if Node.js, npm, and npx are installed and working"""
    print("=" * 70)
    print("1. Checking Node.js Installation")
    print("=" * 70)
    
    results = {}
    
    for cmd_name, cmd in [('node', ['node', '--version']), 
                           ('npm', ['npm', '--version']), 
                           ('npx', ['npx', '--version'])]:
        try:
            result = subprocess.run(cmd, 
                                  capture_output=True, 
                                  timeout=5,
                                  text=True)
            if result.returncode == 0:
                version = result.stdout.strip()
                print(f"✓ {cmd_name}: {version}")
                results[cmd_name] = {'available': True, 'version': version}
            else:
                print(f"✗ {cmd_name}: Command ran but failed (returncode {result.returncode})")
                results[cmd_name] = {'available': False, 'error': f'returncode {result.returncode}'}
        except FileNotFoundError:
            print(f"✗ {cmd_name}: Command not found")
            results[cmd_name] = {'available': False, 'error': 'not found'}
        except subprocess.TimeoutExpired:
            print(f"✗ {cmd_name}: Timeout")
            results[cmd_name] = {'available': False, 'error': 'timeout'}
        except Exception as e:
            print(f"✗ {cmd_name}: Error - {e}")
            results[cmd_name] = {'available': False, 'error': str(e)}
    
    return all(r.get('available', False) for r in results.values())


def check_mlg_converter():
    """Check if mlg-converter package is available"""
    print("\n" + "=" * 70)
    print("2. Checking mlg-converter Package")
    print("=" * 70)
    
    try:
        result = subprocess.run(['npx', 'mlg-converter', '--help'],
                              capture_output=True,
                              timeout=30,
                              text=True)
        
        if result.returncode == 0:
            print("✓ mlg-converter is available")
            # Show first few lines of help
            help_lines = result.stdout.split('\n')[:5]
            print("  " + "\n  ".join(help_lines))
            return True
        else:
            print(f"✗ mlg-converter failed (returncode {result.returncode})")
            if result.stderr:
                print(f"  Error: {result.stderr[:200]}")
            return False
    except subprocess.TimeoutExpired:
        print("✗ mlg-converter check timed out (may be downloading package)")
        print("  This might work on next try after package is cached")
        return False
    except FileNotFoundError:
        print("✗ npx not found (Node.js issue)")
        return False
    except Exception as e:
        print(f"✗ Error checking mlg-converter: {e}")
        return False


def test_actual_conversion():
    """Test actual MLG to CSV conversion"""
    print("\n" + "=" * 70)
    print("3. Testing Actual MLG Conversion")
    print("=" * 70)
    
    # Find a test MLG file
    test_mlg = "/home/runner/work/AE_analysis/AE_analysis/sample data/drive.mlg"
    if not os.path.exists(test_mlg):
        print("✗ Test MLG file not found")
        return False
    
    # Create temp output location
    import tempfile
    temp_dir = tempfile.mkdtemp()
    temp_mlg = os.path.join(temp_dir, "test.mlg")
    temp_csv = os.path.join(temp_dir, "test.csv")
    
    # Copy test file
    import shutil
    shutil.copy(test_mlg, temp_mlg)
    
    print(f"Input:  {temp_mlg}")
    print(f"Output: {temp_csv}")
    print("\nRunning conversion...")
    
    try:
        result = subprocess.run(
            ['npx', 'mlg-converter', '--format=csv', temp_mlg],
            capture_output=True,
            text=True,
            timeout=90
        )
        
        print(f"Return code: {result.returncode}")
        if result.stdout:
            print(f"Stdout: {result.stdout.strip()}")
        if result.stderr:
            stderr_preview = result.stderr[:500]
            print(f"Stderr: {stderr_preview}")
        
        if result.returncode == 0 and os.path.exists(temp_csv):
            csv_size = os.path.getsize(temp_csv)
            print(f"\n✓ Conversion SUCCESSFUL!")
            print(f"  CSV created: {csv_size:,} bytes")
            
            # Clean up
            os.remove(temp_mlg)
            os.remove(temp_csv)
            os.rmdir(temp_dir)
            return True
        else:
            print(f"\n✗ Conversion FAILED!")
            if not os.path.exists(temp_csv):
                print("  CSV file was not created")
            return False
            
    except subprocess.TimeoutExpired:
        print("\n✗ Conversion TIMED OUT after 90 seconds")
        # Check if file was created anyway
        if os.path.exists(temp_csv):
            print(f"  But CSV was created: {os.path.getsize(temp_csv):,} bytes")
            return True
        return False
    except Exception as e:
        print(f"\n✗ Exception during conversion: {e}")
        import traceback
        traceback.print_exc()
        return False


def check_path_environment():
    """Check PATH environment variable"""
    print("\n" + "=" * 70)
    print("4. Checking PATH Environment")
    print("=" * 70)
    
    path = os.environ.get('PATH', '')
    path_entries = path.split(os.pathsep)
    
    print(f"Total PATH entries: {len(path_entries)}")
    
    # Look for Node.js related paths
    node_paths = [p for p in path_entries if 'node' in p.lower() or 'npm' in p.lower()]
    if node_paths:
        print(f"\nNode.js related paths ({len(node_paths)}):")
        for p in node_paths:
            print(f"  {p}")
    else:
        print("\n✗ No Node.js related paths found in PATH")
    
    return bool(node_paths)


def main():
    print("\n" + "=" * 70)
    print("MLG CONVERSION DIAGNOSTIC TOOL")
    print("=" * 70)
    print("\nThis script will identify why MLG conversion might be failing.\n")
    
    results = {
        'node_installed': check_node_installation(),
        'mlg_converter': check_mlg_converter(),
        'conversion_works': test_actual_conversion(),
        'path_ok': check_path_environment()
    }
    
    print("\n" + "=" * 70)
    print("DIAGNOSTIC SUMMARY")
    print("=" * 70)
    
    print("\nResults:")
    print(f"  Node.js installed: {'✓' if results['node_installed'] else '✗'}")
    print(f"  mlg-converter available: {'✓' if results['mlg_converter'] else '✗'}")
    print(f"  Conversion works: {'✓' if results['conversion_works'] else '✗'}")
    print(f"  PATH configured: {'✓' if results['path_ok'] else '✗'}")
    
    all_ok = all(results.values())
    
    print("\n" + "=" * 70)
    if all_ok:
        print("✓ EVERYTHING LOOKS GOOD!")
        print("\nMLG conversion should work in the application.")
        print("\nIf you still see errors:")
        print("  1. Make sure you're using the latest code")
        print("  2. Restart the application")
        print("  3. Check the console output for specific errors")
    else:
        print("✗ ISSUES FOUND!")
        print("\nProblems detected:")
        if not results['node_installed']:
            print("  - Node.js not properly installed or not in PATH")
        if not results['mlg_converter']:
            print("  - mlg-converter package not available")
        if not results['conversion_works']:
            print("  - MLG to CSV conversion failing")
        if not results['path_ok']:
            print("  - Node.js not found in PATH environment variable")
        
        print("\nRecommended actions:")
        if not results['node_installed']:
            print("  1. Reinstall Node.js from https://nodejs.org/")
            print("  2. Make sure to restart your terminal/application after install")
        if not results['path_ok']:
            print("  3. Add Node.js to your PATH environment variable")
        
    print("=" * 70)
    
    return 0 if all_ok else 1


if __name__ == '__main__':
    sys.exit(main())
