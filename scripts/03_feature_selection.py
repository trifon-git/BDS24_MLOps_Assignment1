import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectKBest, f_classif

# Connect to the original SQLite database
conn = sqlite3.connect('database/penguins.db')
query = 'SELECT * FROM PENGUINS'
penguins = pd.read_sql(query, conn)
conn.close()

# Define all relevant features including the newly created ones
features = [
    'bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g', 
    'bill_ratio', 'flipper_to_mass_ratio', 'bill_area', 'size_index', 'mass_flipper_diff'
]

# Extract features and labels
X = penguins[features]
y = penguins['species']

# Check for missing values and clean the data
if X.isnull().values.any() or y.isnull().any():
    print("Cleaning the data...")
    valid_data = penguins.dropna(subset=features + ['species'])
    X = valid_data[features]
    y = valid_data['species']
    print("Data cleaned successfully.")

# 1. Correlation Analysis
correlation_matrix = X.corr()
plt.figure(figsize=(12, 10))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Enhanced Feature Correlation Matrix')
plt.savefig('model/enhanced_correlation_matrix.png')
plt.close()

# 2. Feature Importance (Using RandomForestClassifier)
rf_model = RandomForestClassifier(random_state=42)
rf_model.fit(X, y)
rf_importances = rf_model.feature_importances_

# Plot feature importances for RandomForest
plt.figure(figsize=(10, 6))
sns.barplot(x=rf_importances, y=X.columns)
plt.title('Feature Importance (RandomForest)')
plt.xlabel('Importance')
plt.ylabel('Features')
plt.savefig('model/rf_feature_importance.png')
plt.close()

# 3. Feature Selection using SelectKBest
selector = SelectKBest(score_func=f_classif, k='all')
selector.fit(X, y)
feature_scores = selector.scores_

# Save feature importance scores to a file
with open('model/feature_selection_report.txt', 'w') as f:
    f.write("Feature Importance Scores (RandomForestClassifier):\n")
    for name, score in zip(X.columns, rf_importances):
        f.write(f"{name}: {score}\n")

    f.write("\nFeature Scores (SelectKBest):\n")
    for name, score in zip(X.columns, feature_scores):
        f.write(f"{name}: {score}\n")

print("Feature selection complete. Reports saved to 'model/' folder.")
