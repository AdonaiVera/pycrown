import pandas as pd
import numpy as np
from scipy.signal import welch
from sklearn.preprocessing import StandardScaler
import joblib
import warnings

# Suppress specific warnings
warnings.filterwarnings("ignore", message="X does not have valid feature names")
warnings.filterwarnings("ignore", message="nperseg = 256 is greater than input length")

class MeditationClassifier:
    def __init__(self, model_path, scaler_path):
        # Load the trained model
        self.clf = joblib.load(model_path)
        
        # Load the scaler used during training
        self.scaler = joblib.load(scaler_path)

    @staticmethod
    def baseline_correction(data):
        return data - np.mean(data)
    
    @staticmethod
    def extract_statistical_features(row):
        mean = np.mean(row)
        variance = np.var(row)
        skewness = pd.Series(row).skew()
        kurtosis = pd.Series(row).kurt()
        return [mean, variance, skewness, kurtosis]
    
    @staticmethod
    def extract_psd_features(row, fs=256.0):
        psd_features = []
        f, Pxx = welch(row, fs, nperseg=256)
        psd_features.extend(Pxx[:13])  # Keep first 13 frequency bins as features
        return psd_features
    
    def preprocess_data(self, new_data):
        # Convert the new data to a DataFrame
        new_data_df = pd.DataFrame([new_data])
        
        # Apply baseline correction
        new_data_corrected = self.baseline_correction(new_data_df.iloc[0])
        
        # Normalize the data using the scaler
        new_data_normalized = self.scaler.transform([new_data_corrected])
        
        # Extract features
        statistical_features = self.extract_statistical_features(new_data_normalized[0])
        psd_features = self.extract_psd_features(new_data_normalized[0])
        
        # Combine all features
        features = statistical_features + psd_features
        
        # Convert to DataFrame for consistency with the trained model
        features_df = pd.DataFrame([features])
        
        return features_df
    
    def predict(self, new_data):
        # Preprocess the data
        features_df = self.preprocess_data(new_data)
        
        # Make prediction
        prediction = self.clf.predict(features_df)
        
        return prediction[0]
    
    def predict_proba(self, new_data):
        # Preprocess the data
        features_df = self.preprocess_data(new_data)
        
        # Get prediction probabilities
        probabilities = self.clf.predict_proba(features_df)
        
        return probabilities[0]