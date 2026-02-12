#!/usr/bin/env python3
"""
Integration test - Load CSV through ae_analyzer and verify dropdowns
This simulates what the user does in Spyder
"""

import sys
import os
sys.path.insert(0, '/home/runner/work/AE_analysis/AE_analysis')
os.environ['DISPLAY'] = ':99'

import tkinter as tk
from ae_analyzer import AEAnalyzer
import pandas as pd

def test_csv_loading_through_gui():
    """Test loading CSV through the actual GUI application"""
    
    print("=" * 70)
    print("INTEGRATION TEST: CSV Loading Through GUI")
    print("=" * 70)
    
    root = tk.Tk()
    app = AEAnalyzer(root)
    
    try:
        # Simulate what load_file() does
        filename = '/home/runner/work/AE_analysis/AE_analysis/sample_data.csv'
        
        print(f"\n1. Loading file: {os.path.basename(filename)}")
        
        # This is the FIXED CSV loading logic from ae_analyzer.py
        try:
            app.data = pd.read_csv(filename, sep=';')
            print(f"   Read with sep=';': {len(app.data.columns)} columns")
            
            # If semicolon parse resulted in only 1 column, it's likely comma-separated
            if len(app.data.columns) == 1:
                print(f"   Only 1 column found, retrying with comma...")
                app.data = pd.read_csv(filename, sep=',')
                print(f"   Read with sep=',': {len(app.data.columns)} columns")
        except (pd.errors.ParserError, pd.errors.EmptyDataError):
            app.data = pd.read_csv(filename, sep=',')
            print(f"   Read with sep=',': {len(app.data.columns)} columns")
        
        print(f"\n2. Data loaded:")
        print(f"   Columns: {list(app.data.columns)}")
        print(f"   Shape: {app.data.shape}")
        
        # Set file label
        app.file_label.config(text=f"Loaded: {os.path.basename(filename)}")
        
        # Populate column dropdowns (using the fixed code)
        print(f"\n3. Populating dropdowns...")
        columns = tuple(str(col) for col in app.data.columns)
        print(f"   columns tuple: {columns}")
        print(f"   Type: {type(columns)}")
        print(f"   Length: {len(columns)}")
        
        app.time_combo['values'] = columns
        app.rpm_combo['values'] = columns
        app.tps_combo['values'] = columns
        app.pw_combo['values'] = columns
        app.afr_combo['values'] = columns
        
        # Verify what's in the comboboxes
        print(f"\n4. Verifying combobox values:")
        time_values = app.time_combo['values']
        rpm_values = app.rpm_combo['values']
        tps_values = app.tps_combo['values']
        
        print(f"   time_combo['values']: {time_values}")
        print(f"   Number of items: {len(time_values)}")
        
        # Try auto-select
        app.auto_select_columns(columns)
        
        print(f"\n5. After auto-select:")
        print(f"   time_combo.get(): '{app.time_combo.get()}'")
        print(f"   rpm_combo.get(): '{app.rpm_combo.get()}'")
        print(f"   tps_combo.get(): '{app.tps_combo.get()}'")
        
        # Close the window
        root.after(100, root.quit)
        root.mainloop()
        
        # Verify results
        print("\n" + "=" * 70)
        print("TEST RESULTS:")
        
        success = True
        if len(app.data.columns) == 5:
            print("✓ CSV parsed correctly: 5 columns")
        else:
            print(f"✗ CSV parsing FAILED: {len(app.data.columns)} columns")
            success = False
        
        if len(time_values) == 5:
            print("✓ Combobox has 5 separate items")
        else:
            print(f"✗ Combobox FAILED: {len(time_values)} items")
            print(f"  Values: {time_values}")
            success = False
        
        if app.tps_combo.get() == 'TPS':
            print("✓ Auto-select worked correctly")
        else:
            print(f"✗ Auto-select FAILED: got '{app.tps_combo.get()}'")
            success = False
        
        print("=" * 70)
        
        if success:
            print("\n✓✓✓ ALL TESTS PASSED ✓✓✓")
            print("The dropdown should now show separate items!")
        else:
            print("\n✗✗✗ SOME TESTS FAILED ✗✗✗")
        
        return success
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        root.destroy()

if __name__ == "__main__":
    success = test_csv_loading_through_gui()
    sys.exit(0 if success else 1)
