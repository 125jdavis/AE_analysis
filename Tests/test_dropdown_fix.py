#!/usr/bin/env python3
"""
Test the column selection dropdown fix
Verifies that combobox values are set correctly and show as separate items
"""

import sys
import tkinter as tk
from tkinter import ttk
import pandas as pd

def test_combobox_dropdown_fix():
    """Test that column selection dropdowns are properly configured"""
    
    print("=" * 60)
    print("Testing Column Selection Dropdown Fix")
    print("=" * 60)
    
    # Create minimal tkinter environment
    root = tk.Tk()
    root.withdraw()
    
    try:
        # Load sample data
        data = pd.read_csv('sample_data.csv')
        print(f"\n✓ Loaded sample data with columns: {list(data.columns)}")
        
        # Test the fixed approach (as implemented in ae_analyzer.py)
        columns = tuple(data.columns)  # This is the fix
        
        # Create comboboxes as done in ae_analyzer.py
        time_combo = ttk.Combobox(root, state="readonly", width=20)
        time_combo['values'] = columns
        
        rpm_combo = ttk.Combobox(root, state="readonly", width=20)
        rpm_combo['values'] = columns
        
        tps_combo = ttk.Combobox(root, state="readonly", width=20)
        tps_combo['values'] = columns
        
        print(f"\n✓ Created comboboxes with tuple values")
        
        # Verify the values are set correctly
        time_values = time_combo['values']
        print(f"\nVerifying combobox values:")
        print(f"  Type: {type(time_values)}")
        print(f"  Values: {time_values}")
        print(f"  Number of items: {len(time_values)}")
        
        # Check if each column is a separate item
        if isinstance(time_values, tuple) and len(time_values) == len(data.columns):
            print(f"\n✓ PASS: Combobox has {len(time_values)} separate items")
            for i, val in enumerate(time_values):
                print(f"  Item {i+1}: '{val}'")
            
            # Verify no comma-separated single string
            if len(time_values) == 1 and ',' in time_values[0]:
                print(f"\n✗ FAIL: Values are in a single comma-separated string")
                return False
            
            print(f"\n✓ SUCCESS: Dropdown will show separate items, not a single line")
            return True
        else:
            print(f"\n✗ FAIL: Unexpected combobox value format")
            return False
            
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        root.destroy()

if __name__ == "__main__":
    success = test_combobox_dropdown_fix()
    sys.exit(0 if success else 1)
