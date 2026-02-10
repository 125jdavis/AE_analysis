#!/usr/bin/env python3
"""
Quick test to verify the dropdown fix works in your environment
Run this in Spyder to confirm the fix is working
"""

import tkinter as tk
from tkinter import ttk
import pandas as pd

# Create a simple test
root = tk.Tk()
root.title("Dropdown Fix Test")
root.geometry("500x300")

# Create test data (similar to your CSV)
test_data = pd.DataFrame({
    'Time': [0.0, 0.1, 0.2],
    'RPM': [1000, 1100, 1200],
    'TPS': [5.0, 6.0, 7.0],
    'PW': [2.0, 2.1, 2.2],
    'AFR': [14.7, 14.6, 14.5]
})

# Test WRONG way (what causes the issue)
frame1 = ttk.LabelFrame(root, text="❌ WRONG: tuple(df.columns)", padding=10)
frame1.pack(fill=tk.X, padx=10, pady=5)

combo_wrong = ttk.Combobox(frame1, state="readonly", width=40)
columns_wrong = tuple(test_data.columns)  # Missing str() conversion
combo_wrong['values'] = columns_wrong
combo_wrong.pack(pady=5)

result_wrong = combo_wrong['values']
ttk.Label(frame1, text=f"Result: {result_wrong}").pack()
ttk.Label(frame1, text=f"Count: {len(result_wrong)} items", 
          foreground='red' if len(result_wrong) != 5 else 'green').pack()

# Test CORRECT way (the enhanced fix)
frame2 = ttk.LabelFrame(root, text="✅ CORRECT: tuple(str(col) for col in df.columns)", padding=10)
frame2.pack(fill=tk.X, padx=10, pady=5)

combo_correct = ttk.Combobox(frame2, state="readonly", width=40)
columns_correct = tuple(str(col) for col in test_data.columns)  # With str() conversion
combo_correct['values'] = columns_correct
combo_correct.pack(pady=5)

result_correct = combo_correct['values']
ttk.Label(frame2, text=f"Result: {result_correct}").pack()
ttk.Label(frame2, text=f"Count: {len(result_correct)} items", 
          foreground='green' if len(result_correct) == 5 else 'red').pack()

# Instructions
instructions = ttk.Label(root, 
                         text="Click each dropdown above to see the difference.\n"
                              "The CORRECT version should show 5 separate items.",
                         justify=tk.CENTER, 
                         font=('Arial', 10, 'bold'))
instructions.pack(pady=10)

# Print to console for Spyder
print("=" * 60)
print("DROPDOWN FIX TEST")
print("=" * 60)
print(f"\nWRONG way - tuple(df.columns):")
print(f"  Result: {result_wrong}")
print(f"  Number of items: {len(result_wrong)}")
print(f"  Status: {'✗ BROKEN' if len(result_wrong) != 5 else '✓ OK'}")

print(f"\nCORRECT way - tuple(str(col) for col in df.columns):")
print(f"  Result: {result_correct}")
print(f"  Number of items: {len(result_correct)}")
print(f"  Status: {'✓ WORKS' if len(result_correct) == 5 else '✗ BROKEN'}")

print("\n" + "=" * 60)
if len(result_correct) == 5:
    print("✓ The enhanced fix works in your environment!")
    print("  Update your ae_analyzer.py line 159 to use:")
    print("  columns = tuple(str(col) for col in self.data.columns)")
else:
    print("✗ Issue detected - please report your:")
    print("  - Python version")
    print("  - tkinter version") 
    print("  - pandas version")
print("=" * 60)

root.mainloop()
