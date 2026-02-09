#!/usr/bin/env python3
"""
Create a demonstration plot showing the AE analyzer output
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Load sample data
data = pd.read_csv('sample_data.csv')

# Calculate TPS_dot
time = data['Time'].values
tps = data['TPS'].values
dt = np.diff(time)
dt = np.where(dt == 0, 1e-6, dt)
tps_dot = np.diff(tps) / dt
tps_dot = np.concatenate([[0], tps_dot])

# Create figure
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(12, 10))

# Detect event region
threshold = 10.0
exceeds_threshold = tps_dot > threshold
event_start_idx = np.where(exceeds_threshold)[0][0]
event_end_idx = np.where(exceeds_threshold)[0][-1]
event_time_start = time[event_start_idx]
event_time_end = time[event_end_idx]

# Plot RPM
ax1.plot(time, data['RPM'], 'b-', linewidth=2)
ax1.axvspan(event_time_start, event_time_end, alpha=0.2, color='red', label='AE Event')
ax1.set_ylabel('RPM', fontweight='bold', fontsize=12)
ax1.grid(True, alpha=0.3)
ax1.legend(loc='upper left')
ax1.set_title('Acceleration Enrichment Event Detection', fontweight='bold', fontsize=14)

# Plot TPS and TPS_dot
ax2_twin = ax2.twinx()
ax2.plot(time, tps, 'g-', linewidth=2, label='TPS')
ax2_twin.plot(time, tps_dot, 'r--', linewidth=1.5, label='TPS Rate', alpha=0.7)
ax2_twin.axhline(y=threshold, color='orange', linestyle=':', linewidth=2, label='Threshold (10 %/s)')
ax2.axvspan(event_time_start, event_time_end, alpha=0.2, color='red')
ax2.set_ylabel('TPS (%)', fontweight='bold', fontsize=12, color='g')
ax2_twin.set_ylabel('TPS Rate (%/s)', fontweight='bold', fontsize=12, color='r')
ax2.tick_params(axis='y', labelcolor='g')
ax2_twin.tick_params(axis='y', labelcolor='r')
ax2.grid(True, alpha=0.3)

# Combine legends
lines1, labels1 = ax2.get_legend_handles_labels()
lines2, labels2 = ax2_twin.get_legend_handles_labels()
ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

# Plot Pulsewidth
ax3.plot(time, data['PW'], 'm-', linewidth=2)
ax3.axvspan(event_time_start, event_time_end, alpha=0.2, color='red')
ax3.set_ylabel('Pulsewidth (ms)', fontweight='bold', fontsize=12)
ax3.grid(True, alpha=0.3)

# Plot AFR
ax4.plot(time, data['AFR'], 'c-', linewidth=2)
ax4.axvspan(event_time_start, event_time_end, alpha=0.2, color='red')
ax4.axhline(y=14.7, color='gray', linestyle='--', alpha=0.5, linewidth=2, label='Stoich (14.7)')
ax4.set_ylabel('AFR', fontweight='bold', fontsize=12)
ax4.set_xlabel('Time (s)', fontweight='bold', fontsize=12)
ax4.legend(loc='upper left')
ax4.grid(True, alpha=0.3)

# Add event info text
event_duration = event_time_end - event_time_start
max_tps_dot = np.max(tps_dot[event_start_idx:event_end_idx])
fig.text(0.5, 0.95, 
         f'Event Duration: {event_duration:.2f}s | Max TPS Rate: {max_tps_dot:.1f} %/s',
         ha='center', fontsize=11, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig('ae_event_demo.png', dpi=150, bbox_inches='tight')
print("✓ Saved demonstration plot to ae_event_demo.png")
