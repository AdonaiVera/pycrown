import pandas as pd
import numpy as np
from scipy.signal import welch
from sklearn.preprocessing import StandardScaler
import joblib

# Load your data
data = pd.read_csv("data/brainwave_data_band.csv")

# Baseline Correction
def baseline_correction(data):
    return data - data.mean()

# Apply preprocessing
data.iloc[:, :-1] = baseline_correction(data.iloc[:, :-1])  # Exclude the label column

# Normalize the data
scaler = StandardScaler()
data.iloc[:, :-1] = scaler.fit_transform(data.iloc[:, :-1])

# Save the scaler
scaler_filename = "model/scaler.pkl"
joblib.dump(scaler, scaler_filename)
print(f"Scaler saved as {scaler_filename}")


# Feature Extraction: Statistical Features
def extract_statistical_features(row):
    mean = np.mean(row)
    variance = np.var(row)
    skewness = pd.Series(row).skew()
    kurtosis = pd.Series(row).kurt()
    return [mean, variance, skewness, kurtosis]

# Feature Extraction: Power Spectral Density
def extract_psd_features(row, fs=256.0):
    psd_features = []
    f, Pxx = welch(row, fs, nperseg=256)
    psd_features.extend(Pxx[:13])  # Keep first 13 frequency bins as features
    return psd_features

# Apply feature extraction
statistical_features = data.iloc[:, :-1].apply(extract_statistical_features, axis=1)
statistical_features_df = pd.DataFrame(statistical_features.tolist(), columns=['mean', 'variance', 'skewness', 'kurtosis'])

psd_features = data.iloc[:, :-1].apply(lambda row: extract_psd_features(row), axis=1)
psd_features_df = pd.DataFrame(psd_features.tolist())

# Combine all features
features_df = pd.concat([statistical_features_df, psd_features_df], axis=1)
features_df['label'] = data['label']

# Save preprocessed and feature-extracted data
features_df.to_csv("data/preprocessed_brainwave_data_features.csv", index=False)

print("Preprocessing and feature extraction completed. Preprocessed data saved to 'data/preprocessed_brainwave_data_features.csv'.")
