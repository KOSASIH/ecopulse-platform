import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from prophet import Prophet
from sklearn.preprocessing import MinMaxScaler

class EnergyForecastingDataset(Dataset):
    def __init__(self, data, seq_len, forecast_len):
        self.data = data
        self.seq_len = seq_len
        self.forecast_len = forecast_len

    def __len__(self):
        return len(self.data) - self.seq_len - self.forecast_len

    def __getitem__(self, idx):
        seq_data = self.data[idx:idx + self.seq_len]
        forecast_data = self.data[idx + self.seq_len:idx + self.seq_len + self.forecast_len]
        return {
            'eq_data': torch.tensor(seq_data).float(),
            'forecast_data': torch.tensor(forecast_data).float()
        }

class LSTMModel(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(LSTMModel, self).__init__()
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers=1, batch_first=True)
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        h0 = torch.zeros(1, x.size(0), self.hidden_dim).to(x.device)
        c0 = torch.zeros(1, x.size(0), self.hidden_dim).to(x.device)
        out, _ = self.lstm(x, (h0, c0))
        out = self.fc(out[:, -1, :])
        return out

def train_model(model, device, train_loader, optimizer, criterion):
    model.train()
    total_loss = 0
    for batch in train_loader:
        seq_data, forecast_data = batch['seq_data'].to(device), batch['forecast_data'].to(device)
        optimizer.zero_grad()
        output = model(seq_data)
        loss = criterion(output, forecast_data)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    return total_loss / len(train_loader)

def evaluate_model(model, device, test_loader):
    model.eval()
    total_loss = 0
    with torch.no_grad():
        for batch in test_loader:
            seq_data, forecast_data = batch['seq_data'].to(device), batch['forecast_data'].to(device)
            output = model(seq_data)
            loss = criterion(output, forecast_data)
            total_loss += loss.item()
    return total_loss / len(test_loader)

if __name__ == '__main__':
    # Load data
    data = pd.read_csv('energy_data.csv', index_col='date', parse_dates=['date'])

    # Preprocess data
    scaler = MinMaxScaler()
    data_scaled = scaler.fit_transform(data)

    # Create dataset and data loader
    seq_len = 24
    forecast_len = 24
    dataset = EnergyForecastingDataset(data_scaled, seq_len, forecast_len)
    batch_size = 32
    train_loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    # Create model
    input_dim = 1
    hidden_dim = 128
    output_dim = 1
    model = LSTMModel(input_dim, hidden_dim, output_dim)

    # Define device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)

    # Define optimizer and criterion
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.MSELoss()

    # Train model
    for epoch in range(100):
        loss = train_model(model, device, train_loader, optimizer, criterion)
        print(f'Epoch {epoch+1}, Loss: {loss:.4f}')

    # Evaluate model
    test_loader = DataLoader(dataset, batch_size=batch_size, shuffle=False)
    loss = evaluate_model(model, device, test_loader)
    print(f'Test Loss: {loss:.4f}')

    # Use Prophet for long-term forecasting
    prophet_model = Prophet()
    prophet_model.fit(data)
    future = prophet_model.make_future_dataframe(periods=30)
    forecast = prophet_model.predict(future)
    print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())
