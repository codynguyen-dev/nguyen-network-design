# Network Design Project – Phase Proposal & Design Document (Phase 1 of 5)

> **Purpose:** This document is your team’s *proposal* for how you will implement the current phase **before** you start coding.  
> Keep it clear, concrete, and lightweight.

**Team Name: INdividual**  
**Members: Cody Nguyen, cody_nguyen@student.uml.edu**   
**GitHub Repo URL (with GitHub usernames): https://github.com/codynguyen-dev/nguyen-network-design.git (codynguyen-dev)**  
**Phase: 1** 
**Submission Date: 1/26/26**  
**Version: v1**

---

## 0) Executive summary
In **5–8 sentences**, describe what you are adding/creating in *this* phase, what “done” means, and how you’ll validate it (demo + tests + figures).

---

In Phase 1(a), I will implement two UDP-based programs in Python (a UDP client and UDP server for basic message exchange) and a UDP-based file transfer tool using the RDT 1.0 protocol. The client will send a message (ex: "Hello") to the server, and the server will echo the message back to the client using UDP sockets on different port numbers. For Phase 1(b), the sender will read a file as binary data, break it into fixed size chunks, and send those data packets one at a time over UDP to the receiver. The receiver will reassemble the file by writing packet payloads in order, producing an output file that matches the original. Phase 1 will be complete when 
both parts run reliably end-end and the final received file matches the sent file perfectly. Correctness will be validated with a screen recorded demo of the required scenarios plus visible verification. 

## 1) Phase requirements
### 1.1 Demo deliverable
You will submit a **screen recording** demonstrating the required scenarios.

- **Private YouTube link:** *(fill in at submission time)*  
  - Link:
  - Timestamped outline (mm:ss → scenario name):

### 1.2 Required demo scenarios
Fill in the scenarios required by the phase spec.

| Scenario | What you will inject / configure | Expected observable behavior | What we will see in the video |
|---|---|---|---|
| 1 | Start UDP server and client on different ports, client sends "HELLO" to server | Server receives "HELLO" and echoes it back to client| Terminal shows server received message and client received echo |
| 2 | Transfer a small file (probably BMP) using RDT 1.0, payload size = 1024 bytes | Sender transmits packets one at a time, receiver reconstructs file correctly | Output successfully and visually matches the original |
| 3 | N/A |  |  |

### 1.3 Required figures / plots
Fill in the figures/plots required by the phase spec (if none, write “N/A”).

| Figure/Plot | X-axis | Y-axis | Sweep range + step | Data source (CSV/log) | Output filename |
|---|---|---|---|---|---|
| 1 | N/A |  |  |  |  |
| 2 | N/A |  |  |  |  |

---

## 2) Phase plan (company-style, lightweight)
Think of this as a short “implementation proposal” you’d write at a company.

### 2.1 Scope: what changes/additions this phase
- **New behaviors added: Phase 1(a): UDP client sends “HELLO” to UDP server; UDP server echoes back to client. Phase 1(b): Implement RDT 1.0 file transfer over UDP (split file into fixed data packets, send one packet at a time, reassemble in order).**
- **Behaviors unchanged from previous phase: N/A**
- **Out of scope (explicitly): Any loss or corruption prevention, performance experiments, timeouts and retransmissions**

### 2.2 Acceptance criteria (your checklist)
List 5–10 measurable checks that mean you’re done (examples below).
- [ ] UDP server and client start and bind to chosen ports
- [ ] Sender/receiver run with standard CLI flags
- [ ] All required scenarios demonstrated in the video
- [ ] Server and client demonstrate two-way communication
- [ ] File transfer splits file into fixed-size packets (1024 bytes per payload)
- [ ] REceiver assemblex file packets in correct order and outputs correct file
- [ ] Output file matches input file (byte-for-byte)
- [ ] Figures/plots generated and saved under `results/`
- [ ] Re-run is reproducible using the same seed

### 2.3 Work breakdown (high-level; Person X will work on A, Person Y will work on B...)
- Workstream A: Phase 1(a) UDP echo client/server 
- Workstream B: Phase 1(b) packet format + packet encode/decode
- Workstream C: Phase 1(b) sender/receiver logic + reassembley
- Workstream D: DESIGN DOC + README + demo commands 

---

## 3) Architecture + state diagrams
Your phase specs likely include a reference state diagram. **You should build on it across phases.**

### 3.1 How to evolve the provided state diagram
For each phase:
1. **Start from the current phase diagram** (sender + receiver).
2. **Mark specifics**:
   - new states,
   - new transitions,
   - updated transition conditions (timeouts, corruption checks, window slide rules).
3. Keep both:
   - **“Previous phase diagram”** (for comparison) and
   - **“Current phase diagram”** (what you will implement in more detail).

> Tip: In your PDF submission, include diagrams as images. In Markdown, you can include ASCII diagrams or link to images in `docs/figures/`.

### 3.2 Component responsibilities
- **Sender**
  - responsibilities: reads input file bytes, packetizes file into fixed-size payload chunks (1024B target), constructs RDT 1.0 “packets”, and sends each packet via UDP to receiver (one at a time)
- **Receiver**
  - responsibilities: listens on UDP port, can echo messages, receives packet bytes, and extracts payload and writes to output file in order
- **Shared modules/utilities**
  - packet encode/decode: packets into bytes, parse bytes back into original data
  - checksum: verify data integrity
  - logging/timing: basic printing/logging for debugging
  - CLI/config parsing: parse --host, --port, --file, --out

### 3.3 Message flow overview
Add a simple diagram (box + arrows is fine, you're also welcome to use software with screenshots).

Phase 1(a) message flow:

[Client]  ---- "HELLO" ---->  [Server]
[Client]  <--- "HELLO"  ----  [Server] (echo)

Phase 1(b) file transfer flow: 

[file bytes] -> Sender -> UDP -> Receiver -> [output file bytes]


## 4) Packet format (high-level spec)
Define your on-the-wire format **unambiguously**.

### 4.1 Packet types
List the packet types you will send:
- Data packet
- (Optional) end-of-transfer marker / metadata packet

### 4.2 Header fields (this is the “field table”)
**What this means:** you must specify the *exact* fields in each packet header and their meaning.  
This ensures everyone can encode/decode packets consistently.

| Field | Size (bytes/bits) | Type | Description | Notes |
|---|---:|---|---|---|
| seq |  |  | sequence number |  |
| len |  |  | payload length | last packet may be smaller |
| payload | ≤ ~1024B | bytes | file chunk | binary-safe |

---

## 5) Data structures + module map
This section prevents “random globals everywhere” and helps keep code maintainable.

### 5.1 Key data structures
List the core structures you will store in memory.

Sender:
- seq_num (int): increments for every packet
- payload_size (int): fixed at 1024 bytes

Receiver:
- expected_seq (int): next expected sequence number
- output_file_handle: file opened in write-binary mode

invariants: 
- Packets are written in ascending seq order
- Each data packet’s payload length equals the len field
- Receiver writes only len bytes for the final packet


### 5.2 Module map + dependencies
Show how modules connect.

Minimum expected modules (names may vary):
- `src/udp_client.*`
- `src/udp_server.*`
- `src/sender.*`
- `src/receiver.*`
- `src/packet.*` (encode/decode)
- `src/checksum.*`
- `scripts/run_experiments.*` (if applicable)
- `scripts/plot_results.*` (if applicable)

Provide a simple dependency sketch:
---

udp_client -> socket
udp_server -> socket

sender -> socket, packet
receiver -> socket, packet
packet -> struct


## 6) Protocol logic (high-level spec before implementation)
This section is your “engineering spec” that you implement against. Keep it precise but not code-heavy.

### 6.1 Sender behavior
Describe behavior as steps or a state machine:
- when packets are sent
- when ACKs are processed
- retransmission rules
- termination conditions
- (if applicable) window advance rules

**Sender pseudocode (recommended):**
```text
initialize state
while not done:
  send/queue packets according to phase rules
  wait for ACK/event
  if ACK received:
    validate (checksum/seq)
    update state (advance, ignore duplicate, etc.)
  if timeout/event:
    retransmit according to phase rules
```



### 6.2 Receiver behavior
Describe receiver rules:
- accept/discard conditions
- ACK rules
- duplicate/out-of-order handling
- file write rules (safe and deterministic)

**Receiver pseudocode (recommended):**
```text
on packet receive:
  if corrupt: discard; respond according to phase rules
  else if expected: accept; write/buffer; ACK
  else: handle duplicate/out-of-order according to phase rules
```

### 6.3 Error/loss injection spec (if required by phase) -> (N/A for Phase 1)
If the phase requires injection, state:
- where injection occurs in the pipeline (exact point)
- probability model and RNG seed usage
- what is injected (bit flip vs drop)
- how you ensure repeatability

---

## 7) Experiments + metrics plan (required if phase requires figures/plots) -> (N/A For Phase 1)
### 7.1 Measurement definition
Define completion time precisely:
- start moment:
- stop moment:

State how you will avoid measurement distortion:
- disable verbose printing/logging during timing runs
- run multiple trials if required

### 7.2 Output artifacts
- CSV schema (columns):
- plot filenames:
- where outputs are stored (`results/`):

---

## 8) Edge cases + test plan
This replaces “risks” with what actually matters for correctness.

### 8.1 Edge cases you expect
List the top edge cases you will explicitly test.

| Edge case | Why it matters | Expected behavior |
|---|---|---|
| last packet smaller than payload size | correct file reconstruction | receiver writes exact bytes |
| duplicate packets/ACKs | protocol correctness | ignored or re-ACKed |
| corrupted header | checksum coverage | drop / request retransmit |
| termination marker handling | clean shutdown | no deadlocks |

### 8.2 Tests you will write because of these edge cases
List concrete tests (unit/integration) that map to the edge cases.

- Unit tests (examples):
  - checksum correctness on known inputs
  - packet encode/decode round-trip
- Integration tests (examples):
  - send file and verify output hash matches input
  - run scenario injection and confirm behavior

### 8.3 Test artifacts
State what artifacts you will produce:
- console logs (minimal)
- where tests live (`tests/` optional, or `scripts/`)

---

## 9) Repo structure + reproducibility
Your repo must contain at minimum:

```
src/
scripts/
docs/
results/
README.md
```

State where phase artifacts live:
- Design docs: `docs/`
- Figures/plots + CSV: `results/`
- Any helper scripts: `scripts/`

---

## 10) Team plan, ownership, and milestones
### 10.1 Task ownership
| Task | Owner | Target date | Definition of done |
|---|---|---|---|
| Packet format + encode/decode |  |  |  |
| Sender logic |  |  |  |
| Receiver logic |  |  |  |
| Injection (if required) |  |  |  |
| Figures/plots (if required) |  |  |  |
| README + reproducibility |  |  |  |

### 10.2 Milestones (keep it realistic)
- Milestone 1:
- Milestone 2:
- Milestone 3:

---

## Appendix (optional)
