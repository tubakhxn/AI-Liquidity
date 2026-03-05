
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation



# Ensure parent directory and ai_liquidity_universe directory are in sys.path for imports
PARENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
UNIVERSE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
for path in [PARENT_DIR, UNIVERSE_DIR]:
    if path not in sys.path:
        sys.path.insert(0, path)

from ai.feature_engineering import compute_features
from ai.prediction_model import PredictorWrapper
from simulation.market_engine import MarketEngine

def plot_liquidity_surface(n_levels=20, volatility=0.5, spoofing=False, flash_crash=False, steps=500):
    engine = MarketEngine(n_levels=n_levels, volatility=volatility, spoofing=spoofing)
    if flash_crash:
        engine.trigger_flash_crash()
    for _ in range(steps):
        engine.step()
    history = engine.get_history()
    if len(history) < 2:
        print("Not enough history to plot.")
        return
    timesteps = np.array([h[0] for h in history[-steps:]])
    prices = np.array([h[1] for h in history[-steps:]])
    bids = np.array([h[2] for h in history[-steps:]])
    asks = np.array([h[3] for h in history[-steps:]])
    liquidity = bids - asks
    n_levels = prices.shape[1]
    level_indices = np.arange(n_levels)
    T, L = np.meshgrid(timesteps, level_indices, indexing='ij')
    Z = liquidity
    X = L
    Y = T
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(X, Y, Z, cmap='RdBu', edgecolor='none')
    ax.set_xlabel('Price Levels')
    ax.set_ylabel('Time')
    ax.set_zlabel('Liquidity Volume')
    ax.set_title('Liquidity Landscape')
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10, label='Imbalance')
    plt.show()

if __name__ == "__main__":
    plot_liquidity_surface()
