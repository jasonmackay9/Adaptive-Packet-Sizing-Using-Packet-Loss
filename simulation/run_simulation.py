import random
from network import Network
from potu import POTU

MAXIMUM_PACKET_SIZE = 1500

def run_experiment(seed, loss_probabilities, min_samples, num_packets, 
                   exploration_strategy = "interleaved", congestion_interval = None,
                   congestion_loss = 0.0):
    random.seed(seed)

    potu_network = Network(loss_probabilities, 
                           10_000_000, 
                           50, 
                           congestion_interval = congestion_interval, 
                           congestion_loss = congestion_loss)
    
    baseline_network = Network(loss_probabilities, 
                               10_000_000, 
                               50, 
                               congestion_interval = congestion_interval, 
                               congestion_loss = congestion_loss)

    potu = POTU(
        packet_sizes = [packet_size for packet_size in loss_probabilities.keys() if packet_size <= MAXIMUM_PACKET_SIZE],
        min_samples = min_samples,
        improvement_threshold = 0.005,
        exploration_strategy = exploration_strategy)

    # Initial exploration
    exploration_time, exploration_delivered_bytes = run_potu_exploration(potu_network, potu)

    # Select efficient packet size based on exploration results
    selected_packet_size = potu.select_efficient_packet_size(MAXIMUM_PACKET_SIZE, potu_network.bandwidth, potu_network.overhead)

    # Baseline transmission with maximum packet size
    baseline_time, baseline_delivered_bytes = run_baseline(baseline_network, MAXIMUM_PACKET_SIZE, num_packets)
    baseline_goodput = (baseline_delivered_bytes * 8) / baseline_time

    # POTU steady-state transmission (excluding exploration)
    potu_steady_state_time, potu_steady_state_delivered_bytes = run_potu_steady_state(potu_network, potu, selected_packet_size, num_packets)
    potu_steady_state_goodput = (potu_steady_state_delivered_bytes * 8) / potu_steady_state_time

    # POTU overall performance (including exploration)
    potu_total_time = exploration_time + potu_steady_state_time
    potu_total_delivered_bytes = exploration_delivered_bytes + potu_steady_state_delivered_bytes
    potu_overall_goodput = (potu_total_delivered_bytes * 8) / potu_total_time

    # Percentage improvements
    steady_state_improvement = ((potu_steady_state_goodput - baseline_goodput) / baseline_goodput) * 100
    overall_improvement = ((potu_overall_goodput - baseline_goodput) / baseline_goodput) * 100

    return {
        "selected_packet_size": selected_packet_size,
        "baseline_goodput": baseline_goodput,
        "potu_steady_state_goodput": potu_steady_state_goodput,
        "potu_overall_goodput": potu_overall_goodput,
        "steady_state_improvement": steady_state_improvement,
        "overall_improvement": overall_improvement
    }

def run_baseline(network, packet_size, num_packets):
    total_time = 0
    delivered_bytes = 0

    for _ in range(num_packets):
        total_time += network.transmission_time(packet_size)

        delivered = network.transmit(packet_size)

        if delivered:
            delivered_bytes += network.payload_size(packet_size)

    return total_time, delivered_bytes

def run_potu_exploration(network, potu):
    exploration_time = 0
    exploration_delivered_bytes = 0

    while True:
        packet_size = potu.next_exploration_packet_size()

        if packet_size is None:
            break

        exploration_time += network.transmission_time(packet_size)

        delivered = network.transmit(packet_size)
        potu.record_sent(packet_size, delivered)

        if delivered:
            exploration_delivered_bytes += network.payload_size(packet_size)

    return exploration_time, exploration_delivered_bytes

def run_potu_steady_state(network, potu, packet_size, num_packets):
    total_time = 0
    delivered_bytes = 0

    for _ in range(num_packets):
        total_time += network.transmission_time(packet_size)

        delivered = network.transmit(packet_size)
        potu.record_sent(packet_size, delivered)

        if delivered:
            delivered_bytes += network.payload_size(packet_size)

    return total_time, delivered_bytes

def compare_exploration(seed, loss_probabilities, min_samples,
                         congestion_interval, congestion_loss):

    results = {}
    for strategy in ["interleaved", "sequential"]:
        random.seed(seed)

        network = Network(loss_probabilities, 
                          10_000_000, 
                          50,
                          congestion_interval = congestion_interval, 
                          congestion_loss = congestion_loss)

        potu = POTU(
            packet_sizes = list(loss_probabilities.keys()),
            min_samples = min_samples,
            exploration_strategy = strategy)

        run_potu_exploration(network, potu)

        selected_size = potu.select_efficient_packet_size(MAXIMUM_PACKET_SIZE, 
                                                          network.bandwidth, 
                                                          network.overhead)

        results[strategy] = {
            "selected_packet_size": selected_size,
            "loss_estimates": {size: potu.estimated_loss_rate(size) for size in potu.packet_sizes}
        }

    return results

def evaluate_exploration_strategies(num_trials, loss_probabilities,
                                    min_samples, congestion_interval, congestion_loss):

    congestion_fraction = 0.5 if congestion_interval is not None else 0.0
    expected_goodputs = {}

    for size, base_loss, in loss_probabilities.items():
        average_loss = base_loss + congestion_fraction * congestion_loss
        payload_efficiency = (size - 50) / size
        expected_goodputs[size] = (10_000_000 * payload_efficiency * (1 - average_loss))

    optimal_goodput = max(expected_goodputs.values())
    
    selection_counts = {
        "sequential": {size: 0 for size in loss_probabilities},
        "interleaved": {size: 0 for size in loss_probabilities}
    }

    total_regret = {
        "sequential": 0.0,
        "interleaved": 0.0
    }

    for seed in range(num_trials):

        comparison = compare_exploration(
            seed = seed,
            loss_probabilities = loss_probabilities,
            min_samples = min_samples,
            congestion_interval = congestion_interval,
            congestion_loss = congestion_loss
        )

        for strategy, result in comparison.items():
            selected_size = result["selected_packet_size"]
            selection_counts[strategy][selected_size] += 1

            selected_goodput = expected_goodputs[selected_size]
            regret = optimal_goodput - selected_goodput

            total_regret[strategy] += regret

    average_regret = {
        strategy: total / num_trials for strategy, total in total_regret.items()
    }

    return {
        "selection_counts": selection_counts,
        "average_regret": average_regret
    }

def compare_congestion_intervals(intervals, num_trials, loss_probabilities, min_samples,
                                 congestion_loss):

    results = {}

    for interval in intervals:

        results[interval] = evaluate_exploration_strategies(
            num_trials = num_trials,
            loss_probabilities = loss_probabilities,
            min_samples = min_samples,
            congestion_interval = interval,
            congestion_loss = congestion_loss
        )

    return results

def compare_sample_sizes(sample_sizes, intervals, num_trials, loss_probabilities,
                         congestion_loss):

    results = {}

    for sample_size in sample_sizes:
        results[sample_size] = compare_congestion_intervals(
            intervals = intervals,
            num_trials = num_trials,
            loss_probabilities = loss_probabilities,
            min_samples = sample_size,
            congestion_loss = congestion_loss
        )

    return results

def generate_loss_probabilities(packet_sizes, random_generator):
    loss_probabilities = {}
    current_loss_probability = random_generator.uniform(0.0, 0.005)

    for packet_size in sorted(packet_sizes):
        current_loss_probability += random_generator.uniform(0.0, 0.01)
        loss_probabilities[packet_size] = min(current_loss_probability, 1.0)

    return loss_probabilities

def run_path_change_experiment(initial_loss_probabilities, new_loss_probabilities,
                               min_samples = 100, seed = 1):

    random.seed(seed)
    network = Network(initial_loss_probabilities, 10_000_000, 50)

    potu = POTU(
        packet_sizes = list(initial_loss_probabilities.keys()),
        min_samples = min_samples,
        improvement_threshold = 0.005
    )

    #initial network conditions
    run_potu_exploration(network, potu)

    initial_packet_size = potu.select_efficient_packet_size(
        MAXIMUM_PACKET_SIZE, network.bandwidth, network.overhead
    )

    #network path change
    network.update_loss_probabilities(new_loss_probabilities)

    potu.reset_exploration()
    run_potu_exploration(network, potu)

    updated_packet_size = potu.select_efficient_packet_size(
        initial_packet_size, network.bandwidth, network.overhead
    )

    return {
        "initial_packet_size": initial_packet_size,
        "updated_packet_size": updated_packet_size
    }


if __name__ == "__main__":
    loss_random_generator = random.Random(1)

    loss_probabilities = generate_loss_probabilities(
        packet_sizes = [1200, 1300, 1400, 1492, 1500],
        random_generator = loss_random_generator
    )

    num_trials = 100
    results = []

    for seed in range(num_trials):
        result = run_experiment(
            seed = seed,
            loss_probabilities = loss_probabilities,
            min_samples = 100,
            num_packets = 10_000
        )

        results.append(result)

    average_steady_state_improvement = sum(
        result["steady_state_improvement"] for result in results
    ) / num_trials

    average_overall_improvement = sum(
        result["overall_improvement"] for result in results
    ) / num_trials

    print("RANDOMIZED LOSS SCENARIO:")
    print(f"Loss probabilities: {loss_probabilities}")
    print(f"Number of trials: {num_trials}")
    print(f"Average steady-state improvement: {average_steady_state_improvement:.2f}%")
    print(f"Average overall improvement: {average_overall_improvement:.2f}%")

    initial_loss_probabilities = {
        1200: 0.001,
        1300: 0.002,
        1400: 0.003,
        1492: 0.004,
        1500: 0.005 
    }

    new_loss_probabilities = {
        1200: 0.001,
        1300: 0.003,
        1400: 0.008,
        1492: 0.02,
        1500: 0.05
    }

    successful_adaptions = 0
    optimal_adaptions = 0

    for seed in range(1000):
        path_change_results = run_path_change_experiment(
            initial_loss_probabilities = initial_loss_probabilities,
            new_loss_probabilities = new_loss_probabilities,
            min_samples = 1000,
            seed = seed
        )

        initial_size = path_change_results["initial_packet_size"]
        updated_size = path_change_results["updated_packet_size"]

        if updated_size < initial_size:
            successful_adaptions += 1

        if updated_size == 1300:
            optimal_adaptions += 1

        print(f"Seed {seed}: {initial_size} -> {updated_size} bytes")

    print(f"Adaptions to smaller packets: {successful_adaptions}/1000")
    print(f"Optimal adaptions: {optimal_adaptions}/1000")
