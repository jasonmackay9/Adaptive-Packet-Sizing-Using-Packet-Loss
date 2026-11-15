from pathlib import Path
import sys
import matplotlib.pyplot as plt

# Allow imports from the Simulation folder
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "Simulation"))

from network import Network

def main():
    loss_probabilities = {
        1200: 0.001,
        1300: 0.002,
        1400: 0.005,
        1492: 0.01,
        1500: 0.03,
    }

    network = Network(
        loss_probabilities=loss_probabilities,
        bandwidth=10_000_000,
        overhead=50,
    )

    packet_sizes = sorted(loss_probabilities)

    goodputs = [
        network.expected_goodput(size) / 1_000_000 for size in packet_sizes
    ]

    optimal_index = goodputs.index(max(goodputs))
    optimal_size = packet_sizes[optimal_index]

    fig, ax = plt.subplots(figsize=(8, 5))

    positions = range(len(packet_sizes))

    ax.plot(
        positions,
        goodputs,
        marker = "o",
        linewidth = 2,
        label = "Expected goodput",
    )

    ax.scatter(
        optimal_index,
        goodputs[optimal_index],
        s = 110,
        zorder = 3,
        label = f"Optimal size: {optimal_size} B",
    )

    ax.set_title("Expected Goodput by Packet Size")
    ax.set_xlabel("Packet size (bytes)")
    ax.set_ylabel("Expected goodput (Mbps)")

    ax.set_xticks(positions)
    ax.set_xticklabels(packet_sizes)

    ax.grid(True, alpha = 0.3)
    ax.legend()

    fig.tight_layout()

    output_dir = Path(__file__).resolve().parent / "figures"
    output_dir.mkdir(parents = True, exist_ok = True)

    output_path = output_dir / "expected_goodput.png"
    fig.savefig(output_path, dpi = 300)

    print(f"Optimal packet size: {optimal_size} bytes")
    print(f"Maximum expected goodput: {max(goodputs):.4f} Mbps")
    print(f"Figure saved to: {output_path}")

    plt.show()


if __name__ == "__main__":
    main()
