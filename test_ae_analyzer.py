#!/usr/bin/env python3
"""
Test script for AE Analyzer - tests core functionality without GUI
"""

import pandas as pd
import numpy as np
import sys


def test_ae_detection():
    """Test the AE event detection logic"""
    
    # Load sample data
    try:
        data = pd.read_csv('sample_data.csv')
        print("✓ Successfully loaded sample_data.csv")
        print(f"  Data shape: {data.shape}")
        print(f"  Columns: {list(data.columns)}")
    except Exception as e:
        print(f"✗ Failed to load sample data: {e}")
        return False
    
    # Calculate TPS_dot
    try:
        time = data['Time'].values
        tps = data['TPS'].values
        
        dt = np.diff(time)
        dt = np.where(dt == 0, 1e-6, dt)
        tps_dot = np.diff(tps) / dt
        tps_dot = np.concatenate([[0], tps_dot])
        
        data['TPS_dot'] = tps_dot
        print(f"✓ Successfully calculated TPS_dot")
        print(f"  Max TPS_dot: {np.max(tps_dot):.2f} %/s")
        print(f"  Min TPS_dot: {np.min(tps_dot):.2f} %/s")
    except Exception as e:
        print(f"✗ Failed to calculate TPS_dot: {e}")
        return False
    
    # Detect AE events
    try:
        threshold = 10.0  # %/s
        duration_thresh = 0.1  # seconds
        
        exceeds_threshold = tps_dot > threshold
        
        ae_events = []
        in_event = False
        event_start = 0
        
        for i in range(len(exceeds_threshold)):
            if exceeds_threshold[i] and not in_event:
                event_start = i
                in_event = True
            elif not exceeds_threshold[i] and in_event:
                event_end = i
                event_duration = time[event_end] - time[event_start]
                
                if event_duration >= duration_thresh:
                    ae_events.append({
                        'start': event_start,
                        'end': event_end,
                        'duration': event_duration,
                        'max_tps_dot': np.max(tps_dot[event_start:event_end])
                    })
                
                in_event = False
        
        # Handle event extending to end
        if in_event:
            event_end = len(exceeds_threshold) - 1
            event_duration = time[event_end] - time[event_start]
            if event_duration >= duration_thresh:
                ae_events.append({
                    'start': event_start,
                    'end': event_end,
                    'duration': event_duration,
                    'max_tps_dot': np.max(tps_dot[event_start:event_end])
                })
        
        print(f"✓ Successfully detected {len(ae_events)} AE events")
        for i, event in enumerate(ae_events):
            print(f"  Event {i+1}: duration={event['duration']:.2f}s, "
                  f"max_tps_dot={event['max_tps_dot']:.1f} %/s")
        
        if len(ae_events) == 0:
            print("  Note: No events detected with current thresholds (this is valid for some data)")
            return True  # This is a valid outcome, not a failure
            
    except Exception as e:
        print(f"✗ Failed to detect AE events: {e}")
        return False
    
    return True


def test_imports():
    """Test that all required modules can be imported"""
    try:
        import pandas
        print(f"✓ pandas {pandas.__version__}")
    except ImportError as e:
        print(f"✗ pandas not available: {e}")
        return False
    
    try:
        import numpy
        print(f"✓ numpy {numpy.__version__}")
    except ImportError as e:
        print(f"✗ numpy not available: {e}")
        return False
    
    try:
        import matplotlib
        print(f"✓ matplotlib {matplotlib.__version__}")
    except ImportError as e:
        print(f"✗ matplotlib not available: {e}")
        return False
    
    try:
        import tkinter
        print(f"✓ tkinter available")
    except ImportError as e:
        print(f"✗ tkinter not available: {e}")
        print("  Note: tkinter is required for GUI but may not be available in headless environments")
    
    return True


if __name__ == "__main__":
    print("=" * 60)
    print("AE Analyzer Test Suite")
    print("=" * 60)
    
    print("\n1. Testing imports...")
    imports_ok = test_imports()
    
    print("\n2. Testing AE detection logic...")
    detection_ok = test_ae_detection()
    
    print("\n" + "=" * 60)
    if imports_ok and detection_ok:
        print("✓ All tests passed!")
        sys.exit(0)
    else:
        print("✗ Some tests failed")
        sys.exit(1)
