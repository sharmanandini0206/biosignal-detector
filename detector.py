'''
detector.py

Implementing the main AnomalyDetector class. Its takes streaming 
physiological data points, updates historical sliding metrics through
CircularDeque, and runs many clinical rules to detect anomalies in real time.

Architecture:
- Runs in O(1) or O(log k) complexity.
- No historical re scanning or sorting inside processing loops.
'''

import math

class AnomalyDetector :
    def __init__(self, window_buffer, alert_log, priority_heap) :
        # initialized the detector engine
        # window_buffer (CircularDeque) : The custom fixed size rolling window tracker
        # alert_log (AlertStack) : The custom stack tracking historical undo/redo alerts
        # priority_heap (MinHeap) : The priority queue trackering top K severe anomalies.

        self.window = window_buffer
        self.alerts = alert_log
        self.top_k = priority_heap

        self.last_peak_timestamp = Non
        self.rolling_interval_sum = 0.0
        self.peak_count = 0
    
    def process(self, value, timestamp) :
        # process a single data point from the stream
        # run varification rules, record anomalies, and update sliding buffer

        # we need a small priming window before running statistical checks
        if not self.window.is_full() :
            self.window.push_right((value, timestamp))
            return None
        mean, std_dev = self.window.get_stats()
        alert = None

        # ---------------------------------------------------------------------
        # RULE 1: PREMATURE VENTRICULAR COMPLEX (PVC / SPIKE)
        # ---------------------------------------------------------------------
        # If the current value spikes significantly above standard deviation lines
        if std_dev > 0.5 and value > (mean + 3.0 * std_dev) :
            severity = min(1.0, (value - mean) / (5.0 * std_dev if std_dev != 0 else 1))
            alert = {
                "type": "PVC",
                "value": value,
                "timestamp": timestamp,
                "severity": round(severity, 3),
                "desc": f"Voltage spike detected: {value:.2f} (μ={mean:.2f}, σ={std_dev:.2f})"
            }

        # ---------------------------------------------------------------------
        # RULE 2: LEAD-OFF / SIGNAL LOSS (DROP)
        # ---------------------------------------------------------------------
        # If the electrode wire is uncoupled, the voltage drops close to absolute zero
        elif value < 5.0 and value < (mean - 3.0 * std_dev) :
            severity = min(1.0, (mean - value) / (mean if mean != 0 else 1))
            alert = {
                "type": "LEAD_OFF",
                "value": value,
                "timestamp": timestamp,
                "severity": round(severity, 3),
                "desc": f"Electrode disconnect or massive signal drop: {value:.2f}"
            }
        
        # ---------------------------------------------------------------------
        # RULE 3: ASYSTOLE (FLATLINE)
        # ---------------------------------------------------------------------
        # If the standard deviation drops exceptionally close to zero over our window
        elif self.window.size >= 20 and std_dev < 0.15 :
            alert {
                "type": "ASYSTOLE",
                "value": value,
                "timestamp": timestamp,
                "severity": 0.950,
                "desc": "Total absence of electrical cardiac activity (flatline)."
            }
        
        # ---------------------------------------------------------------------
        # RULE 4: SINUS PAUSE / SA BLOCK (MISSED BEAT)
        # ---------------------------------------------------------------------
        # First, run a micro peak-detection check using our random access buffer
        # A peak is a point greater than its neighbors, rising above a threshold (e.g., 78)
        if self.window.size >= 3 :
            val = self.window[self.window.size - 1][0]
            mid_val = self.window[self.window.size - 2][0]
            old_val = self.window[self.window.size - 3][0]
            mid_time = self.window[self.window.size - 2][1]

            if mid_val > old_val and mid_val > prev_val and mid_val > 78.0 :
                if self.last_peak_timestamp is not None :
                    current_interval = mid_time - self.last_peak_timestamp
                    if self.peak_count > 0 :
                        avg_interval = self.rolling_interval_sum / self.peak_count
                        if current_interval > (1.45 * avg_interval) :
                            deviation_pct = (current_interval - avg_interval) / avg_interval
                            severity = min(1.0, deviation_pct, 2.0)
                            alert = {
                                "type": "SINUS_PAUSE",
                                "value": mid_val,
                                "timestamp": mid_time,
                                "severity": round(severity, 3),
                                "desc": f"Sinus Pause detected: Beat interval stretched to {current_interval:.2f}s
                            }
                        self.rolling_interval_sum += current_interval
                        self.peak_count += 1
                    else :
                        self.rolling_interval_sum += current_interval
                        self.peak_count += 1
                self.last_peak_timestamp = mid_time

        # ---------------------------------------------------------------------
        # WINDOW UPDATE & DATA LOG MAINTENANCE
        # ---------------------------------------------------------------------
        # If an anomaly fired, log it directly into our historical data tracking components
        if alert is not None :
            self.alerts.push(alert)
            self.top_k.insert(alert)
        self.window.pop_left()
        self.window.push_right((value, timestamp))

        return alert