import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import numpy as np
from ai.feature_engineering import compute_features
from ai.prediction_model import PredictorWrapper

engine = None
predictor = PredictorWrapper()

app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("AI Liquidity Universe Simulator"),
    dcc.Graph(id="liquidity-3d"),
    html.Div([
        html.Label("Volatility"),
        dcc.Slider(id="volatility-slider", min=0.1, max=2.0, step=0.1, value=0.5),
        html.Label("Price Levels"),
        dcc.Slider(id="levels-slider", min=10, max=50, step=1, value=20),
        html.Label("Spoofing"),
        dcc.Checklist(id="spoofing-toggle", options=[{"label": "Enable", "value": "spoof"}], value=[]),
        html.Button("Flash Crash", id="flash-crash-btn"),
        html.Button("Play/Pause", id="play-pause-btn"),
    ], style={"width": "50%"}),
    dcc.Interval(id="interval", interval=200, n_intervals=0, disabled=False)
])

playing = True

@app.callback(
    Output("interval", "disabled"),
    [Input("play-pause-btn", "n_clicks")],
    [State("interval", "disabled")]
)
def toggle_play_pause(n_clicks, disabled):
    if n_clicks is None:
        return False
    return not disabled

@app.callback(
    Output("liquidity-3d", "figure"),
    [Input("interval", "n_intervals"),
     Input("volatility-slider", "value"),
     Input("levels-slider", "value"),
     Input("spoofing-toggle", "value"),
     Input("flash-crash-btn", "n_clicks")]
)
def update_surface(n, volatility, n_levels, spoofing, flash_crash):
    global engine
    if engine is None or engine.n_levels != n_levels:
        engine = __import__("simulation.market_engine").market_engine.MarketEngine(n_levels=n_levels, volatility=volatility, spoofing="spoof" in spoofing)
    engine.set_volatility(volatility)
    engine.set_spoofing("spoof" in spoofing)
    if flash_crash:
        engine.trigger_flash_crash()
    engine.step()
    history = engine.get_history()
    if len(history) < 2:
        return go.Figure()
    timesteps = [h[0] for h in history[-500:]]
    prices = np.array([h[1] for h in history[-500:]])
    bids = np.array([h[2] for h in history[-500:]])
    asks = np.array([h[3] for h in history[-500:]])
    liquidity = bids - asks
    surface = go.Surface(
        x=prices.T,
        y=np.tile(timesteps, (prices.shape[1], 1)).T,
        z=liquidity.T,
        surfacecolor=bids.T - asks.T,
        colorscale="RdBu",
        colorbar=dict(title="Imbalance"),
    )
    features = compute_features(prices[-1], bids[-1], asks[-1])
    pred = predictor.predict(features)
    fig = go.Figure(data=[surface])
    # Animate camera rotation
    angle = 0.5 + 0.5 * np.sin(n * 0.05)
    fig.update_layout(
        title=f"Liquidity Landscape (Predicted ΔPrice: {pred:.4f})",
        scene=dict(
            xaxis_title="Price Levels",
            yaxis_title="Time",
            zaxis_title="Liquidity Volume",
            camera=dict(eye=dict(x=2.0 * np.cos(angle), y=2.0 * np.sin(angle), z=1.2))
        ),
        margin=dict(l=0, r=0, b=0, t=40)
    )
    return fig

def run_dashboard(engine_instance):
    global engine
    engine = engine_instance
    app.run(debug=True)
