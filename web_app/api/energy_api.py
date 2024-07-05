from flask import Flask, jsonify, request
from flask_openapi import OpenAPI
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

app = Flask(__name__)
api = OpenAPI(app)

# Load energy data
energy_data = pd.read_csv("energy_data.csv")

# Define forecasting model
model = RandomForestRegressor(n_estimators=100)

# Define API endpoints
@api.route("/energy/forecast", methods=["GET"])
def get_forecast():
    # Get forecast data
    forecast_data = model.predict(energy_data)
    return jsonify({"forecast": forecast_data.tolist()})

@api.route("/energy/realtime", methods=["GET"])
def get_realtime_data():
    # Get real-time data
    realtime_data = energy_data.iloc[-1]
    return jsonify({"realtime": realtime_data.to_dict()})

@api.route("/energy/historical", methods=["GET"])
def get_historical_data():
    # Get historical data
    historical_data = energy_data.to_dict("records")
    return jsonify({"historical": historical_data})

if __name__ == "__main__":
    app.run(debug=True)
