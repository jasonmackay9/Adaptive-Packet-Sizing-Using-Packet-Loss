
from pathlib import Path
import matplotlib.pyplot as plt
import sys
import random
import csv
import statistics

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "Simulation"))

from run_simulation import (
    generate_loss_probabilities,
    run_experiment,
)


PACKET_SIZES = [1200, 1300, 1400, 1492, 1500]
NUM_PROFILES = 1000
MIN_SAMPLES = 1000
NUM_PACKETS = 10_000


def main():
    random_generator = random.Random(2026)
    results = []

    for profile_index in range(NUM_PROFILES):
        loss_probabilities = generate_loss_probabilities(
            packet_sizes = PACKET_SIZES,
            random_generator = random_generator,
        )

        result = run_experiment(
            seed = profile_index,
            loss_probabilities = loss_probabilities,
            min_samples = MIN_SAMPLES,
            num_packets = NUM_PACKETS,
        )

        results.append({
            "profile": profile_index,
            "steady_state_improvement": result["steady_state_improvement"],
            "overall_improvement": result["overall_improvement"],
            **{
                f"loss_{size}": loss_probabilities[size]
                for size in PACKET_SIZES
            },
        })

    steady_state = [
        result["steady_state_improvement"] for result in results
    ]

    overall = [
        result["overall_improvement"] for result in results
    ]

    print(f"Independent loss profiles: {NUM_PROFILES}")
    print(f"Average steady-state improvement: {statistics.mean(steady_state):.2f}%")
    print(f"Average overall improvement: {statistics.mean(overall):.2f}%")
    print(f"Profiles with positive steady-state improvement: {sum(value > 0 for value in steady_state) / NUM_PROFILES:.1%}")
    print(f"Profiles with positive overall improvement: {sum(value > 0 for value in overall) / NUM_PROFILES:.1%}")
    print(f"Median improvement: {statistics.median(steady_state):.2f}%")
    print(f"Standard deviation: {statistics.stdev(steady_state):.2f} percentage points")
    print(f"Improvement range: {min(steady_state):.2f}% to {max(steady_state):.2f}%")

    output_dir = Path(__file__).resolve().parent / "results"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "random_profiles.csv"

    with output_path.open("w", newline = "") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=results[0].keys(),
        )
        writer.writeheader()
        writer.writerows(results)

    print(f"Results saved to: {output_path}")

    fig, ax = plt.subplots(figsize = (9, 5))

    average_improvement = statistics.mean(steady_state)

    ax.hist(
        steady_state,
        bins = 30,
        edgecolor = "black",
        alpha = 0.75,
        label = "Simulation results",
    )

    ax.axvline(
        0,
        color = "red",
        linestyle = "--",
        linewidth = 2,
        label = "No improvement (0%)",
    )

    ax.axvline(
        average_improvement,
        color = "green",
        linestyle = "--",
        linewidth = 2,
        label = f"Mean improvement: {average_improvement:.2f}%",
    )

    ax.set_title(
        "Distribution of Steady-State Goodput Improvement"
    )
    ax.set_xlabel("Goodput improvement over baseline (%)")
    ax.set_ylabel("Number of simulated loss profiles")

    ax.legend()
    ax.grid(axis="y", alpha = 0.3)

    fig.tight_layout()

    figures_dir = Path(__file__).resolve().parent / "figures"
    figures_dir.mkdir(parents=True, exist_ok = True)

    figure_path = figures_dir / "random_profiles_histogram.png"
    fig.savefig(figure_path, dpi = 300)

    print(f"Figure saved to: {figure_path}")

    plt.show()



if __name__ == "__main__":
    main()
