import numpy as np

def compute_features(prices, bids, asks):
    order_imbalance = np.sum(bids) - np.sum(asks)
    spread = prices[np.argmax(asks)] - prices[np.argmax(bids)]
    volume_delta = np.sum(bids) - np.sum(asks)
    volatility = np.std(prices)
    return np.array([order_imbalance, spread, volume_delta, volatility])
