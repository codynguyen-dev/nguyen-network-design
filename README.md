# Network Design Project – Team ____

<!-- Optional: add badges if you want -->
<!-- ![language](https://img.shields.io/badge/language-python-blue) -->

## Overview
This repository implements a UDP/TCP-based file transfer protocol across **6 phases**, progressively adding reliability 
mechanisms and performance evaluation.

## Team
| Name | Email | Primary responsibility |
|---|---|---|
| Cody Nguyen | cody_nguyen@student.uml.edu | UDP echo + RDT 1.0 file transfer |
|  |  |  |
|  |  |  |

## Demo Video (submission)
- **Private YouTube link:** *(submit via Blackboard)*  
- **Timestamped outline:** *(mm:ss → scenario)*

---

## Repository Structure (required)
Your repo must match this layout (minimum):

```
src/        # sender, receiver, protocol utilities
scripts/    # experiment runner, plotting utilities
docs/       # design documents and diagrams
results/    # CSV + plots generated from experiments
README.md
```

Optional (recommended):
- `tests/`
- `data/`
- `requirements.txt` (Python)

---

## Requirements
- Language/runtime: (Python 3.x)
- OS tested: (macOS / Windows / Linux)
- Dependencies:
  - Python: `pip install -r requirements.txt`

---

## Standard CLI Interface (required)
Your program must support these standardized flags so the TA can run and grade consistently.

### Receiver (required flags)
- `--port <int>`: UDP port to bind
- `--out <path>`: output file path to write received bytes
- `--seed <int>`: RNG seed (default: 0)
- `--log-level <debug|info|warning|error>` (default: info)

### Sender (required flags)
- `--host <ip/hostname>`: receiver host
- `--port <int>`: receiver port
- `--file <path>`: input file to send
- `--seed <int>`: RNG seed (default: 0)
- `--log-level <debug|info|warning|error>` (default: info)

### Injection flags (if required by phase)
- `--data-error-rate <float 0..1>` (default: 0)
- `--ack-error-rate <float 0..1>` (default: 0)
- `--data-loss-rate <float 0..1>` (default: 0)
- `--ack-loss-rate <float 0..1>` (default: 0)

### Timing / windowing flags (if required by phase)
- `--timeout-ms <int>` (default: 40)
- `--window-size <int>` (default: 10)

**Notes**
- “Rates” are probabilities per packet/ACK.
- Timing experiments must disable verbose logging (use `--log-level warning` or `error`).

---

## Quick Start (Run Locally)
### Start Receiver
```bash
python src/receiver.py --port 9000 --out results/received.bin --seed 0
```

### Run Sender
```bash
python src/sender.py --host 127.0.0.1 --port 9000 --file data/sample.jpg --seed 0
```

---

## Required Demo Scenarios (Current Phase)
Provide the exact commands used to demonstrate each required scenario.

### Scenario 1: UDP HELLO + ECHO (Phase 1a)
Receiver:
```bash
python src/udp_server.py --port 8000 --log-level info --seed 0
```
Sender:
```bash
python src/udp_client.py --host 127.0.0.1 --port 8000 --log-level info --seed 0
```
Expected behavior:
- The client sends "HELLO" to the UDP server
- The server echoes "HELLO" back to the client 

### Scenario 2: __________
Receiver:
```bash
python src/receiver.py --port 9000 --out results/received.bmp --seed 0 --log-level info
```
Sender:
```bash
python src/sender.py --host 127.0.0.1 --port 9000 --file data/input.bmp --seed 0 --log-level info
```
Expected behavior:
- Sender sends a BMP file over UDP
- Receiver reconstructs it correctly and writes it to the results/ folder 

## Figures / Plots (if required by phase) -> (N/A for Phase 1)
### Reproduce experiment runs
Your repo must include a script that can reproduce required sweeps and output CSV.

Example:
```bash
python scripts/run_experiments.py --phase 4 --out results/phase4.csv
```

### Generate plots
Example:
```bash
python scripts/plot_results.py --in results/phase4.csv --out results/phase4.png
```

### Results files
- `results/phaseX.csv`
- `results/phaseX.png`

---

## Known Issues / Limitations
List any limitations honestly.

- RDT 1.0 assumes a reliable channel and does not handle packet loss or corruption

---

## Academic Integrity / External Tools
Debugging tools (IDE debugger, logging) and LLMs may be used for learning and troubleshooting. Final implementation decisions and understanding are our own.
