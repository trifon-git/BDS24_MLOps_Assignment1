import seaborn as sns
import pandas as pd
import sqlite3

# Load the penguins dataset from Seaborn
penguins = sns.load_dataset("penguins").dropna()
penguins.info()

# Create a connection to a new SQLite database
conn = sqlite3.connect('database/penguins.db')
cursor = conn.cursor()

# Create tables according to the schema
cursor.execute('''
    CREATE TABLE IF NOT EXISTS ISLANDS (
        island_id INTEGER PRIMARY KEY,
        name TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS PENGUINS (
        species TEXT,
        bill_length_mm REAL,
        bill_depth_mm REAL,
        flipper_length_mm REAL,
        body_mass_g REAL,
        sex TEXT,
        island_id INTEGER,
        animal_id INTEGER PRIMARY KEY,
        FOREIGN KEY (island_id) REFERENCES ISLANDS (island_id)
    )
''')

# Extract unique island names and insert them into the ISLANDS table
islands = pd.DataFrame(penguins['island'].unique(), columns=['name'])
islands['island_id'] = range(1, len(islands) + 1)
islands.to_sql('ISLANDS', conn, if_exists='replace', index=False)

# Map island names to island_ids
island_map = dict(zip(islands['name'], islands['island_id']))
penguins['island_id'] = penguins['island'].map(island_map)

# Drop the original 'island' column and reset index
penguins = penguins.drop(columns=['island'])
penguins.reset_index(drop=True, inplace=True)

# Insert penguins data into the PENGUINS table
penguins.to_sql('PENGUINS', conn, if_exists='replace', index=False)

# Close the connection
conn.close()

print("Database 'penguins.db' successfully created with the local dataset.")
