from utils.dependency_installer import install_dependencies
install_dependencies()

from simulation.market_engine import MarketEngine
from visualization.liquidity_surface import run_dashboard

if __name__ == "__main__":
    import numpy as np
    import time
    from ai.feature_engineering import compute_features
    from ai.prediction_model import PredictorWrapper
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D

    engine = MarketEngine()
    predictor = PredictorWrapper()
    # Pre-fill history
    for _ in range(500):
        engine.step()

    plt.ion()
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    while True:
        engine.step()
        history = engine.get_history()
        timesteps = np.array([h[0] for h in history[-500:]])
        prices = np.array([h[1] for h in history[-500:]])
        bids = np.array([h[2] for h in history[-500:]])
        asks = np.array([h[3] for h in history[-500:]])
        liquidity = bids - asks
        ax.clear()
        # X: price levels, Y: time, Z: liquidity
        X, Y = np.meshgrid(prices[-1], timesteps)
        Z = liquidity
        surf = ax.plot_surface(X, Y, Z, cmap='coolwarm', edgecolor='none')
        ax.set_xlabel('Price Levels')
        ax.set_ylabel('Time')
        ax.set_zlabel('Liquidity Volume')
        features = compute_features(prices[-1], bids[-1], asks[-1])
        pred = predictor.predict(features)
        ax.set_title(f'Liquidity Landscape (Predicted ΔPrice: {pred:.4f})')
        fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10, label='Imbalance')
        plt.draw()
        plt.pause(0.5)
