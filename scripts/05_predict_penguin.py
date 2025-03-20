import requests  
import pandas as pd
import joblib
import json
import re
import os
import sqlite3

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
        # Load the response as JSON
        penguin_data = response.json()
        
        # If the response is a single dictionary, convert it to a list
        if isinstance(penguin_data, dict):
            penguin_data = [penguin_data]
        
        # Convert the data to a DataFrame
        penguins_df = pd.DataFrame(penguin_data)
        
        # Assign proper column names if they aren't present
        expected_columns = ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g', 'datetime']
        
        # Reorder or fill missing columns with None
        for col in expected_columns:
            if col not in penguins_df.columns:
                penguins_df[col] = None
        
        # Reorder columns to match expected structure
        penguins_df = penguins_df[expected_columns]
        
        # -------- Check If Penguin Already Processed --------
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
            exit()  # Exit the script as this penguin is already processed.

        # -------- Feature Engineering --------
        if 'bill_length_mm' in penguins_df.columns and 'bill_depth_mm' in penguins_df.columns:
            penguins_df['bill_ratio'] = penguins_df['bill_length_mm'] / penguins_df['bill_depth_mm']
            penguins_df['bill_area'] = penguins_df['bill_length_mm'] * penguins_df['bill_depth_mm']
        
        if 'flipper_length_mm' in penguins_df.columns and 'body_mass_g' in penguins_df.columns:
            penguins_df['flipper_to_mass_ratio'] = penguins_df['flipper_length_mm'] / penguins_df['body_mass_g']
            penguins_df['size_index'] = penguins_df['flipper_length_mm'] * penguins_df['body_mass_g']
            penguins_df['mass_flipper_diff'] = penguins_df['body_mass_g'] - penguins_df['flipper_length_mm']
        
        # -------- Classification Process --------
        # Filter the DataFrame to include only relevant features for prediction
        X_new = penguins_df[relevant_features]

        # Make predictions using the trained model
        predictions = model.predict(X_new)
        
        # Overwrite the 'species' column with the predicted species
        penguins_df['species'] = predictions
        
        # Display the classified DataFrame
        print("\nClassified DataFrame:")
        print(penguins_df[['species']])
        
        # -------- Save to Database --------
        penguins_df.to_sql('PENGUINS', conn, if_exists='append', index=False)
        
        conn.close()
        print("\nClassified results saved to the 'penguins.db' database.")
    
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from API response.")
else:
    print(f"Failed to fetch data from the API. Status Code: {response.status_code}")

import json

# Save prediction to prediction.txt for GitHub Pages
with open(os.path.join(current_dir, '..', 'prediction.txt'), 'w') as f:
    f.write(f"Predicted species: {predictions[0]}")

# -------- Save to JSON File for GitHub Pages --------
json_file_path = os.path.join(current_dir, '..','docs','latest_penguin.json')

# Prepare data to save
penguin_info = {
    "species": predictions[0],
    "bill_length_mm": penguins_df['bill_length_mm'][0],
    "bill_depth_mm": penguins_df['bill_depth_mm'][0],
    "flipper_length_mm": penguins_df['flipper_length_mm'][0],
    "body_mass_g": penguins_df['body_mass_g'][0],
    "datetime": penguins_df['datetime'][0]
}

# Save the data to JSON file
with open(json_file_path, 'w') as json_file:
    json.dump(penguin_info, json_file, indent=4)

print(f"\nPenguin information saved to 'latest_penguin.json'")
