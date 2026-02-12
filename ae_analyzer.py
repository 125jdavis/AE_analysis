#!/usr/bin/env python3
"""
Acceleration Enrichment (AE) Event Analyzer
Tool for analyzing acceleration enrichment events in MegaSquirt log files
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import os


class AEAnalyzer:
    """Main application for AE event analysis"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("AE Event Analyzer")
        self.root.geometry("1200x800")
        
        # Data storage
        self.data = None
        self.ae_events = []
        self.current_event_index = 0
        
        # Column names
        self.rpm_col = None
        self.tps_col = None
        self.pw_col = None
        self.afr_col = None
        self.time_col = None
        
        # Detection parameters
        self.tps_dot_threshold = tk.DoubleVar(value=10.0)  # %/s
        self.duration_threshold = tk.DoubleVar(value=0.1)  # seconds
        
        self.create_widgets()
        
    def create_widgets(self):
        """Create the GUI layout"""
        
        # Top frame for file loading and column selection
        top_frame = ttk.Frame(self.root, padding="10")
        top_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # File loading
        ttk.Button(top_frame, text="Load CSV/MLG/MSL File", 
                  command=self.load_file).grid(row=0, column=0, padx=5)
        self.file_label = ttk.Label(top_frame, text="No file loaded")
        self.file_label.grid(row=0, column=1, padx=5)
        
        # Column selection frame
        col_frame = ttk.LabelFrame(self.root, text="Column Selection", padding="10")
        col_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=10, pady=5)
        
        ttk.Label(col_frame, text="Time:").grid(row=0, column=0, sticky=tk.W)
        self.time_combo = ttk.Combobox(col_frame, state="readonly", width=20)
        self.time_combo.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(col_frame, text="RPM:").grid(row=0, column=2, sticky=tk.W)
        self.rpm_combo = ttk.Combobox(col_frame, state="readonly", width=20)
        self.rpm_combo.grid(row=0, column=3, padx=5, pady=2)
        
        ttk.Label(col_frame, text="TPS:").grid(row=1, column=0, sticky=tk.W)
        self.tps_combo = ttk.Combobox(col_frame, state="readonly", width=20)
        self.tps_combo.grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(col_frame, text="Pulsewidth:").grid(row=1, column=2, sticky=tk.W)
        self.pw_combo = ttk.Combobox(col_frame, state="readonly", width=20)
        self.pw_combo.grid(row=1, column=3, padx=5, pady=2)
        
        ttk.Label(col_frame, text="AFR:").grid(row=2, column=0, sticky=tk.W)
        self.afr_combo = ttk.Combobox(col_frame, state="readonly", width=20)
        self.afr_combo.grid(row=2, column=1, padx=5, pady=2)
        
        # Detection parameters frame
        param_frame = ttk.LabelFrame(self.root, text="Detection Parameters", padding="10")
        param_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), padx=10, pady=5)
        
        ttk.Label(param_frame, text="TPS Rate Threshold (%/s):").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(param_frame, textvariable=self.tps_dot_threshold, width=10).grid(row=0, column=1, padx=5)
        
        ttk.Label(param_frame, text="Duration Threshold (s):").grid(row=0, column=2, sticky=tk.W, padx=(20, 0))
        ttk.Entry(param_frame, textvariable=self.duration_threshold, width=10).grid(row=0, column=3, padx=5)
        
        ttk.Button(param_frame, text="Detect AE Events", 
                  command=self.detect_ae_events).grid(row=0, column=4, padx=20)
        
        # Events info frame
        events_frame = ttk.Frame(self.root, padding="10")
        events_frame.grid(row=3, column=0, sticky=(tk.W, tk.E))
        
        self.events_label = ttk.Label(events_frame, text="No events detected")
        self.events_label.grid(row=0, column=0, padx=5)
        
        ttk.Button(events_frame, text="◀ Previous Event", 
                  command=self.previous_event).grid(row=0, column=1, padx=5)
        ttk.Button(events_frame, text="Next Event ▶", 
                  command=self.next_event).grid(row=0, column=2, padx=5)
        
        # Plot frame
        plot_frame = ttk.Frame(self.root)
        plot_frame.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
        
        # Configure grid weights for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(4, weight=1)
        
        # Create matplotlib figure
        self.fig = Figure(figsize=(12, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Add toolbar
        toolbar = NavigationToolbar2Tk(self.canvas, plot_frame)
        toolbar.update()
        
    def load_file(self):
        """Load a CSV, MLG, or MSL file"""
        filename = filedialog.askopenfilename(
            title="Select log file",
            filetypes=[
                ("All supported files", "*.csv *.msl *.mlg"),
                ("CSV files", "*.csv"),
                ("MSL files", "*.msl"),
                ("MLG files", "*.mlg"),
                ("All files", "*.*")
            ]
        )
        
        if not filename:
            return
            
        try:
            # Check if it's an MLG file
            if filename.lower().endswith('.mlg'):
                # Show status message
                self.file_label.config(text="Converting MLG file...")
                self.root.update()
                
                # Try to convert MLG to CSV using mlg-converter if available
                csv_filename = self.convert_mlg_to_csv(filename)
                if csv_filename:
                    filename = csv_filename
                else:
                    # Check if npx is available to determine appropriate error message
                    import subprocess
                    npx_available = False
                    try:
                        result = subprocess.run(['npx', '--version'], 
                                              capture_output=True, 
                                              timeout=5,
                                              text=True)
                        # Check if npx actually succeeded (returncode 0)
                        if result.returncode == 0:
                            npx_available = True
                            print(f"npx is available: {result.stdout.strip()}")
                        else:
                            print(f"npx returned non-zero exit code: {result.returncode}")
                    except FileNotFoundError:
                        print(f"npx command not found - Node.js not installed")
                    except subprocess.TimeoutExpired:
                        print(f"npx --version timed out")
                    except Exception as e:
                        print(f"Error checking npx availability: {e}")
                    
                    # Show appropriate error message based on npx availability
                    if npx_available:
                        error_msg = (
                            "Failed to convert .mlg file to CSV.\n\n"
                            "The mlg-converter tool encountered an error. "
                            "Check the console output for details.\n\n"
                            "You can manually convert using:\n"
                            "npx mlg-converter --format=csv yourfile.mlg"
                        )
                    else:
                        error_msg = (
                            "Cannot convert .mlg files - Node.js not found.\n\n"
                            "Please install Node.js from https://nodejs.org/\n\n"
                            "Then the app will automatically convert .mlg files.\n\n"
                            "Alternatively, you can manually convert using:\n"
                            "1. Install: npm install -g mlg-converter\n"
                            "2. Convert: npx mlg-converter --format=csv yourfile.mlg\n"
                            "3. Load the resulting CSV file"
                        )
                    self.file_label.config(text="No file loaded")
                    messagebox.showerror("MLG Conversion Failed", error_msg)
                    return
            
            # Check if it's an MSL file (tab-separated or space-separated)
            if filename.lower().endswith('.msl'):
                # MSL files can be tab-separated (modern MegaSquirt format) or space-separated (older style)
                # Modern format has quoted metadata headers, column names, units row, then data:
                # "MS3 Format 0568.11E..."
                # "Capture Date: ..."
                # Time	RPM	TPS...  (column names)
                # s	RPM	%...      (units row)
                # 0.00	1000	10.0... (data)
                
                # Read file to detect format and count header lines
                with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                
                # Detect if file uses tabs (modern format) or spaces (older format)
                # Check non-header lines for tabs
                has_tabs = False
                for line in lines[:10]:
                    stripped = line.strip()
                    if stripped and not stripped.startswith(('"', '#')):
                        if '\t' in line:
                            has_tabs = True
                            break
                
                if has_tabs:
                    # Tab-separated format (modern MegaSquirt)
                    # Count lines starting with quotes or # (metadata headers)
                    skip_count = 0
                    for line in lines:
                        stripped = line.strip()
                        if stripped.startswith('"') or stripped.startswith('#'):
                            skip_count += 1
                        else:
                            break
                    
                    # Read with column names as header
                    self.data = pd.read_csv(filename, sep='\t', skiprows=skip_count, header=0,
                                           engine='python', encoding='utf-8', encoding_errors='ignore')
                    
                    # Check if first row is units row (contains letters/symbols) and skip it
                    if len(self.data) > 0:
                        first_row_str = self.data.iloc[0].astype(str)
                        has_letters = first_row_str.str.contains('[a-zA-Z°%]', regex=True, na=False).any()
                        if has_letters:
                            self.data = self.data.iloc[1:].reset_index(drop=True)
                            # Convert columns to numeric where possible
                            for col in self.data.columns:
                                self.data[col] = pd.to_numeric(self.data[col], errors='coerce')
                else:
                    # Space-separated format (older style, backward compatibility)
                    self.data = pd.read_csv(filename, sep=r'\s+', comment='#', engine='python')
            else:
                # Try reading with different separators
                # First try semicolon, but verify it parsed correctly (multiple columns)
                try:
                    self.data = pd.read_csv(filename, sep=';')
                    # If semicolon parse resulted in only 1 column, it's likely comma-separated
                    if len(self.data.columns) == 1:
                        self.data = pd.read_csv(filename, sep=',')
                except (pd.errors.ParserError, pd.errors.EmptyDataError):
                    # If semicolon fails, try comma
                    self.data = pd.read_csv(filename, sep=',')
                
                # Check if first row is units row (from MLG conversion or other sources)
                # Units rows contain letters/symbols like "s", "RPM", "%", "ms", etc.
                if len(self.data) > 0:
                    first_row_str = self.data.iloc[0].astype(str)
                    has_letters = first_row_str.str.contains('[a-zA-Z°%]', regex=True, na=False).any()
                    if has_letters:
                        # Skip the units row
                        self.data = self.data.iloc[1:].reset_index(drop=True)
                        # Convert columns to numeric where possible
                        for col in self.data.columns:
                            self.data[col] = pd.to_numeric(self.data[col], errors='coerce')
            
            self.file_label.config(text=f"Loaded: {os.path.basename(filename)}")
            
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
            
            # Try to auto-select common column names
            self.auto_select_columns(columns)
            
            messagebox.showinfo("Success", 
                f"File loaded successfully!\n"
                f"Rows: {len(self.data)}\n"
                f"Columns: {len(self.data.columns)}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file:\n{str(e)}")
    
    def convert_mlg_to_csv(self, mlg_file):
        """Convert MLG file to CSV using mlg-converter if available"""
        import subprocess
        
        # Get absolute path for the mlg file
        mlg_file_abs = os.path.abspath(mlg_file)
        output_file = mlg_file_abs.rsplit('.', 1)[0] + '.csv'
        
        # Check if CSV already exists (from previous conversion)
        if os.path.exists(output_file):
            # Verify it's not empty
            if os.path.getsize(output_file) > 0:
                print(f"Using existing CSV: {output_file}")
                return output_file
        
        # Try to convert using mlg-converter
        print(f"Converting MLG to CSV: {mlg_file_abs}")
        try:
            result = subprocess.run(
                ['npx', 'mlg-converter', '--format=csv', mlg_file_abs],
                capture_output=True,
                text=True,
                timeout=90  # Increased timeout for first-time package download
            )
            
            print(f"Conversion result: returncode={result.returncode}")
            if result.stdout:
                print(f"Stdout: {result.stdout.strip()}")
            if result.stderr:
                print(f"Stderr: {result.stderr.strip()}")
            
            if result.returncode == 0:
                if os.path.exists(output_file):
                    print(f"✓ Conversion successful: {output_file}")
                    return output_file
                else:
                    print(f"✗ Conversion returned success but CSV not found at: {output_file}")
            else:
                print(f"✗ Conversion failed with return code: {result.returncode}")
                
        except subprocess.TimeoutExpired:
            print(f"✗ Conversion timeout after 90 seconds")
            # Timeout - check if file was still created
            if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
                print(f"✓ File created despite timeout: {output_file}")
                return output_file
        except FileNotFoundError:
            print(f"✗ npx or mlg-converter not found. Please install Node.js and mlg-converter.")
        except (subprocess.CalledProcessError, OSError) as e:
            print(f"✗ MLG conversion error: {e}")
        
        return None
    
    def auto_select_columns(self, columns):
        """Auto-select columns based on common naming patterns"""
        # Convert to lowercase for matching
        cols_lower = {col.lower(): col for col in columns}
        
        # Time column
        for pattern in ['time', 'timestamp', 't']:
            if pattern in cols_lower:
                self.time_combo.set(cols_lower[pattern])
                break
        
        # RPM column
        for pattern in ['rpm', 'engine speed']:
            if pattern in cols_lower:
                self.rpm_combo.set(cols_lower[pattern])
                break
        
        # TPS column
        for pattern in ['tps', 'throttle', 'throttle position']:
            if pattern in cols_lower:
                self.tps_combo.set(cols_lower[pattern])
                break
        
        # Pulsewidth column
        for pattern in ['pw', 'pulsewidth', 'injector pulse', 'pw1', 'inj_pw']:
            if pattern in cols_lower:
                self.pw_combo.set(cols_lower[pattern])
                break
        
        # AFR column
        for pattern in ['afr', 'lambda', 'o2', 'air/fuel', 'air fuel']:
            if pattern in cols_lower:
                self.afr_combo.set(cols_lower[pattern])
                break
    
    def detect_ae_events(self):
        """Detect acceleration enrichment events in the loaded data"""
        if self.data is None:
            messagebox.showwarning("Warning", "Please load a file first")
            return
        
        # Get selected columns
        self.time_col = self.time_combo.get()
        self.rpm_col = self.rpm_combo.get()
        self.tps_col = self.tps_combo.get()
        self.pw_col = self.pw_combo.get()
        self.afr_col = self.afr_combo.get()
        
        if not all([self.time_col, self.tps_col]):
            messagebox.showwarning("Warning", "Please select at least Time and TPS columns")
            return
        
        try:
            # Calculate TPS rate of change (TPS_dot)
            time = self.data[self.time_col].values
            tps = self.data[self.tps_col].values
            
            # Calculate time differences
            dt = np.diff(time)
            dt = np.where(dt == 0, 1e-6, dt)  # Avoid division by zero
            
            # Calculate TPS rate of change (%/s)
            tps_dot = np.diff(tps) / dt
            tps_dot = np.concatenate([[0], tps_dot])  # Add zero at beginning to match length
            
            # Add TPS_dot to dataframe for analysis
            self.data['TPS_dot'] = tps_dot
            
            # Detect events where TPS_dot exceeds threshold
            threshold = self.tps_dot_threshold.get()
            duration_thresh = self.duration_threshold.get()
            
            # Find periods where TPS_dot exceeds threshold
            exceeds_threshold = tps_dot > threshold
            
            # Find start and end of each event
            self.ae_events = []
            in_event = False
            event_start = 0
            
            for i in range(len(exceeds_threshold)):
                if exceeds_threshold[i] and not in_event:
                    # Start of new event
                    event_start = i
                    in_event = True
                elif not exceeds_threshold[i] and in_event:
                    # End of event
                    event_end = i
                    event_duration = time[event_end] - time[event_start]
                    
                    if event_duration >= duration_thresh:
                        # Valid event - add some context before and after
                        context_samples = 50
                        start_idx = max(0, event_start - context_samples)
                        end_idx = min(len(self.data), event_end + context_samples)
                        
                        self.ae_events.append({
                            'start_idx': start_idx,
                            'end_idx': end_idx,
                            'event_start': event_start,
                            'event_end': event_end,
                            'duration': event_duration,
                            'max_tps_dot': np.max(tps_dot[event_start:event_end])
                        })
                    
                    in_event = False
            
            # Handle case where event extends to end of data
            if in_event:
                event_end = len(exceeds_threshold) - 1
                event_duration = time[event_end] - time[event_start]
                if event_duration >= duration_thresh:
                    context_samples = 50
                    start_idx = max(0, event_start - context_samples)
                    end_idx = len(self.data)
                    
                    self.ae_events.append({
                        'start_idx': start_idx,
                        'end_idx': end_idx,
                        'event_start': event_start,
                        'event_end': event_end,
                        'duration': event_duration,
                        'max_tps_dot': np.max(tps_dot[event_start:event_end])
                    })
            
            if self.ae_events:
                self.current_event_index = 0
                self.events_label.config(text=f"Found {len(self.ae_events)} AE events")
                self.plot_event(0)
                messagebox.showinfo("Success", 
                    f"Detected {len(self.ae_events)} acceleration enrichment events")
            else:
                self.events_label.config(text="No AE events detected")
                messagebox.showinfo("Info", 
                    "No acceleration enrichment events detected.\n"
                    "Try adjusting the threshold parameters.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to detect events:\n{str(e)}")
    
    def plot_event(self, event_idx):
        """Plot the data for a specific AE event"""
        if not self.ae_events or event_idx >= len(self.ae_events):
            return
        
        event = self.ae_events[event_idx]
        
        # Extract data for this event
        event_data = self.data.iloc[event['start_idx']:event['end_idx']]
        time = event_data[self.time_col].values
        
        # Clear previous plot
        self.fig.clear()
        
        # Create subplots
        ax1 = self.fig.add_subplot(4, 1, 1)
        ax2 = self.fig.add_subplot(4, 1, 2, sharex=ax1)
        ax3 = self.fig.add_subplot(4, 1, 3, sharex=ax1)
        ax4 = self.fig.add_subplot(4, 1, 4, sharex=ax1)
        
        # Highlight the actual event region
        event_time_start = self.data[self.time_col].iloc[event['event_start']]
        event_time_end = self.data[self.time_col].iloc[event['event_end']]
        
        # Plot RPM
        if self.rpm_col:
            ax1.plot(time, event_data[self.rpm_col], 'b-', linewidth=1.5)
            ax1.axvspan(event_time_start, event_time_end, alpha=0.2, color='red')
            ax1.set_ylabel('RPM', fontweight='bold')
            ax1.grid(True, alpha=0.3)
        
        # Plot TPS and TPS_dot
        ax2_twin = ax2.twinx()
        ax2.plot(time, event_data[self.tps_col], 'g-', linewidth=1.5, label='TPS')
        ax2_twin.plot(time, event_data['TPS_dot'], 'r--', linewidth=1, label='TPS Rate', alpha=0.7)
        ax2_twin.axhline(y=self.tps_dot_threshold.get(), color='orange', 
                        linestyle=':', label='Threshold')
        ax2.axvspan(event_time_start, event_time_end, alpha=0.2, color='red')
        ax2.set_ylabel('TPS (%)', fontweight='bold', color='g')
        ax2_twin.set_ylabel('TPS Rate (%/s)', fontweight='bold', color='r')
        ax2.tick_params(axis='y', labelcolor='g')
        ax2_twin.tick_params(axis='y', labelcolor='r')
        ax2.grid(True, alpha=0.3)
        
        # Combine legends
        lines1, labels1 = ax2.get_legend_handles_labels()
        lines2, labels2 = ax2_twin.get_legend_handles_labels()
        ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
        
        # Plot Pulsewidth
        if self.pw_col:
            ax3.plot(time, event_data[self.pw_col], 'm-', linewidth=1.5)
            ax3.axvspan(event_time_start, event_time_end, alpha=0.2, color='red')
            ax3.set_ylabel('Pulsewidth (ms)', fontweight='bold')
            ax3.grid(True, alpha=0.3)
        
        # Plot AFR
        if self.afr_col:
            ax4.plot(time, event_data[self.afr_col], 'c-', linewidth=1.5)
            ax4.axvspan(event_time_start, event_time_end, alpha=0.2, color='red')
            ax4.set_ylabel('AFR', fontweight='bold')
            ax4.axhline(y=14.7, color='gray', linestyle='--', alpha=0.5, label='Stoich (14.7)')
            ax4.legend(loc='upper left')
            ax4.grid(True, alpha=0.3)
        
        ax4.set_xlabel('Time (s)', fontweight='bold')
        
        # Add title
        self.fig.suptitle(
            f'AE Event {event_idx + 1} of {len(self.ae_events)} - '
            f'Duration: {event["duration"]:.2f}s, Max TPS Rate: {event["max_tps_dot"]:.1f} %/s',
            fontsize=12, fontweight='bold'
        )
        
        self.fig.tight_layout()
        self.canvas.draw()
    
    def previous_event(self):
        """Show previous AE event"""
        if not self.ae_events:
            return
        
        self.current_event_index = (self.current_event_index - 1) % len(self.ae_events)
        self.plot_event(self.current_event_index)
    
    def next_event(self):
        """Show next AE event"""
        if not self.ae_events:
            return
        
        self.current_event_index = (self.current_event_index + 1) % len(self.ae_events)
        self.plot_event(self.current_event_index)


def main():
    """Main entry point"""
    root = tk.Tk()
    app = AEAnalyzer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
