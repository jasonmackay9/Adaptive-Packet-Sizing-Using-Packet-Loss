
from pathlib import Path
import sys
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "Simulation"))

from run_simulation import compare_sample_sizes


def main():
    loss_probabilities = {
        1200: 0.001,
        1300: 0.002,
        1400: 0.005,
        1492: 0.01,
        1500: 0.03
    }

    sample_sizes = [50, 100, 250, 500, 1000]
    congestion_intervals = [50, 100, 500]
    num_trials = 100
    congestion_loss = 0.05

    results = compare_sample_sizes(
        sample_sizes = sample_sizes,
        intervals = congestion_intervals,
        num_trials = num_trials,
        loss_probabilities = loss_probabilities,
        congestion_loss = congestion_loss
    )

    sequential_regret = []
    interleaved_regret = []

    for sample_size in sample_sizes:
        average_regret = results[sample_size][500]["average_regret"]

        sequential_regret.append(average_regret["sequential"] / 1_000_000)
        interleaved_regret.append(average_regret["interleaved"] / 1_000_000)

    fig, ax = plt.subplots(figsize = (8, 5))

    ax.plot(
        sample_sizes,
        sequential_regret,
        marker = "o",
        linewidth = 2,
        label = "Sequential"
    )

    ax.plot(
        sample_sizes,
        interleaved_regret,
        marker = "o",
        linewidth = 2,
        label = "Interleaved"
    )

    ax.set_title("Goodput Regret by Exploration Sample Size")
    ax.set_xlabel("Exploration samples per packet size")
    ax.set_ylabel("Average goodput regret (Mbps)")
    ax.set_xticks(sample_sizes)
    ax.grid(True, alpha = 0.3)
    ax.legend()

    fig.tight_layout()

    output_dir = Path(__file__).resolve().parent / "figures"
    output_dir.mkdir(parents = True, exist_ok = True)

    output_path = output_dir / "exploration_regret.png"
    fig.savefig(output_path, dpi = 300)

    print(f"Figure saved to: {output_path}")

    
    print(f"Figure saved to: {output_path}")

    for interval in congestion_intervals:
        print()
        print(f"Congestion interval: {interval}")

        for sample_size in sample_sizes:
            average_regret = results[sample_size][interval]["average_regret"]

            sequential = average_regret["sequential"] / 1_000_000
            interleaved = average_regret["interleaved"] / 1_000_000

            print(
                f"{sample_size} samples: "
                f"Sequential = {sequential:.4f} Mbps, "
                f"Interleaved = {interleaved:.4f} Mbps"
            )

    plt.show()


if __name__ == "__main__":
    main()
