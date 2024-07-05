import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import xgboost as xgb
import tensorflow as tf

class DemandResponseModel:
    def __init__(self, data):
        self.data = data

    def preprocess_data(self):
        # Preprocess data
        self.data['date'] = pd.to_datetime(self.data['date'])
        self.data['hour'] = self.data['date'].dt.hour
        self.data['day_of_week'] = self.data['date'].dt.dayofweek
        self.data['month'] = self.data['date'].dt.month
        self.data['year'] = self.data['date'].dt.year
        self.data.drop('date', axis=1, inplace=True)

    def train_random_forest(self):
        # Train random forest model
        X = self.data.drop('demand', axis=1)
        y = self.data['demand']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
        rf_model.fit(X_train, y_train)
        y_pred = rf_model.predict(X_test)
        print(f'Random Forest MSE: {mean_squared_error(y_test, y_pred):.4f}')

    def train_xgboost(self):
        # Train XGBoost model
        X = self.data.drop('demand', axis=1)
        y = self.data['demand']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        xgb_model = xgb.XGBRegressor(objective='reg:squarederror', max_depth=6, learning_rate=0.1, n_estimators=1000)
        xgb_model.fit(X_train, y_train)
        y_pred = xgb_model.predict(X_test)
        print(f'XGBoost MSE: {mean_squared_error(y_test, y_pred):.4f}')

    def train_neural_network(self):
        # Train neural network model
        X = self.data.drop('demand', axis=1)
        y = self.data['demand']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = tf.keras.models.Sequential([
            tf.keras.layers.Dense(64, activation='relu', input_shape=(X.shape[1],)),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(1)
        ])
        model.compile(optimizer='adam', loss='mean_squared_error')
        model.fit(X_train, y_train, epochs=100, batch_size=32, validation_data=(X_test, y_test))
        y_pred = model.predict(X_test)
        print(f'Neural Network MSE: {mean_squared_error(y_test, y_pred):.4f}')

if __name__ == '__main__':
    # Load data
    data = pd.read_csv('demand_response_data.csv')

    # Create model
    model = DemandResponseModel(data)

    # Preprocess data
    model.preprocess_data()

    # Train models
    model.train_random_forest()
    model.train_xgboost()
    model.train_neural_network()
