# Adaptive Packet Sizing Using Packet Loss

**CSC 466**

## Project Overview

This project investigates whether packet-loss observations can be used to select more efficient packet sizes to improve network goodput.

Datagram Packetization Layer Path MTU Discovery (DPLPMTUD) is used to determine the maximum usable packet size along a network path. However, the largest usable packet size may not always provide the highest goodput if larger packets experience higher loss probabilities.

To investigate this, I am developing a proposed packet-sizing mechanism called **POTU (Path Optimal Transmission Unit)**. POTU estimates packet-loss probabilities for different packet sizes and uses these observations to select a packet size expected to improve goodput.

QUIC and DPLPMTUD provide the motivation for this project, but the current scope is to evaluate POTU through a standalone Python-based simulation under controlled network conditions. The project does not implement POTU directly within QUIC.

## Project Structure

```text
Adaptive-Packet-Sizing-Using-Packet-Loss/
├── .vscode/
│   └── settings.json
├── Simulation/
│   ├── network.py
│   ├── potu.py
│   ├── run_simulation.py
│   ├── test_network.py
│   └── test_potu.py
├── .gitignore
├── PROJECT_LOG.md
└── README.md
```

### Simulation Files

| File | Description |
|---|---|
| `network.py` | Implements the simulated network, including bandwidth, packet overhead, packet-loss probabilities, and transmission outcomes. |
| `potu.py` | Implements POTU's packet-loss estimation, exploration, expected-goodput calculations, and packet-size selection. |
| `run_simulation.py` | Runs the experiments, compares POTU with the fixed maximum-size baseline, and reports goodput results. |
| `test_network.py` | Contains unit tests for the simulated network. |
| `test_potu.py` | Contains unit tests for POTU's behaviour. |

The `.vscode/` directory contains workspace-specific VS Code settings, while `.gitignore` specifies files that Git should exclude from version control.

## Current Simulation

The simulation models a network with configurable bandwidth, packet overhead, and packet-loss probabilities for different packet sizes.

POTU initially explores the available packet sizes by transmitting packets and recording whether they are successfully delivered. It uses these observations to estimate the loss probability and expected goodput of each candidate size.

Once sufficient observations have been collected, POTU selects a packet size if its estimated goodput exceeds that of the current size by a configurable improvement threshold.

The simulation compares POTU against a baseline that always transmits at the maximum permitted packet size.

The simulation also supports sequential and interleaved exploration strategies, alternating periods of network congestion, and changes in packet-loss probabilities. POTU can repeat its exploration process following a simulated network path change to select a new packet size based on updated observations.

### Initial Experimental Configuration (Baseline Comparison)

| Parameter | Value |
|---|---|
| Candidate packet sizes | 1200, 1300, 1400, 1492, 1500 bytes |
| Packet-loss probabilities | 0.1%, 0.2%, 0.5%, 1%, 3% |
| Network bandwidth | 10 Mbps |
| Packet overhead | 50 bytes |
| Exploration samples | 100 per packet size |
| Improvement threshold | 0.5% |
| Post-exploration transmissions | 10,000 packets |
| Trials | 100 |

These packet-loss probabilities are hypothetical and are used to investigate scenarios where larger packets experience higher loss rates.

## Running the Simulation

The simulation uses Python and does not currently require any third-party Python packages.

From the repository's root directory, run:

```bash
python Simulation/run_simulation.py
```

To run the unit tests:

```bash
python -m unittest discover -s Simulation -p "test_*.py"
```

Depending on your Python installation, you may need to use `py` instead of `python` on Windows.

## Preliminary Results

In the initial experiment, POTU achieved an average steady-state goodput improvement of approximately **1.98%** and an average overall improvement of approximately **1.97%** compared with the fixed maximum-size baseline.

These results were obtained across 100 trials using different random seeds.

Although the theoretical optimal packet size under the initial loss probabilities is 1300 bytes, POTU does not consistently select this size. This highlights the importance of investigating exploration sample size and the reliability of packet-loss estimates.

These results are preliminary and apply only to the assumed network conditions.

Additional experiments were conducted using randomly generated packet-loss probabilities. Across 100 trials using one randomly generated loss profile, POTU achieved an average goodput improvement of approximately **0.59%** compared with the fixed maximum-size baseline.

Sequential and interleaved exploration strategies were also compared under simulated periods of congestion. Neither strategy consistently outperformed the other across the tested conditions. Increasing the number of exploration samples generally improved the reliability of packet-size selection, although the results varied between configurations.

To investigate adaptation to changing network conditions, a controlled path-change experiment was conducted across 1,000 random seeds. Following a change in packet-loss probabilities, POTU selected a smaller packet size in **987 of 1,000 trials (98.7%)** and selected the theoretical goodput-optimal size of 1300 bytes in **680 trials (68.0%)**.

These results are preliminary and depend on the simulated network conditions.

## Simulation Scope

The current simulation uses a simplified goodput model to isolate the relationship between packet size, packet loss, and transmission efficiency.

QUIC and DPLPMTUD provide the motivation for this project, but POTU is currently evaluated as a standalone packet-size selection mechanism rather than as part of an existing transport protocol.

The simulation does not model the complete QUIC protocol, including retransmissions and congestion control. Although POTU can repeat its exploration process following a simulated change in network conditions, re-exploration is currently triggered explicitly rather than automatically.

The purpose of the simulation is to investigate the conditions under which adaptive packet sizing may improve goodput, rather than to demonstrate real-world QUIC performance.

## Project Logbook

A chronological record of the project's research, design decisions, implementation, and experimental findings is maintained in the [Project Logbook](PROJECT_LOG.md).

## Reference

Rust, S., Petto, J., & Scheuermann, B. (2025). *On the Correlation Between Packet Size and Packet Loss on the Internet*. IEEE/IFIP Network Operations and Management Symposium (NOMS)