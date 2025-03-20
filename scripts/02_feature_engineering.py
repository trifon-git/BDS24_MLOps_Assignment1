import sqlite3
import pandas as pd

# Connect to the original SQLite database
conn = sqlite3.connect('database/penguins.db')
query = 'SELECT * FROM PENGUINS'
penguins = pd.read_sql(query, conn)

# Feature selection
features = ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g']
X = penguins[features]
y = penguins['species']

# Check for missing values and clean the data
if X.isnull().values.any() or y.isnull().any():
    print("Cleaning the data...")
    valid_data = penguins.dropna(subset=features + ['species'])
    X = valid_data[features]
    y = valid_data['species']
    print("Data cleaned successfully.")

# Create new features
penguins['bill_ratio'] = X['bill_length_mm'] / X['bill_depth_mm']
penguins['flipper_to_mass_ratio'] = X['flipper_length_mm'] / X['body_mass_g']
penguins['bill_area'] = X['bill_length_mm'] * X['bill_depth_mm']
penguins['size_index'] = X['flipper_length_mm'] * X['body_mass_g']
penguins['mass_flipper_diff'] = X['body_mass_g'] - X['flipper_length_mm']

# Save the enhanced dataset to the original database
penguins.to_sql('PENGUINS', conn, if_exists='replace', index=False)
conn.close()

print("Feature engineering complete. Enhanced dataset saved to the original 'penguins.db' database.")
