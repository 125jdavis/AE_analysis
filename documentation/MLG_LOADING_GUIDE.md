# MLG File Loading - User Guide

## Overview

The AE Analyzer can automatically convert .mlg (MegaLogViewer binary) files to CSV format when you load them. The conversion happens seamlessly within the application.

## How It Works

When you load a .mlg file:

1. **Check for existing CSV**: The app first looks for a CSV file with the same name in the same directory
   - If found: Uses the existing CSV (fast!)
   - If not found: Proceeds to step 2

2. **Automatic conversion**: The app converts the .mlg file to CSV
   - Shows "Converting MLG file..." status message
   - Uses `mlg-converter` tool (installed automatically via npx)
   - Takes 10-30 seconds on first run (downloads package)
   - Takes 5-10 seconds on subsequent runs (package cached)
   - Creates CSV in same directory as the .mlg file

3. **Load the CSV**: The app then loads the converted CSV file

## Requirements

**Node.js** must be installed on your system for MLG conversion to work.

### Installing Node.js

**Windows:**
1. Download from https://nodejs.org/
2. Run the installer
3. Restart the AE Analyzer application

**macOS:**
```bash
brew install node
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt-get install nodejs npm

# Fedora
sudo dnf install nodejs npm
```

### Verifying Installation

Open a terminal/command prompt and run:
```bash
node --version
npx --version
```

Both should show version numbers. If not, Node.js is not properly installed.

## Troubleshooting

### "Cannot convert .mlg files - Node.js not found"

**Problem**: Node.js is not installed or not in PATH

**Solution**:
1. Install Node.js (see above)
2. Restart the AE Analyzer application
3. Try loading the .mlg file again

### "Failed to convert .mlg file to CSV"

**Problem**: The conversion tool encountered an error

**Solution**:
1. Check the console/terminal output for error details
2. Ensure you have write permissions in the file's directory
3. Ensure you have enough disk space (CSV is ~1.5x larger than MLG)
4. Try manually converting:
   ```bash
   npx mlg-converter --format=csv yourfile.mlg
   ```
5. If manual conversion works, load the resulting CSV file

### Conversion Works in Repo Folder but Not Downloads

**Problem**: This was a bug in earlier versions

**Solution**: Update to the latest version where this is fixed

**Why it happened**: 
- In repo folder: CSV already existed from previous conversion
- In Downloads: No CSV existed, so conversion was attempted
- Bug: Conversion wasn't working correctly in all directories

**Status**: ✅ FIXED in latest commits

## Performance Notes

### First Time Conversion
- Takes 10-30 seconds
- Downloads mlg-converter package (~10 MB)
- Package is cached for future use

### Subsequent Conversions
- Takes 5-10 seconds
- Uses cached package
- Speed depends on file size

### Using Existing CSV
- Instant (< 1 second)
- No conversion needed
- CSV must be in same directory with same name

## File Locations

The converted CSV file is created in the **same directory** as the .mlg file.

Example:
```
Downloads/
  ├── drive.mlg          ← Original file
  └── drive.csv          ← Created by conversion
```

## Manual Conversion (Alternative)

If automatic conversion doesn't work, you can convert manually:

```bash
# Install mlg-converter globally (one time)
npm install -g mlg-converter

# Convert your file
mlg-converter --format=csv drive.mlg

# This creates drive.csv in the same directory
```

Then load the CSV file in the AE Analyzer.

## Testing Conversion

To test if MLG conversion works on your system:

```bash
# Navigate to the test directory
cd AE_analysis/Tests

# Run the user scenario test
python test_user_downloads_scenario.py
```

This simulates loading a .mlg file from your Downloads folder (no existing CSV).

Expected output:
```
✓ TEST PASSED!
The MLG conversion works correctly from any directory.
```

## Advanced: Conversion Details

The conversion process:

1. Checks for `npx` command (Node.js package runner)
2. Runs: `npx mlg-converter --format=csv /path/to/file.mlg`
3. mlg-converter:
   - Reads the binary .mlg format
   - Extracts all sensor data
   - Creates CSV with semicolon separators
   - Includes a units row (e.g., "s", "RPM", "%")
4. App loads CSV and removes units row automatically

## Support

If you continue to have issues:

1. **Check Node.js installation**: `node --version`
2. **Check console output**: Look for detailed error messages
3. **Try manual conversion**: Use command line
4. **Check file permissions**: Ensure you can write to the directory
5. **Check disk space**: CSV files are larger than MLG files

## Recent Improvements

**Latest version includes:**
- ✅ Better error messages (shows specific failure reason)
- ✅ Visual feedback during conversion ("Converting MLG file...")
- ✅ Increased timeout (90 seconds for package download)
- ✅ Detailed console logging (for debugging)
- ✅ Fixed: Works from any directory (not just repo folder)
- ✅ Fixed: Properly handles paths with spaces

## Summary

**It should just work!** 

When you load a .mlg file:
- If CSV exists → Loads instantly
- If CSV doesn't exist → Converts automatically (requires Node.js)
- Shows status during conversion
- Shows specific error if something fails

The conversion is completely contained within the app - you don't need to manually convert files anymore (as long as Node.js is installed).
