
import unittest
from potu import POTU


class TestPOTU(unittest.TestCase):

    def setUp(self):
        self.potu = POTU(
            [1200, 1300, 1400, 1492, 1500], min_samples=100, improvement_threshold=0.005)

        self.bandwidth = 10_000_000
        self.overhead = 50

    def test_record_sent(self):
        self.potu.record_sent(1500, True)
        self.potu.record_sent(1500, True)
        self.potu.record_sent(1500, False)
        self.potu.record_sent(1500, True)

        self.assertEqual(self.potu.sent[1500], 4)
        self.assertEqual(self.potu.lost[1500], 1)

    def test_estimated_loss_rate(self):
        self.assertIsNone(self.potu.estimated_loss_rate(1200))

        self.potu.record_sent(1500, True)
        self.potu.record_sent(1500, False)

        self.assertAlmostEqual(self.potu.estimated_loss_rate(1500), 0.5)

    def test_estimated_goodput(self):
        for delivered in [True, True, False, True]:
            self.potu.record_sent(1500, delivered)

        goodput = self.potu.estimated_goodput(1500, self.bandwidth, self.overhead)

        self.assertAlmostEqual(goodput, 7_250_000)

    def test_select_efficient_packet_size(self):
        loss_counts = {
            1200: 1,
            1300: 2,
            1400: 5,
            1492: 10,
            1500: 30
        }

        for packet_size, losses in loss_counts.items():
            for i in range(1000):
                delivered = i >= losses
                self.potu.record_sent(packet_size, delivered)

        selected_size = self.potu.select_efficient_packet_size(1500, self.bandwidth, self.overhead)

        self.assertEqual(selected_size, 1300)

    def test_next_exploration_packet_size(self):

        expected_order = [1200, 1300, 1400, 1492, 1500]

        for _ in range(100):
            for packet_size in expected_order:
                self.assertEqual(self.potu.next_exploration_packet_size(), packet_size)
                self.potu.record_sent(packet_size, True)

        self.assertIsNone(self.potu.next_exploration_packet_size())

    def test_sequential_exploration(self):
        potu = POTU(
            [1200, 1300, 1400, 1492, 1500],
            min_samples=100,
            improvement_threshold=0.005,
            exploration_strategy="sequential"
        )

        for packet_size in potu.packet_sizes:
            for _ in range(100):
                self.assertEqual(potu.next_exploration_packet_size(), packet_size)
                potu.record_sent(packet_size, True)

        self.assertIsNone(potu.next_exploration_packet_size())

    def test_invalid_exploration_strategy(self):
        with self.assertRaises(ValueError):
            POTU(
                [1200, 1300, 1400, 1492, 1500],
                min_samples=100,
                improvement_threshold=0.005,
                exploration_strategy="invalid_strategy"
            )

    def test_reset_exploration(self):
        self.potu.record_sent(1500, True)
        self.potu.record_sent(1500, False)

        self.potu.reset_exploration()

        self.assertEqual(self.potu.sent[1500], 0)
        self.assertEqual(self.potu.lost[1500], 0)
        self.assertEqual(self.potu.exploration_index, 0)

        self.assertEqual(
            self.potu.next_exploration_packet_size(),
            1200
        )

    

if __name__ == "__main__":
    unittest.main()
