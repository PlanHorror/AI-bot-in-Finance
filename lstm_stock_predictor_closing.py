import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler

def window_data(df, window, feature_col_number, target_col_number):
    X, y = [], []
    for i in range(len(df) - window - 1):
        features = df.iloc[i:(i + window), feature_col_number]
        target = df.iloc[(i + window), target_col_number]
        X.append(features)
        y.append(target)
    return np.array(X), np.array(y).reshape(-1, 1)

def load_and_prepare_data(price_file, fng_file, window_size=1):
    # Load data with correct date format
    price_data = pd.read_csv(price_file, parse_dates=['Date'], index_col='Date', dayfirst=False)  # Assume mm/dd/yyyy
    fng_data = pd.read_csv(fng_file, parse_dates=['date'], index_col='date', dayfirst=True)  # dd/mm/yyyy
    fng_data = fng_data.drop(columns="fng_classification")
    # Standardize date format for both datasets
    fng_data.index = pd.to_datetime(fng_data.index, format='%d/%m/%Y')
    price_data.index = pd.to_datetime(price_data.index, format='%m/%d/%Y')

    # Sort fng_data in ascending order
    fng_data = fng_data.sort_index()

    # Debug: Print the date ranges of the data
    print("Price Data Date Range:", price_data.index.min(), "to", price_data.index.max())
    print("FNG Data Date Range:", fng_data.index.min(), "to", fng_data.index.max())

    # Merge data
    df = fng_data.join(price_data['Close'], how='inner')
    
    # Debug: Print the first few rows of the merged data
    print("Merged Data:")
    print(df.head())
    
    # Prepare data
    feature_column = 1  # Fear and Greed index
    target_column = 1   # Close price
    X, y = window_data(df, window_size, feature_column, target_column)
    
    # Debug: Print the shapes of X and y
    print("X shape:", X.shape)
    print("y shape:", y.shape)
    
    # Check if X and y are not empty
    if X.size == 0 or y.size == 0:
        raise ValueError("X or y array is empty. Please check your data.")
    
    # Split data
    split = int(0.7 * len(X))
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]
    
    # Scale data
    feature_scaler = MinMaxScaler()
    target_scaler = MinMaxScaler()
    
    X_train_scaled = feature_scaler.fit_transform(X_train)
    X_test_scaled = feature_scaler.transform(X_test)
    y_train_scaled = target_scaler.fit_transform(y_train)
    y_test_scaled = target_scaler.transform(y_test)
    
    # Reshape for LSTM
    X_train_reshaped = X_train_scaled.reshape((X_train_scaled.shape[0], X_train_scaled.shape[1], 1))
    X_test_reshaped = X_test_scaled.reshape((X_test_scaled.shape[0], X_test_scaled.shape[1], 1))
    
    return {
        'X_train': X_train_reshaped,
        'X_test': X_test_reshaped,
        'y_train': y_train_scaled,
        'y_test': y_test_scaled,
        'feature_scaler': feature_scaler,
        'target_scaler': target_scaler,
        'original_data': df
    }

def build_lstm_model(input_shape):
    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=input_shape),
        Dropout(0.2),
        LSTM(50, return_sequences=True),
        Dropout(0.2),
        LSTM(50),
        Dropout(0.2),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def app(price_file, fng_file, pk):
    # Prepare data
    data = load_and_prepare_data(price_file, fng_file)

    # Build and train model
    model = build_lstm_model((data['X_train'].shape[1], 1))
    model.fit(data['X_train'], data['y_train'], 
              epochs=15, batch_size=1, shuffle=False, verbose=1)

    # Predict
    predictions_scaled = model.predict(data['X_test'])

    # Check if predictions_scaled is not empty
    if predictions_scaled.size == 0:
        raise ValueError("predictions_scaled array is empty. Please check your data.")

    # Inverse transform
    predictions = data['target_scaler'].inverse_transform(predictions_scaled)
    real_prices = data['target_scaler'].inverse_transform(data['y_test'])

    # Get the dates corresponding to the test set
    test_dates = data['original_data'].index[-len(real_prices):]

    # Debug: Print the dates being used for plotting
    print("Real Prices Date Range:", test_dates.min(), "to", test_dates.max())

    # Visualize
    plt.figure(figsize=(12, 6))
    plt.plot(test_dates, real_prices, label="Thực tế")
    plt.plot(test_dates, predictions, label="Dự đoán")
    plt.title("Dự Đoán Giá Tiền Điện Tử")
    plt.xlabel("Thời Gian")
    plt.ylabel("Giá")
    plt.legend()
    result_path = f'media/image/result_{pk}.png'
    plt.savefig(result_path)
    plt.close()

    return f'image/result_{pk}'
