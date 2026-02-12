# MLG File Support - Implementation Summary

## Problem Solved ✓
The program can now successfully open .mlg files from the "sample data" folder.

## What Was Done

### 1. Improved MLG to CSV Conversion (`convert_mlg_to_csv`)

**Previous Issues:**
- 30-second timeout was too short for first-time package downloads
- No handling of pre-existing converted CSV files
- Silent failures with broad exception handling

**Solutions Implemented:**
```python
def convert_mlg_to_csv(self, mlg_file):
    # Check for existing CSV first (saves time)
    if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
        return output_file
    
    # Increased timeout to 60 seconds
    result = subprocess.run(
        ['npx', 'mlg-converter', '--format=csv', mlg_file],
        timeout=60  # Was 30
    )
    
    # Handle timeout gracefully - check if file was created anyway
    except subprocess.TimeoutExpired:
        if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
            return output_file
```

### 2. Added Units Row Detection for CSV Files

**Discovery:**
MLG-converter creates CSV files with a units row:
```csv
"Time";"RPM";"TPS";"AFR"...
"s";"RPM";"%";"AFR"...        ← Units row
0.000;0;0.000;14.7...         ← Data starts here
```

**Solution:**
Added automatic detection and removal of units rows in CSV loading:
```python
# Check if first row contains letters (units)
first_row_str = data.iloc[0].astype(str)
has_letters = first_row_str.str.contains('[a-zA-Z°%]', regex=True, na=False).any()

if has_letters:
    # Skip units row and convert to numeric
    data = data.iloc[1:].reset_index(drop=True)
    for col in data.columns:
        data[col] = pd.to_numeric(data[col], errors='coerce')
```

### 3. Created Comprehensive Tests

**Test Files Created:**
1. `Tests/test_mlg_conversion.py` - Tests MLG to CSV conversion
2. `Tests/test_mlg_endtoend.py` - Full workflow validation

**Test Results:**
```
✓ MLG file: 12,887,380 bytes
✓ Converted CSV: 20,312,801 bytes
✓ Data rows: 8,053
✓ Columns: 570
✓ All numeric columns after units removal
✓ Contains Time, RPM, TPS, AFR columns
```

## Technical Details

### MLG Conversion Process
1. Check if CSV already exists (skip conversion if yes)
2. Run `npx mlg-converter --format=csv <file.mlg>`
3. Wait up to 60 seconds (allows for package download)
4. Verify output file exists and is non-empty
5. Return path to CSV file

### CSV Loading Process
1. Load CSV with semicolon separator (MLG-converter uses `;`)
2. Check first row for letters using regex `[a-zA-Z°%]`
3. If units row detected:
   - Remove first row
   - Reset index
   - Convert all columns to numeric (with coercion)
4. Populate column dropdowns in GUI

## Files Modified

### Core Application
- `ae_analyzer.py`
  - Lines 240-272: Enhanced `convert_mlg_to_csv()` 
  - Lines 205-227: Added CSV units row detection

### Tests
- `Tests/test_mlg_conversion.py` (new)
- `Tests/test_mlg_endtoend.py` (new)

## Usage

### For Users
Just click "Load CSV/MLG/MSL File" and select the .mlg file:
1. File dialog shows .mlg files
2. App automatically converts to CSV
3. Units row automatically removed
4. Data ready for analysis

### Requirements
- Node.js with npx (for mlg-converter)
- On first run, npx downloads mlg-converter automatically
- Subsequent runs are faster (package cached)

## Sample Data

**Location:** `sample data/drive.mlg`
- Size: 12.9 MB (binary)
- Converts to: 20.3 MB (CSV)
- Contains: 8,053 data rows, 570 columns
- Includes: Time, RPM, TPS, AFR, and 566 other engine parameters

## Backward Compatibility

✓ Existing CSV files still work
✓ MSL files still work
✓ No breaking changes to any existing functionality

## Testing Verification

Run tests to verify:
```bash
python Tests/test_mlg_conversion.py   # Basic conversion test
python Tests/test_mlg_endtoend.py     # Full workflow test
```

Both should pass with "✓ ALL TESTS PASSED!" message.

## Success Criteria - ALL MET ✓

- [x] MLG file can be selected in file dialog
- [x] MLG file converts to CSV automatically
- [x] Units row is detected and removed
- [x] Data loads into application
- [x] Columns are properly recognized
- [x] Data is ready for analysis
- [x] Tests verify functionality
- [x] No breaking changes

**The .mlg file can now be successfully opened and processed!** 🎉
