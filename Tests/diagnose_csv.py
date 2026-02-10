#!/usr/bin/env python3
"""
Diagnostic script to debug why dropdown shows comma-separated values
This will help us understand what's happening when CSV is loaded
"""

import pandas as pd
import tkinter as tk
from tkinter import ttk

def diagnose_csv_loading():
    """Diagnose what happens when we load the CSV"""
    
    print("=" * 70)
    print("DIAGNOSTIC: CSV Loading and Column Handling")
    print("=" * 70)
    
    # Load CSV the same way ae_analyzer does
    filename = 'sample_data.csv'
    
    # Try with semicolon first (as ae_analyzer does)
    print("\n1. Trying to read with sep=';'...")
    try:
        data1 = pd.read_csv(filename, sep=';')
        print(f"   SUCCESS with semicolon separator")
        print(f"   Shape: {data1.shape}")
        print(f"   Columns: {list(data1.columns)}")
        print(f"   Column types: {[type(col) for col in data1.columns]}")
        print(f"   First column: {repr(data1.columns[0])}")
    except Exception as e:
        print(f"   FAILED: {e}")
        data1 = None
    
    # Try with comma (fallback)
    print("\n2. Trying to read with sep=','...")
    try:
        data2 = pd.read_csv(filename, sep=',')
        print(f"   SUCCESS with comma separator")
        print(f"   Shape: {data2.shape}")
        print(f"   Columns: {list(data2.columns)}")
        print(f"   Column types: {[type(col) for col in data2.columns]}")
        print(f"   First column: {repr(data2.columns[0])}")
    except Exception as e:
        print(f"   FAILED: {e}")
        data2 = None
    
    # Use whichever worked (prioritizing semicolon like ae_analyzer)
    if data1 is not None and data1.shape[1] > 1:
        data = data1
        sep_used = ';'
    else:
        data = data2
        sep_used = ','
    
    print(f"\n3. Using data loaded with sep='{sep_used}'")
    print(f"   Number of columns: {len(data.columns)}")
    print(f"   Columns: {list(data.columns)}")
    
    # Now test what happens with combobox
    print("\n4. Testing Combobox values...")
    
    root = tk.Tk()
    root.withdraw()
    
    # Test direct assignment
    combo1 = ttk.Combobox(root, state="readonly")
    combo1['values'] = tuple(str(col) for col in data.columns)
    result1 = combo1['values']
    print(f"   With enhanced fix: {result1}")
    print(f"   Number of items: {len(result1)}")
    
    # Test what happens if columns is weird
    print(f"\n5. Detailed column inspection:")
    for i, col in enumerate(data.columns):
        print(f"   Column {i}: {repr(col)}")
        print(f"     Type: {type(col)}")
        print(f"     str(col): {repr(str(col))}")
        print(f"     Contains comma: {',' in str(col)}")
    
    # Check if the issue is in how auto_select_columns uses columns
    print(f"\n6. Testing auto_select_columns parameter:")
    columns_tuple = tuple(str(col) for col in data.columns)
    print(f"   columns_tuple: {columns_tuple}")
    print(f"   Type: {type(columns_tuple)}")
    print(f"   Length: {len(columns_tuple)}")
    
    # Check if passing to auto_select_columns changes anything
    columns_list = list(columns_tuple)
    print(f"   After converting to list: {columns_list}")
    
    root.destroy()
    
    print("\n" + "=" * 70)
    print("CONCLUSION:")
    if len(result1) == 5:
        print("✓ Combobox receives 5 separate items correctly")
        print("  The issue must be elsewhere in the application flow")
    else:
        print("✗ Combobox is NOT receiving separate items")
        print(f"  It received: {result1}")
    print("=" * 70)

if __name__ == "__main__":
    diagnose_csv_loading()
