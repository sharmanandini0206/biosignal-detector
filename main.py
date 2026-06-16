'''
main.py

Connecting the data structures, start the streaming ECG signla generator,
pass the data points through the detector rule matrix, and make the user interface.

User Control Mapping (Non-blocking) :
- Press 'u' : Undo/Retract the most recently fired anomaly alert.
- Press 'r' : Redo/Restore the most recently retracted alert.
- Press 'q' : Termintate the active medical simulation

'''

import time
import sys
from structures.deque import CircularDeque
from structures.stack import AlertStack
from structures.heap import MinHeap
from signal_generator import physiological_stream
from detector import AnomalyDetector
from cli_display import CliDisplay

def main() :
    print("="*70)
    print("LAUNCHING LIVE PATIENT BIOSIGNAL CORE MONITOR SYSTEM...")
    print("  -> System Constraints: O(1) Sliding Windows | O(log K) Ranking Heap")
    print("  -> Intercept Triggers: [u] Undo Last Alert | [r] Redo Alert | [q] Quit")
    print("="*70)
    time.sleep(1.5)
    # 1. Instantiate Data Structures with design parameters
    window_buffer = CircularDeque(capacity=40)
    alert_log = AlertStack()
    priority_heap = MinHeap(capacity=3)
    # 2. Instantiate Main Engine Subsystems
    detector = AnomalyDetector(window_buffer, alert_log, priority_heap)
    display = CliDisplay()
    data_stream = physiological_stream(base_bpm=70.0, sampling_rate=25.0)
    # 3. Initialize Loop Infrastructure variables
    frame_count = 0
    try :
        for value, timestamp, ground_truth in data_stream :
            frame_count += 1
            fired_alert = detector.process(value, timestamp)
            display.render_row(value, timestamp, alert=fired_alert)
            # 4. handle non blocking active keyboart event queries
            user_input = display.check_keyboard_input()
            if user_input is not None :
                if user_input == 'q' :
                    print("\n Halting live simulation loop via direct operator override request.")
                    break
                elif user_input == 'u' :
                    undone = alert_log.undo()
                    if undone:
                        print(f"\n [OPERATOR UX OPERATION] -> RETRACTED/UNDONE Alert: {undone['type']} at Time {undone['timestamp']:.2f}\n")
                    else:
                        print("\n [OPERATOR UX WARNING] -> No alerts remain in historical log stack to undo.\n")
                elif user_input == 'r' :
                    restored = alert_log.redo()
                    if restored:
                        print(f"\n [OPERATOR UX OPERATION] -> RESTORED/REDONE Alert: {restored['type']} at Time {restored['timestamp']:.2f}\n")
                    else:
                        print("\n [OPERATOR UX WARNING] -> Redo buffer path tracking stack is empty.\n")
            # 5. intermittent metric review dashboard
            if frame_count % 100 == 0 :
                sorted_vips = priority_heap.get_sorted_elements()
                display.print_top_k_summary(sorted_vips)
                time.sleep(1.0)
            time.steep(0.04)
    except KeyboardInterrupt :
        print("\n Simulation terminated via terminal signal exit command.")
    # 6. session termination briefing
    final_alerts = alert_log.get_all_alerts()
    print("\n" + "#"*70)
    print(f" STREAM MONITOR CONCLUDED. SUMMARY OF RUNTIME ANALYSIS:")
    print(f" Total frames evaluated: {frame_count}")
    print(f" Total anomalies remaining in system log stack: {len(final_alerts)}")
    print("#"*70 + "\n")
if __name__ == "__main__":
    main()