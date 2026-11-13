# Project Logbook

## Entry 1 — Initial Research and Project Proposal

Investigated the possibility of improving QUIC goodput by selecting packet sizes based on observed packet loss rather than always using the maximum viable packet size.

Reviewed DPLPMTUD and identified that, while it determines the maximum usable packet size, this may not always be the most efficient size when packet-loss probability depends on packet size.

Developed the initial concept for POTU (Path Optimal Transmission Unit), a proposed mechanism that estimates packet-loss probabilities and uses these estimates to select a packet size expected to improve goodput.

Completed and submitted the initial project proposal.

## Entry 2 — Simulation Design

Decided to use a Python-based simulation rather than implementing POTU directly within QUIC. This approach allows me to investigate the relationship between packet size, packet loss, and goodput under controlled conditions.

Designed a simplified network model with configurable bandwidth, packet overhead, packet sizes, and loss probabilities.

Established an initial approach where POTU explores different packet sizes, estimates their loss probabilities, and selects a size based on expected goodput.

Also decided to compare POTU against a baseline that consistently transmits at the maximum permitted packet size.

## Entry 3 — Initial Implementation and Experiments

Implemented the initial simulation framework in Python, including the `Network` and `POTU` classes, unit tests, and functions for running repeated experiments.

The `Network` class simulates packet transmission and probabilistic loss, while the `POTU` class records transmission outcomes, estimates loss probabilities, and selects packet sizes based on expected goodput.

Conducted an initial experiment using five packet sizes (1200, 1300, 1400, 1492, and 1500 bytes), with hypothetical loss probabilities ranging from 0.1% to 3%.

Across 100 trials, POTU achieved an average steady-state goodput improvement of approximately 1.98% and an average overall improvement of approximately 1.97% compared with the fixed maximum-size baseline.

Observed that POTU did not consistently select the theoretical optimal packet size, suggesting that exploration sample size may affect selection reliability.

Identified several limitations of the current implementation, including the lack of periodic re-exploration and the use of a simplified goodput model.