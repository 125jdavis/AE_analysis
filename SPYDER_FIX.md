# QUICK FIX FOR SPYDER USERS

## Problem
Dropdown shows "Time,RPM,TPS,PW,AFR" as one line instead of 5 separate items.

## Solution
In your `ae_analyzer.py` file, find line ~156 and change:

### ❌ Current (WRONG):
```python
columns = tuple(self.data.columns)
```

### ✅ Change to (CORRECT):
```python
columns = tuple(str(col) for col in self.data.columns)
```

## Complete Section Should Be:
```python
# Populate column dropdowns
# Convert to tuple for proper tkinter Combobox display
# Using tuple() ensures columns appear as separate dropdown items
# rather than as a single comma-separated string
columns = tuple(str(col) for col in self.data.columns)
self.time_combo['values'] = columns
self.rpm_combo['values'] = columns
self.tps_combo['values'] = columns
self.pw_combo['values'] = columns
self.afr_combo['values'] = columns
```

## After Making the Change:
1. Save the file
2. **Restart Spyder** (important - clears cached modules)
3. Run your script again
4. Load a CSV file
5. Click on any dropdown - you should now see separate items!

## Test the Fix
Run `test_spyder_fix.py` in this directory to verify the fix works in your Spyder environment.

## Why This Works
The explicit `str(col)` conversion ensures each pandas column name is properly converted to a Python string before being passed to tkinter's Combobox. Without this, some tkinter/pandas version combinations may not handle the conversion correctly, especially in IDE environments like Spyder.
