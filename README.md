
# AI Liquidity Universe

**Creator/Dev:** tubakhxn

## What is this project?
This project is a realistic financial limit order book simulator. It models the dynamics of a market order book, including bid/ask levels, random order arrivals, market orders, volatility shocks, spoofing, flash crash events, and liquidity imbalance. It also includes an AI model to predict short-term price movements and provides interactive 3D liquidity visualization using Matplotlib and Plotly.

## How to fork this project
1. Go to the GitHub repository for this project (or upload it to your own GitHub account).
2. Click the "Fork" button at the top right of the repository page.
3. Clone your forked repository to your local machine:
	```
	git clone https://github.com/your-username/ai-liquidity-universe.git
	```
4. Install dependencies and run as described below.

## Features
- Simulates bid/ask order book levels
- Random order arrivals
- Market orders consuming liquidity
- Volatility shocks
- Spoofing (fake liquidity)
- Flash crash events
- Liquidity imbalance
- AI model predicts short-term price movement
- Interactive dashboard (volatility, price levels, spoofing, flash crash, play/pause)
- Animated 3D surface (Plotly)

## Usage
1. Install Python 3.8+
2. Run: `python main.py`
3. Dashboard opens in browser

## Project Structure
- main.py
- requirements.txt
- simulation/
- ai/
- visualization/
- utils/

## Dependencies
- numpy
- pandas
- plotly
- dash
- scikit-learn
- torch
- numba
