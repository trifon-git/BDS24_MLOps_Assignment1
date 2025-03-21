# 🐧 Penguins of Madagascar Classifier

## 📖 Project Overview  
The **Penguins of Madagascar Classifier** is a machine learning project designed to classify penguin species from the famous Penguins of Madagascar series. This classifier is deployed as a fun, interactive webpage that displays the latest penguin detection with fancy animations, modern design, and playful visuals.  

---

## 📂 Project Structure  
The repository is organized as follows:  

```
BDS24_MLOps_Assignment1/
│
├── .github/
│ └── workflows/
│ └── fetch_and_predict.yml # GitHub Action to fetch data, predict species, and update database
│
├── database/
│ └── penguins.db # SQLite database storing penguin data
│
├── model/
│ ├── enhanced_correlation_matrix.png
│ ├── evaluation_report.txt
│ ├── feature_selection_report.txt
│ ├── model.pkl # Trained RandomForest model
│ └── rf_feature_importance.png
│
├── public/
│ ├── index.html # Animated webpage for predictions
│ ├── predictions.json # JSON file storing all predictions over time
│ ├── scripts.js # JavaScript code handling page interactions and animations
│ └── styles.css # Styling for the webpage
│
├── scripts/
│ ├── 01_create_database.py # Create initial database from Seaborn dataset
│ ├── 02_feature_engineering.py # Add new features to the dataset
│ ├── 03_feature_selection.py # Select relevant features for training
│ ├── 04_train_model.py # Train the RandomForest model
│ └── 05_predict_penguin.py # Fetch new data, predict and store results
│
├── README.md # Project documentation
├── requirements.txt # Python dependencies
└── vercel.json # Vercel configuration for deployment
```

---
## 📌 Setup Instructions
1. **Clone the Repository:**
```bash
git clone https://github.com/trifon-git/BDS24_MLOps_Assignment1.git
```
2.**Navigate to the Project Directory:**
```bash
cd BDS24_MLOps_Assignment1

```
3.**Install Dependencies:**
```bash
pip install -r requirements.txt
```
4.**Run the Scripts in Order::**
```bash
python scripts/01_create_database.py
python scripts/02_feature_engineering.py
python scripts/03_feature_selection.py
python scripts/04_train_model.py
```
5.**Running the Prediction Script:**
-To manually run the prediction script:
```bash
python scripts/05_predict_penguin.py
```
## 🌐 Deployment
1. Create a vercel.json file for Vercel deployment.
2. Deploy the public folder to Vercel.
3. The site will be live and update daily via GitHub Actions.


## 🚀 Technologies Used
- **Python** (Version: 3.12)
- **Scikit-Learn**: For model training and evaluation (RandomForest Classifier)
- **Pandas**: Data manipulation and processing
- **NumPy**: Numerical operations
- **SQLite**: Database to store predictions
- **Matplotlib & Seaborn**: For visualizations and feature importance graphs
- **JavaScript (Vanilla)**: Handling animations and interactions on the webpage
- **HTML/CSS**: Designing the UI for predictions
- **GitHub Actions**: Automating the prediction process
- **Vercel**: Deploying the web interface

---

## 📊 Methods Applied
1. **Data Preparation**
   - Data is collected from the Seaborn penguins dataset.
   - Missing values are handled by removing rows with missing entries.
   - New features are generated (e.g., bill ratio, bill area, flipper-to-mass ratio).

2. **Feature Selection**
   - A RandomForest Classifier is trained to identify the most important features.
   - The top 4 most relevant features are selected for final model training:
     - `bill_ratio`
     - `flipper_length_mm`
     - `bill_length_mm`
     - `size_index`
   - Feature importance scores are saved in the `feature_selection_report.txt`.

3. **Model Training**
   - A RandomForest Classifier is trained with the most relevant features.
   - **Hyperparameters** used for training:
     - `n_estimators`: 100
     - `max_depth`: None
     - `min_samples_split`: 2
     - `min_samples_leaf`: 1
     - `random_state`: 42
   - The trained model is saved as `model.pkl`.

4. **Prediction**
   - New data is fetched from the API daily.
   - The model predicts the species of the penguin.
   - The prediction is stored in two JSON files:
     - `latest_penguin.json`: Stores the most recent prediction.
     - `predictions.json`: Stores all predictions over time with timestamps.
   - The results are also stored in the `penguins.db` SQLite database.

5. **Evaluation**
   - Model evaluation is performed using standard classification metrics.
   - **Accuracy Score:** 0.96 (96%)
   - Evaluation results are saved in the `evaluation_report.txt`.

6. **Data Normalization & Resampling**
   - The training data is normalized before model training.
   - **Random UnderSampling** is applied to handle class imbalance.

---

## 🌟 Features
- Dynamic prediction of penguin species with animated web interface.
- Automated daily data fetching and prediction process via GitHub Actions.
- Data visualization of feature importance and prediction probabilities.
- Storage of all predictions in a SQLite database and JSON files.
- User-friendly web interface with playful design inspired by *Penguins of Madagascar*.

---
