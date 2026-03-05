import numpy as np
from simulation.order_book import OrderBook
import random

class MarketEngine:
    def __init__(self, n_levels=20, volatility=0.5, spoofing=False):
        self.n_levels = n_levels
        self.volatility = volatility
        self.spoofing = spoofing
        self.order_book = OrderBook(n_levels=n_levels)
        self.timestep = 0
        self.history = []
        self.flash_crash = False
        self.reset()

    def reset(self):
        self.order_book.reset()
        self.timestep = 0
        self.history = []
        self.flash_crash = False

    def step(self):
        # Volatility shock
        if random.random() < self.volatility * 0.01:
            shock = np.random.normal(0, self.volatility)
            self.order_book.mid_price += shock
            self.order_book.prices += shock
        # Flash crash event
        if self.flash_crash:
            crash_level = random.randint(0, self.n_levels//2)
            self.order_book.bids[:crash_level] = 0
            self.order_book.asks[:crash_level] = 0
            self.flash_crash = False
        # Spoofing
        if self.spoofing and random.random() < 0.05:
            spoof_level = random.randint(0, self.n_levels-1)
            self.order_book.add_order("bid", spoof_level, 1000)
            # Remove spoof after a few steps
            if self.timestep % 10 == 0:
                self.order_book.bids[spoof_level] = 0
        # Random order arrivals
        for _ in range(random.randint(5, 15)):
            side = random.choice(["bid", "ask"])
            level = random.randint(0, self.n_levels-1)
            volume = np.abs(np.random.normal(10, 5))
            self.order_book.add_order(side, level, volume)
        # Market orders
        for _ in range(random.randint(1, 3)):
            side = random.choice(["bid", "ask"])
            level = random.randint(0, self.n_levels-1)
            volume = np.abs(np.random.normal(20, 10))
            self.order_book.consume_order(side, level, volume)
        # Save snapshot
        prices, bids, asks = self.order_book.get_snapshot()
        self.history.append((self.timestep, prices.copy(), bids.copy(), asks.copy()))
        self.timestep += 1

    def trigger_flash_crash(self):
        self.flash_crash = True

    def set_volatility(self, value):
        self.volatility = value

    def set_n_levels(self, value):
        self.n_levels = value
        self.order_book = OrderBook(n_levels=value)

    def set_spoofing(self, value):
        self.spoofing = value

    def get_history(self):
        return self.history
