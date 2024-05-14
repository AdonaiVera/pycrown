import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Load preprocessed data
preprocessed_data = pd.read_csv("data/preprocessed_brainwave_data_features.csv")

# Separate features and labels
X = preprocessed_data.drop('label', axis=1)
y = preprocessed_data['label']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a RandomForest Classifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Predict on the test set
y_pred = clf.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

classification_report_str = classification_report(y_test, y_pred)
print("Classification Report:")
print(classification_report_str)

# Save the trained model
model_filename = "model/meditation_classifier.pkl"
joblib.dump(clf, model_filename)
print(f"Trained model saved as {model_filename}")

# Optionally save the evaluation report to a text file
report_filename = "model/classification_report.txt"
with open(report_filename, "w") as report_file:
    report_file.write(f"Accuracy: {accuracy}\n\n")
    report_file.write("Classification Report:\n")
    report_file.write(classification_report_str)
print(f"Classification report saved as {report_filename}")
