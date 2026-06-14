'''
signal_generator.py
Implementing a synthetic physiological data stream generator.
It models an ECG baseline using a combination of periodic functions and
Gaussian noise, adding clinical anomalies with known label in between.

Architecture :
- Utilizes Python's generator pattern ('yield') to create an infinite real time stream
- Injected Anomalies: PVC (Spike), LEAD_OFF (Drop), ASYSTOLE (Flatline), and SINUS_PAUSE (Missed Beat).
'''
import math
import random
import time

def physiological_stream(base_bpm=70.0, sampling_rate=25.0) :
    '''
    Infinite generator that yields simulated ECG data points.
    Parameters: base_bpm (float) : Baseline heart rate in beats per min
                sampling_rate (float) : How many samples to generate per simulated second
    Yields: Tuple (value: float, timestamp: float, label: str). Label is NORMAL or explicit name of added anomaly.
    '''
    # Calculate angular frequency based on BPM and sampling rate
    # Beats per second = base_bpm / 60.0
    # Cycles per sample frame = (base_bpm / 60.0) / sampling_rate
    omega = (2 * math.pi * (base_bpm / 60.0)) / sampling_rate

    frame = 0
    anomaly_cooldown = 50 # prevent back to back overlapping anomalies

    while True :
        timestamp = time.time()

        # 1. Base signal: Periodic sine wave oscillating around a baseline of 70
        # Incorporate minor Gaussian noise to simulate thermal/sensor interference
        baseline_noise = random.gauss(0, 1.5)
        raw_value = 70.0 + (15.0 * math.sin(frame * omega)) + baseline_noise
        label = "NORMAL"

        # 2. Anomaly injection logic
        # If we aren't in a cooldown phase, randomly roll to inject a critical cardiac event
        if frame > anomaly_cooldown and random.random() < 0.008 :
            anomaly_choice = random.choice(['PVC', 'LEAD_OFF', 'ASYSTOLE', 'SINUS_PAUSE'])

            if anomaly_choice == 'PVC' :
                # Premature Ventricular Complex: Sudden massive upward electrical voltage jump
                raw_value += random.uniform(45.0, 60.0) 
                label = 'PVC'
                frame += 1
                yield (raw_value, timestamp, label)
            elif anomaly_choice == 'LEAD_OFF' :
                # Lead-Off / Signal Loss: A sharp plunge straight down to 0, simulating a detached wire  
                raw_value = random.uniform(0.0, 2.0)
                label = 'LEAD_OFF'
                frame += 1
                yield (raw_value, timestamp, label)
            elif anomaly_choice == 'ASYSTOLE' :
                # Asystole (Flatline): Signal immediately freezes at its current level (flatline)
                label = 'ASYSTOLE'
                flatline_duration = random.randint(25, 35)
                frozen_value = raw_value
                for _ in range(flatline_duration) :
                    timestamp = time.time()
                    yield (frozen_value, timestamp, label)
                    frame += 1
                anomaly_cooldown = frame + 50
            elif anomaly_choice == 'SINUS_PAUSE' :
                # Sinus Pause / SA Block: A temporary delay creating an elongated baseline gap
                label = 'SINUS_PAUSE'
                skipped_frames = random.randint(20, 30)
                for _ in range(skipped_frames) :
                    timestamp = time.time()
                    # Signal stays flat around the resting baseline, missing the sinus peak waves
                    resting_value = 70.0 + random.gauss(0, 0.5) 
                    yield (resting_value, timestamp, label)
                    frame += 1
                anomaly_cooldown = frame + 50
        else:
            frame += 1
            yield (raw_value, timestamp, label)