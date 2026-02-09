# AE_analysis

Tool for analyzing acceleration enrichment (AE) events in MegaSquirt log files.

## Features

- Load MegaLog (.mlg) or CSV files
- Automatically detect acceleration enrichment events based on TPS rate of change
- Select specific data columns (RPM, TPS, Pulsewidth, AFR)
- Configurable detection thresholds
- Interactive visualization of each AE event
- Navigate between detected events

## Installation

1. Clone the repository:
```bash
git clone https://github.com/125jdavis/AE_analysis.git
cd AE_analysis
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) For .mlg file support, install Node.js and mlg-converter:
```bash
npm install -g mlg-converter
```

## Usage

### Running the Tool

```bash
python ae_analyzer.py
```

### Loading Files

1. Click "Load CSV/MLG File" button
2. Select your log file:
   - **CSV files**: Supported directly
   - **MLG files**: Will attempt automatic conversion if mlg-converter is installed
   - If automatic conversion fails, manually convert: `npx mlg-converter --format=csv yourfile.mlg`

### Analyzing Data

1. **Select Columns**: Choose the appropriate columns for:
   - Time
   - RPM
   - TPS (Throttle Position Sensor)
   - Pulsewidth (Injector pulsewidth)
   - AFR (Air/Fuel Ratio)
   
   The tool will attempt to auto-select columns based on common naming patterns.

2. **Configure Detection Parameters**:
   - **TPS Rate Threshold**: Minimum rate of TPS change (in %/s) to trigger an event
   - **Duration Threshold**: Minimum duration (in seconds) for a valid event

3. **Detect Events**: Click "Detect AE Events" to analyze the data

4. **View Results**: 
   - Navigate through detected events using "Previous Event" and "Next Event" buttons
   - Each event shows:
     - RPM profile
     - TPS and TPS rate of change
     - Injector pulsewidth
     - Air/Fuel Ratio
   - Red shaded regions indicate the actual AE event period

## Sample Data

A sample CSV file (`sample_data.csv`) is included for testing the tool.

## How It Works

The tool identifies acceleration enrichment events by:

1. Calculating the rate of change of TPS (TPS_dot) over time
2. Finding periods where TPS_dot exceeds the configured threshold
3. Filtering events by minimum duration
4. Displaying the data with context before and after each event

## Requirements

- Python 3.6+
- pandas
- numpy
- matplotlib
- tkinter (usually included with Python)

## File Format Support

### CSV Format
CSV files should have a header row with column names. The tool supports both comma (`,`) and semicolon (`;`) separators.

Example:
```csv
Time,RPM,TPS,PW,AFR
0.00,1000,5.2,2.1,14.7
0.05,1020,5.5,2.1,14.6
...
```

### MLG Format
MLG (MegaLog) files are binary log files from MegaSquirt ECUs. The tool can:
- Automatically convert them using mlg-converter (if installed)
- Guide you to manually convert them to CSV format

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is open source and available under the MIT License.
