import numpy as np

class OrderBook:
    def __init__(self, n_levels=20, tick_size=0.01, mid_price=100.0):
        self.n_levels = n_levels
        self.tick_size = tick_size
        self.mid_price = mid_price
        self.reset()

    def reset(self):
        self.bids = np.zeros(self.n_levels)
        self.asks = np.zeros(self.n_levels)
        self.prices = np.array([
            self.mid_price + (i - self.n_levels//2) * self.tick_size
            for i in range(self.n_levels)
        ])

    def add_order(self, side, level, volume):
        if side == "bid":
            self.bids[level] += volume
        else:
            self.asks[level] += volume

    def consume_order(self, side, level, volume):
        if side == "bid":
            self.bids[level] = max(0, self.bids[level] - volume)
        else:
            self.asks[level] = max(0, self.asks[level] - volume)

    def get_snapshot(self):
        return self.prices.copy(), self.bids.copy(), self.asks.copy()
