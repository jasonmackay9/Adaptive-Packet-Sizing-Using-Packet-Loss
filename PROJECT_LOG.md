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

Investigated whether interleaved exploration could reduce the influence of changing congestion conditions on packet-loss estimates. Initial experiments suggested that neither strategy consistently outperformed the other, although the exact experimental configuration used to produce some of the original regret values was not preserved. These results were therefore revisited in a subsequent experiment to establish a reproducible comparison.

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

## Entry 6 - Additional Experiments, Visualization, and Midterm Project Update - Mid November

Extended the experimental evaluation by conducting 1,000 trials using independently generated packet-loss profiles, with both 100 and 1,000 exploration samples per candidate packet size.

With 100 samples per candidate, POTU achieved an average steady-state goodput improvement of 0.80% and an average overall improvement of 0.79% compared with the fixed 1500-byte baseline. Increasing exploration to 1,000 samples improved these results to 1.08% and 0.93%, respectively. This demonstrated that additional exploration can improve packet-size selection accuracy, although it also increases exploration overhead.

Added Python plotting scripts to visualize the experimental results, including theoretical expected goodput for different packet sizes, distributions of goodput improvement across randomly generated loss profiles, and average goodput regret for sequential and interleaved exploration.

Revisited the earlier exploration-strategy experiment after discovering that its original regret values could not be reproduced using the parameters in the new plotting script. The precise cause of the discrepancy was not established, as the original experimental configuration was not fully documented. Rather than relying on those earlier values, a new set of experiments was conducted using explicitly defined parameters.

The updated exploration experiments evaluated congestion intervals of 50, 100, and 500 transmissions, with an additional 5-percentage-point packet-loss probability during congested periods. Sequential and interleaved exploration were compared using 50, 100, 250, 500, and 1,000 samples per candidate packet size, with 100 trials per configuration.

Across the 15 configurations, interleaved exploration achieved lower average goodput regret in 10 cases, while sequential exploration performed better in 5. Both strategies generally achieved lower regret as the number of exploration samples increased. These results suggest that exploration timing and congestion conditions influence the relative performance of each strategy, rather than either strategy being consistently superior.

Updated the experimental analysis to use the new results and generated a comparison graph for the 500-transmission congestion interval, illustrating how the relative performance of the two strategies changes with exploration sample size.

Completed the midterm project update, documenting POTU's implementation, experimental methodology, results, limitations, and potential future improvements. The report also establishes a foundation for the final project report and presentation.