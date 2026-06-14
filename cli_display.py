'''
cli_display.py

Sets up the streaming command line visual display interface.
Handles ANSI text color-coding, generates scrolling real time ASCII waveforms,
and uses low-level operating system modules to intercept non blocking
user keyboard events for instant Undo/Redo commands.
'''

import sys
import os

if os.name == 'nt' :
    import msvcrt
else :
    import select

class CliDisplay :
    def __init__(self) :
        # color palettes
        self.COLOR_NORMAL = "\033[0m"       # Reset text styling
        self.COLOR_PVC = "\033[93m"          # Bold Yellow
        self.COLOR_LEAD_OFF = "\033[91m"     # Bold Red
        self.COLOR_ASYSTOLE = "\033[97;41m"  # White text on Red Background
        self.COLOR_SINUS_PAUSE = "\033[95m"   # Magenta
    def generate_ascii_bar(self, value, min_val=0.0, max_val=140.0) :
        # maps a float signal value to a proportional horizontal ASCII bar
        # create a rolling visual wave inside the runnign text logs.

        #camp value within predictable boundaries
        clamped_val = max(min_val, min(max_val, value))
        # determine active character width (max 20 char wide)
        max_bars = 20
        percentage = (clamped_val - min_val) / (max_val - min_val)
        num_bars = int(percentage * max_bars)
        # build string using block characters
        # Full block: '█', Half block: '▌'
        bar_string = "█" * num_bars + "░" * (max_bars - num_bars)
        return bar_string
    
    def render_row(self, value, timestamp, alert=None) :
        # format and print a single data frame row with color coded alerts
        bar = self.generate_ascii_bar(value)
        time_str = f"{timestamp:.2f}"
        # Default row presentation
        color = self.COLOR_NORMAL
        alert_tag = ""
        # If an anomaly was caught on this frame, override color styling
        if alert is not None :
            alert_type = alert["type"]
            if alert_type == "PVC":
                color = self.COLOR_PVC
                alert_tag = f"[CRITICAL: PVC] -> {alert['desc']}"
            elif alert_type == "LEAD_OFF":
                color = self.COLOR_LEAD_OFF
                alert_tag = f"[ALERT: LEAD_OFF] -> {alert['desc']}"
            elif alert_type == "ASYSTOLE":
                color = self.COLOR_ASYSTOLE
                alert_tag = f"[EMERGENCY: ASYSTOLE] -> {alert['desc']}"
            elif alert_type == "SINUS_PAUSE":
                color = self.COLOR_SINUS_PAUSE
                alert_tag = f"[ALERT: SINUS_PAUSE] -> {alert['desc']}"
                
        print(f"{color}[Time: {time_str}] | Val: {value:6.2f} | {bar} {alert_tag}{self.COLOR_NORMAL}")
        sys.stdout.flush()
    
    def print_top_k_summary(self, sorted_alerts) :
        #print a clean summary dashboard of top-k most severe anomalies.
        print("\n" + "="*70)
        print("MEDICAL RECOGNITION REPORT: TOP INCIDENTS CAPTURED")
        print("="*70)

        if not sorted_alerts :
            print("No anomalies recorded in current session log")
        else :
            for idx, alert in enumerate(sorted_alerts, start=1) :
                print(f" {idx}. [{alert['type']}] Severity: {alert['severity']:.3%}")
                print(f"    Context: {alert['desc']}")
                print(f"    Timestamp: {alert['timestamp']:.2f}")
                print("-" * 50)
        print("="*70 + "\n")
        sys.stdout.flush()
    def check_keyboard_input(self) :
        # scans the standard input buffer to look for single key strokes
        # Windows specific non blocking logic
        if os.name == 'nt':
            if msvcrt.kbhit():
                char = msvcrt.getch().decode('utf-8', errors='ignore').lower()
                return char
                
        # Unix/POSIX (Mac & Linux) non blocking logic via polling select
        else:
            # Check if standard input (sys.stdin) is ready to read instantly (0 second timeout)
            ready_to_read, _, _ = select.select([sys.stdin], [], [], 0.0)
            if ready_to_read:
                return sys.stdin.read(1).lower()
                
        return None