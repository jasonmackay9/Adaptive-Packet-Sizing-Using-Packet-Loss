
class POTU:
    def __init__(self, packet_sizes, min_samples = 100, improvement_threshold = 0.005, 
                 exploration_strategy = "interleaved"):

        if exploration_strategy not in ["interleaved", "sequential"]:
            raise ValueError("Invalid exploration strategy. Choose 'interleaved' or 'sequential'.")
        
        self.packet_sizes = packet_sizes
        self.sent = {size: 0 for size in packet_sizes}
        self.lost = {size: 0 for size in packet_sizes}
        self.min_samples = min_samples
        self.improvement_threshold = improvement_threshold
        self.exploration_strategy = exploration_strategy
        self.exploration_index = 0

    def record_sent(self, packet_size, delivered):
        self.sent[packet_size] += 1

        if not delivered:
            self.lost[packet_size] += 1

    def estimated_loss_rate(self, packet_size):
        if self.sent[packet_size] == 0:
            return None
        
        return self.lost[packet_size] / self.sent[packet_size]

    def estimated_goodput(self, packet_size, bandwidth, overhead):
        estimated_loss_rate = self.estimated_loss_rate(packet_size)
        if estimated_loss_rate is None:
            return None

        payload_efficiency = (packet_size - overhead) / packet_size
        return bandwidth * payload_efficiency * (1 - estimated_loss_rate)

    def has_enough_samples(self, packet_size):
        return self.sent[packet_size] >= self.min_samples

    def select_efficient_packet_size(self, current_packet_size, bandwidth, overhead):
        if not self.has_enough_samples(current_packet_size):
            return current_packet_size

        current_goodput = self.estimated_goodput(current_packet_size, bandwidth, overhead)

        best_packet_size = current_packet_size
        best_goodput = current_goodput

        for packet_size in self.packet_sizes:
            if packet_size == current_packet_size:
                continue

            if not self.has_enough_samples(packet_size):
                continue

            goodput = self.estimated_goodput(packet_size, bandwidth, overhead)

            if goodput is not None and goodput > best_goodput:
                best_goodput = goodput
                best_packet_size = packet_size

        if best_goodput > current_goodput * (1 + self.improvement_threshold):
            return best_packet_size
        
        return current_packet_size

    def next_exploration_packet_size(self):

        if self.exploration_strategy == "sequential":
            for packet_size in self.packet_sizes:
                if not self.has_enough_samples(packet_size):
                    return packet_size

            return None

        for _ in range(len(self.packet_sizes)):
            packet_size = self.packet_sizes[self.exploration_index]
            self.exploration_index = (self.exploration_index + 1) % len(self.packet_sizes)

            if not self.has_enough_samples(packet_size):
                return packet_size

        return None

    def reset_exploration(self):
        self.sent = {packet_size: 0 for packet_size in self.packet_sizes}
        self.lost = {packet_size: 0 for packet_size in self.packet_sizes}
        self.exploration_index = 0

    