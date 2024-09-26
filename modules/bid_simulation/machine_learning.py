# BidOptimizerPro/modules/bid_simulation/machine_learning.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def train_bid_model(data, model_path='bid_success_model.pkl'):
    """
    Trains a machine learning model to predict bid success.

    Args:
        data (pd.DataFrame): Processed bid data.
        model_path (str): Path to save the trained model.

    Returns:
        None
    """
    # Feature Engineering: Example features
    data['hour'] = pd.to_datetime(data['timestamp']).dt.hour
    features = ['bid_amount', 'hour']
    X = data[features]
    y = data['is_won']

    # Split Data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Model Training
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluation
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    logging.info(f"Model Accuracy: {accuracy:.2f}")

    # Save Model
    joblib.dump(model, model_path)
    logging.info(f"Model saved to {model_path}")

def load_model(model_path='bid_success_model.pkl'):
    """
    Loads the trained machine learning model.

    Args:
        model_path (str): Path to the trained model.

    Returns:
        model: Loaded machine learning model.
    """
    if not os.path.exists(model_path):
        logging.error(f"Model file not found at {model_path}. Please train the model first.")
        return None
    model = joblib.load(model_path)
    logging.info(f"Model loaded from {model_path}")
    return model

def predict_bid_success(model, bid_amount, hour):
    """
    Predicts the success of a bid.

    Args:
        model: Trained machine learning model.
        bid_amount (float): Amount of the bid.
        hour (int): Hour of the day when the bid is placed.

    Returns:
        bool: Prediction of bid success.
    """
    prediction = model.predict(pd.DataFrame({'bid_amount': [bid_amount], 'hour': [hour]}))
    return bool(prediction[0])
