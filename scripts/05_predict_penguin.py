import requests  
import pandas as pd
import joblib
import json
import re
import os
import sqlite3
import datetime
import pytz

# Load the trained model from parent directory
current_dir = os.path.dirname(os.path.abspath(__file__))  # Get the current directory of this script
model_path = os.path.join(current_dir, '..', 'model', 'model.pkl')  # Path to model.pkl

# Check if the model file exists
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file not found at: {model_path}")

# Load the trained model
model = joblib.load(model_path)

# Load relevant features from the feature selection report
def load_relevant_features(file_path='../model/feature_selection_report.txt', top_n=4):
    feature_file_path = os.path.join(current_dir, '..', 'model', 'feature_selection_report.txt')
    
    if not os.path.exists(feature_file_path):
        raise FileNotFoundError(f"Feature selection report not found at: {feature_file_path}")

    rf_features = []
    
    with open(feature_file_path, 'r') as f:
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

# Get relevant features
relevant_features = load_relevant_features()
print(f"Relevant Features Used for Prediction: {relevant_features}")

# -------- Update Database Structure --------
db_path = os.path.join(current_dir, '..', 'database', 'penguins.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Ensure required columns are present in PENGUINS table
required_columns = ['species', 'bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 
                    'body_mass_g', 'datetime']
cursor.execute('PRAGMA table_info(PENGUINS);')
columns = cursor.fetchall()
existing_columns = [column[1] for column in columns]

# Add missing columns if necessary
for col in required_columns:
    if col not in existing_columns:
        try:
            cursor.execute(f"ALTER TABLE PENGUINS ADD COLUMN {col} TEXT;")
        except sqlite3.OperationalError:
            print(f"Column '{col}' already exists or cannot be added.")

conn.commit()  # Apply changes

# -------- Fetch Data from API --------
url = 'http://130.225.39.127:8000/new_penguin/'
response = requests.get(url)

if response.status_code == 200:
    try:
        penguin_data = response.json()
        
        if isinstance(penguin_data, dict):
            penguin_data = [penguin_data]
        
        penguins_df = pd.DataFrame(penguin_data)
        
        expected_columns = ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g', 'datetime']
        
        for col in expected_columns:
            if col not in penguins_df.columns:
                penguins_df[col] = None
        
        penguins_df = penguins_df[expected_columns]
        
        query = f"""
        SELECT * FROM PENGUINS 
        WHERE bill_length_mm = ? AND bill_depth_mm = ? 
        AND flipper_length_mm = ? AND body_mass_g = ? AND datetime = ?
        """
        
        cursor.execute(query, (penguins_df['bill_length_mm'][0], penguins_df['bill_depth_mm'][0],
                               penguins_df['flipper_length_mm'][0], penguins_df['body_mass_g'][0],
                               penguins_df['datetime'][0]))
        
        if cursor.fetchone():
            print("This Penguin is already processed.")
            conn.close()
            exit()

        if 'bill_length_mm' in penguins_df.columns and 'bill_depth_mm' in penguins_df.columns:
            penguins_df['bill_ratio'] = penguins_df['bill_length_mm'] / penguins_df['bill_depth_mm']
            penguins_df['bill_area'] = penguins_df['bill_length_mm'] * penguins_df['bill_depth_mm']
        
        if 'flipper_length_mm' in penguins_df.columns and 'body_mass_g' in penguins_df.columns:
            penguins_df['flipper_to_mass_ratio'] = penguins_df['flipper_length_mm'] / penguins_df['body_mass_g']
            penguins_df['size_index'] = penguins_df['flipper_length_mm'] * penguins_df['body_mass_g']
            penguins_df['mass_flipper_diff'] = penguins_df['body_mass_g'] - penguins_df['flipper_length_mm']
        
        X_new = penguins_df[relevant_features]

        # Make predictions using the trained model
        predictions = model.predict(X_new)
        # Get probabilities for all species
        prediction_probabilities = model.predict_proba(X_new)[0]

        # Find the index of the predicted class
        predicted_index = model.classes_.tolist().index(predictions[0])

        # Get the probability of the predicted class
        predicted_probability = prediction_probabilities[predicted_index] * 100  # Convert to percentage

        
        penguins_df['species'] = predictions
        
        print("\nClassified DataFrame:")
        print(penguins_df[['species']])
        
        penguins_df.to_sql('PENGUINS', conn, if_exists='append', index=False)
        
        conn.close()
        print("\nClassified results saved to the 'penguins.db' database.")
    
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from API response.")
else:
    print(f"Failed to fetch data from the API. Status Code: {response.status_code}")




# -------- Save to JSON Files for GitHub Pages --------
latest_json_path = os.path.join(current_dir, '..', 'public', 'latest_penguin.json')
all_predictions_json_path = os.path.join(current_dir, '..', 'public', 'predictions.json')

# Get the exact time of prediction in UTC format
utc_now = datetime.datetime.now(pytz.UTC)
prediction_time = utc_now.strftime("%Y-%m-%dT%H:%M:%S%z")

# Convert the original datetime to the same format if it's not already
if isinstance(penguins_df['datetime'][0], str):
    api_datetime = penguins_df['datetime'][0]
else:
    api_datetime = utc_now.strftime("%Y-%m-%dT%H:%M:%S%z")

# Prepare data to save
penguin_info = {
    "species": predictions[0],
    "confidence": round(predicted_probability, 2),
    "bill_length_mm": round(penguins_df['bill_length_mm'][0], 2),
    "bill_depth_mm": round(penguins_df['bill_depth_mm'][0], 2),
    "flipper_length_mm": round(penguins_df['flipper_length_mm'][0], 2),
    "body_mass_g": round(penguins_df['body_mass_g'][0], 2),
    "datetime": api_datetime,             # API-provided datetime formatted correctly
    "prediction_time": prediction_time    # Prediction time formatted correctly
}

# Save the latest penguin prediction to 'latest_penguin.json'
with open(latest_json_path, 'w') as latest_file:
    json.dump(penguin_info, latest_file, indent=4)
print(f"\nLatest penguin information saved to 'public/latest_penguin.json'.")

# Save all predictions to 'predictions.json'
if os.path.exists(all_predictions_json_path):
    with open(all_predictions_json_path, 'r') as all_file:
        try:
            all_predictions = json.load(all_file)
        except json.JSONDecodeError:
            all_predictions = []  # If the file is empty or corrupted, start fresh
else:
    all_predictions = []

# Append the new prediction to the list
all_predictions.append(penguin_info)

# Save the updated list back to the file
with open(all_predictions_json_path, 'w') as all_file:
    json.dump(all_predictions, all_file, indent=4)
print(f"\nPenguin information appended to 'public/predictions.json'.")
