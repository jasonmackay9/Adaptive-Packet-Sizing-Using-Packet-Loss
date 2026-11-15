# Project Logbook

## Entry 1 - Initial Research and Project Proposal - Early October

Investigated the possibility of improving QUIC goodput by selecting packet sizes based on observed packet loss rather than always using the maximum viable packet size.

Reviewed DPLPMTUD and identified that, while it determines the maximum usable packet size, this may not always be the most efficient size when packet-loss probability depends on packet size.

Developed the initial concept for POTU (Path Optimal Transmission Unit), a proposed mechanism that estimates packet-loss probabilities and uses these estimates to select a packet size expected to improve goodput.

Completed and submitted the initial project proposal.

## Entry 2 - Simulation Design - Mid October

Decided to use a Python-based simulation rather than implementing POTU directly within QUIC. This approach allows me to investigate the relationship between packet size, packet loss, and goodput under controlled conditions.

Designed a simplified network model with configurable bandwidth, packet overhead, packet sizes, and loss probabilities.

Established an initial approach where POTU explores different packet sizes, estimates their loss probabilities, and selects a size based on expected goodput.

Also decided to compare POTU against a baseline that consistently transmits at the maximum permitted packet size.

## Entry 3 - Initial Implementation and Experiments - Early November

Implemented the initial simulation framework in Python, including the `Network` and `POTU` classes, unit tests, and functions for running repeated experiments.

The `Network` class simulates packet transmission and probabilistic loss, while the `POTU` class records transmission outcomes, estimates loss probabilities, and selects packet sizes based on expected goodput.

Conducted an initial experiment using five packet sizes (1200, 1300, 1400, 1492, and 1500 bytes), with hypothetical loss probabilities ranging from 0.1% to 3%.

Across 100 trials, POTU achieved an average steady-state goodput improvement of approximately 1.98% and an average overall improvement of approximately 1.97% compared with the fixed maximum-size baseline.

Observed that POTU did not consistently select the theoretical optimal packet size, suggesting that exploration sample size may affect selection reliability.

Identified several limitations of the current implementation, including the lack of periodic re-exploration and the use of a simplified goodput model.

## Entry 4 - Exploration Strategies and Performance Evaluation - Mid November

Extended the simulation to support randomly generated packet-loss profiles and alternating periods of network congestion. This allowed me to evaluate POTU under more varied network conditions rather than relying exclusively on manually selected loss probabilities.

Conducted experiments using a randomly generated packet-loss profile across 100 trials. POTU achieved an average goodput improvement of approximately 0.59% compared with the fixed maximum-size baseline, suggesting that the benefits of packet-size optimization depend on the network's loss characteristics.

Implemented and compared two exploration strategies: sequential exploration, which tests each packet size before moving to the next, and interleaved exploration, which alternates between candidate packet sizes.

Investigated whether interleaving exploration could reduce the influence of changing congestion conditions on packet-loss estimates. Across different congestion intervals, neither exploration strategy consistently outperformed the other.

Also investigated how the number of exploration samples affects packet-size selection. Generally, increasing the number of samples reduced selection regret, although improvements were not consistent across every configuration.

These experiments highlighted the trade-off between exploration overhead and selection accuracy, as well as the difficulty of distinguishing packet-size-dependent loss from temporary network congestion.

## Entry 5 - Adaptation to Network Path Changes - Mid November

Extended the simulation to support changes in network loss probabilities during an experiment. Also implemented functionality allowing POTU to discard previous observations and repeat its exploration process.

Designed a controlled path-change experiment where the initial network conditions had relatively low packet loss across all candidate sizes, before changing to conditions where larger packets experienced substantially higher loss probabilities.

Conducted the experiment across 1,000 trials using different random seeds, with 1,000 exploration samples per candidate packet size.

POTU selected a smaller packet size after the simulated path change in 987 of the 1,000 trials (98.7%). It selected the theoretical goodput-optimal packet size of 1300 bytes in 680 trials (68.0%).

These results suggest that POTU can consistently adjust its packet-size selection when the network's loss characteristics change. However, the results also demonstrate that selecting a smaller packet size does not necessarily mean selecting the optimal size.

Implemented and successfully passed additional unit tests verifying that the network's loss probabilities can be updated and that POTU's exploration observations can be reset correctly.

Identified several areas for future work, including automatically triggering re-exploration, evaluating adaptation overhead, and measuring overall goodput when network conditions change.