import torch
import torch.nn as nn
import numpy as np

class PricePredictor(nn.Module):
    def __init__(self, input_dim=4, hidden_dim=16):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1)
        )
    def forward(self, x):
        return self.net(x)

class PredictorWrapper:
    def __init__(self):
        self.model = PricePredictor()
        self.model.eval()
    def predict(self, features):
        x = torch.tensor(features, dtype=torch.float32)
        with torch.no_grad():
            pred = self.model(x)
        return pred.item()
