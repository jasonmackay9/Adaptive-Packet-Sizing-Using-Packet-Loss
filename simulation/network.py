import random

class Network:
    def __init__(self, loss_probabilities, bandwidth, overhead, congestion_interval = None, congestion_loss = 0.0):
        self.loss_probabilities = loss_probabilities
        self.bandwidth = bandwidth
        self.overhead = overhead
        self.packet_count = 0
        self.congestion_interval = congestion_interval
        self.congestion_loss = congestion_loss

    def payload_size(self, packet_size):
        return packet_size - self.overhead

    def transmission_time(self, packet_size):
        return (packet_size * 8) / self.bandwidth #transmission time in seconds

    def transmit(self, packet_size):
        loss_probability = self.loss_probabilities[packet_size]

        if self.is_congested():
            loss_probability += self.congestion_loss

        loss_probability = min(loss_probability, 1.0)
        self.packet_count += 1

        return random.random() >= loss_probability

    def expected_goodput(self, packet_size):
        loss_probability = self.loss_probabilities[packet_size]
        payload_efficiency = self.payload_size(packet_size) / packet_size
        return self.bandwidth * payload_efficiency * (1 - loss_probability)

    def is_congested(self):
        if self.congestion_interval is None:
            return False
        
        phase = (self.packet_count // self.congestion_interval) % 2
        return phase == 1

    def update_loss_probabilities(self, new_loss_probabilities) :
        self.loss_probabilities = new_loss_probabilities

