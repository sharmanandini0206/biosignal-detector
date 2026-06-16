# 🏥 Real-Time Biosignal Event Detector & Parser

A physiological data stream processor built completely from scratch in Python. This system acts as a real-time clinical cardiac monitor, ingesting continuous ECG streams, tracking rolling window metrics, and instantaneously diagnosing physiological anomalies using optimized, custom-built data structures.

## 🚀 Core Features
* **Deterministic Streaming Architecture:** Evaluates continuous data point-by-point, perfectly mimicking low-level firmware processing a live hardware sensor feed.
* **Clinical Event Simulation:** Synthesizes periodic ECG patterns with stochastic noise and intentional, labeled clinical condition injections.
* **Low-Overhead Metric Estimation:** Tracks floating rolling variances and temporal intervals to run multi-rule diagnostic evaluations without re-scanning historical frames.
* **Non-Blocking Interrupt Engine:** Features a command-line interface that captures keyboard overrides (Undo/Redo/Quit operations) asynchronously without ever stalling the live data pipe.

---

## 🧠 Data Structures Implemented (From Scratch)

### 1. Circular Deque (`structures/deque.py`)
* **Complexity:** $O(1)$ Enqueue, $O(1)$ Dequeue, $O(1)$ Random Access via internal index wrapping arithmetic.
* **Purpose:** Manages a pre-allocated, fixed-capacity memory buffer representing the active sliding window of patient history.
* **Optimization:** Maintains a running sum and running sum-of-squares of the numerical signal. This allows the system to compute the exact mathematical mean and standard deviation in **$O(1)$ time per frame**, completely eliminating the traditional $O(N)$ overhead of scanning back through the window.

### 2. Alert Stack with Timed History (`structures/stack.py`)
* **Complexity:** $O(1)$ Push, $O(1)$ Pop / Undo.
* **Purpose:** Registers every anomaly triggered by the detector matrix. 
* **Mechanics:** Employs a dual-stack configuration (Main Alert Log + Parallel Redo Stack). If an operator flags a false positive or hits the undo key (`u`), the state is popped off history and isolated in the redo layer, allowing a user to step backward and forward through clinical actions in real time.

### 3. Capped Min-Heap / Priority Queue (`structures/heap.py`)
* **Complexity:** $O(\log K)$ Insertions/Bubbling, $O(1)$ Minimum Peek.
* **Purpose:** Acts as a real-time leaderboard filter that retains exclusively the top-$K$ *most severe* cardiac events seen during the monitoring session.
* **Mechanics:** Implements binary tree index arithmetic (`2*i + 1`, `2*i + 2`) over a flat array layout. By maintaining the least severe of the critical events at the root node, incoming frames can be compared or integrated into the top list in constant or logarithmic time, avoiding costly sorting algorithms.

---

## 🔬 Multi-Rule Diagnostic Matrix
The engine cross-references the sliding `CircularDeque` stats against four real-world clinical anomalies:
1. **PVC (Premature Ventricular Complex):** Caught when an electrical voltage spike leaps $> 3\sigma$ above the running baseline mean.
2. **LEAD_OFF (Signal Loss):** Caught when the signal undergoes an uncompensated drop straight down toward absolute zero, separating it from normal human baseline patterns.
3. **ASYSTOLE (Cardiac Flatline):** Caught when the rolling variance over a sustained period approaches zero ($o < 0.15$), identifying a lethal cessation of electrical activity.
4. **SINUS_PAUSE (SA Block):** Analyzes local maxima peak timestamps inside the array buffer. If the time interval between consecutive heartbeat peaks elongates by $> 45\%$ compared to the historical average peak interval, a missed beat state is instantly declared.

---

## 📂 System Architecture
```text
biosignal/
├── main.py                # Wires components together; manages the primary execution loop
├── signal_generator.py    # Infinite physiological generator yielding simulated ECG feeds
├── detector.py            # Diagnostic state engine processing rule conditions
├── cli_display.py         # Handles scrolling ASCII graph and low-level OS non-blocking inputs
└── structures/
    ├── __init__.py
    ├── deque.py           # Custom CircularDeque implementation
    ├── stack.py           # Custom AlertStack with undo/redo architecture
    └── heap.py            # Custom MinHeap sorting structure
