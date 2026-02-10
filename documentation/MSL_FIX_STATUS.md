# .msl and .mlg File Loading - Status Update

## Issue Summary
The user reported two errors:
1. **.msl file error**: "expected 8 fields in line 4, saw 368. Error could possibly be due to quotes being ignored when a multi-char delimiter is used."
2. **.mlg file error**: "cannot read .mlg files directly" message shown

## Root Cause Analysis

### .msl File Issue - FIXED ✓
**Problem**: The parser was using `sep=r'\s+'` (whitespace regex) which treats every space as a delimiter. Real MegaSquirt .msl files are **tab-separated**, so spaces within field values were incorrectly split into separate fields.

**Example**:
```
"MS3 Format 0568.11E: MS3 pre-1.5.2 RC 12 20200729..."
```
With `\s+`, this became 12 fields instead of 1, causing the error.

**Solution**: 
- Auto-detect tab vs space separation
- Use `sep='\t'` for tab-separated files
- Skip quoted metadata headers
- Skip units row
- Maintain backward compatibility with space-separated format

### .mlg File Issue - EXPECTED BEHAVIOR ✓
**Status**: This is working as designed. The error message correctly informs users that .mlg files require mlg-converter (Node.js tool) to convert to CSV first.

## Changes Implemented

### Updated ae_analyzer.py
```python
# Auto-detect tab vs space separation
has_tabs = any('\t' in line for line in lines[:10] 
               if line.strip() and not line.strip().startswith(('"', '#')))

if has_tabs:
    # Tab-separated format (modern MegaSquirt)
    # Skip quoted headers
    # Read with tab separator
    # Skip units row if present
else:
    # Space-separated format (backward compatibility)
    self.data = pd.read_csv(filename, sep=r'\s+', comment='#')
```

## Testing Status

### ✓ Completed Tests
1. **Tab-separated .msl** - Realistic MegaSquirt format with quoted headers and units
2. **Space-separated .msl** - Backward compatibility with older format  
3. **Core AE analyzer** - All logic tests pass

### ⏳ Pending Tests
**Need actual user files** - The provided URLs (tunes.fome.tech) are not accessible from this environment.

## Next Steps

### For User:
Please provide your .msl and .mlg files via one of these methods:

1. **Upload directly** (if supported by your interface)

2. **Share via public URL** from:
   - GitHub Gist
   - Pastebin  
   - Dropbox
   - Google Drive
   - Any other accessible hosting

3. **Paste sample content** - If files are small, paste the first 50-100 lines in chat

### For Testing:
Once files are available, I will:
1. Test parsing with actual user files
2. Verify all columns load correctly
3. Ensure data types are appropriate
4. Complete full integration testing
5. Run code review and security scan

## File Format Reference

### Modern .msl Format (Tab-separated)
```
"MS3 Format 0568.11E: MS3 pre-1.5.2 RC 12..."
"Capture Date: Mon Aug 24 15:24:33 EDT 2020"
Time	RPM	TPS	PW	AFR	MAP	CLT
s	RPM	%	ms	AFR	kPa	°F
0.00	1000	10.0	2.5	14.7	45.0	180
0.05	1050	12.0	2.6	14.6	46.0	180
```

### Key Characteristics:
- Lines 1-N: Quoted metadata headers
- Line N+1: Tab-separated column names
- Line N+2: Tab-separated units
- Lines N+3+: Tab-separated data

## Current Status: ✓ READY FOR USER FILE TESTING

The fix is implemented and tested with synthetic realistic data. 
Waiting for user to provide accessible .msl/.mlg files for final validation.
