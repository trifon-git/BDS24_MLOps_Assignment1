import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder
from imblearn.under_sampling import RandomUnderSampler
import joblib
import numpy as np
import re

# Load top features from feature_selection_report.txt
def load_top_features(file_path='model/feature_selection_report.txt', top_n=4):
    rf_features = []
    
    with open(file_path, 'r') as f:
        content = f.read()

    # Extract RandomForest top features
    rf_section = re.findall(r"Feature Importance Scores \(RandomForestClassifier\):([\s\S]*?)\n\n", content)
    if rf_section:
        rf_features = sorted(
            [(line.split(':')[0].strip(), float(line.split(':')[1].strip())) for line in rf_section[0].strip().split('\n')],
            key=lambda x: x[1], reverse=True
        )[:top_n]
    
    # Return only the feature names
    rf_features = [feature[0] for feature in rf_features]

    return rf_features

# Get top 4 features from feature selection report
rf_features = load_top_features()
print(f"Top 4 Features from RandomForest: {rf_features}")

# Connect to the original SQLite database
conn = sqlite3.connect('database/penguins.db')
query = 'SELECT * FROM PENGUINS'
penguins = pd.read_sql(query, conn)
conn.close()

# Extract relevant features and labels
X = penguins[rf_features]
y = penguins['species']

# Check for missing values and clean the data
if X.isnull().values.any() or y.isnull().any():
    print("Cleaning the data...")
    penguins = penguins.dropna(subset=rf_features + ['species'])
    X = penguins[rf_features]
    y = penguins['species']
    print("Data cleaned successfully.")

# Check original class distribution
print("Original Class Distribution:")
print(y.value_counts())

# Apply RandomUnderSampler
rus = RandomUnderSampler(random_state=42)
X_resampled, y_resampled = rus.fit_resample(X, y)

# Check new class distribution
print("\nNew Class Distribution After RandomUnderSampler:")
print(pd.Series(y_resampled).value_counts())

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)

# Define the model
model = RandomForestClassifier(random_state=42)

# Simplified hyperparameters for quicker search
param_dist = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5],
    'min_samples_leaf': [1, 2],
    'max_features': ['sqrt', 'log2'],
    'bootstrap': [True],
    'criterion': ['gini', 'entropy'],
    'class_weight': [None, 'balanced']
}

# Perform GridSearchCV for hyperparameter tuning
grid_search = GridSearchCV(
    model, param_grid=param_dist,
    cv=5, verbose=2, n_jobs=-1
)

# Train the model with hyperparameter tuning
grid_search.fit(X_train, y_train)
best_model = grid_search.best_estimator_

# Save the trained model
joblib.dump(best_model, 'model/model.pkl')

# Get the best cross-validation accuracy
cv_accuracy = grid_search.best_score_ * 100
print(f"\nCross-Validation Accuracy: {cv_accuracy:.2f}%")

# Make predictions on the test set
y_pred = best_model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
classification_rep = classification_report(y_test, y_pred)

# Display evaluation results
print(f"\nModel Accuracy on Test Set: {accuracy * 100:.2f}%")
print("\nClassification Report on Test Set:\n")
print(classification_rep)

# Save the evaluation report to a file
with open('model/evaluation_report.txt', 'w') as f:
    f.write(f"Cross-Validation Accuracy: {cv_accuracy:.2f}%\n")
    f.write(f"\nModel Accuracy on Test Set: {accuracy * 100:.2f}%\n\n")
    f.write("Classification Report on Test Set:\n")
    f.write(classification_rep)

print("Model training, tuning, and evaluation complete. Model and report saved.")
