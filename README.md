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
│   └── workflows/
│       └── fetch_and_predict.yml   # GitHub Action to fetch data, predict species, and update database
│
├── database/
│   └── penguins.db                 # SQLite database storing penguin data
│
├── model/
│   ├── model.pkl                   # Trained RandomForest model
│   ├── feature_selection_report.txt
│   └── evaluation_report.txt
│
├── scripts/
│   ├── 01_create_database.py
│   ├── 02_feature_engineering.py
│   ├── 03_feature_selection.py
│   ├── 04_train_model.py
│   └── 05_predict_penguin.py
│
├── docs/
│   ├── index.html                  # Fancy, animated webpage for predictions
│   ├── style.css                   # Styling for the webpage
│   └── latest_penguin.json         # JSON file storing the latest prediction
│
├── README.md                       # Project documentation
├── requirements.txt                # Python dependencies
└── notebook.ipynb                  # Jupyter Notebook for development
```

---

## 🚀 How It Works  
1. **Data Collection**: Data is fetched from a live API providing penguin measurements.  
2. **Feature Engineering**: Features like `bill_ratio`, `size_index`, etc., are calculated.  
3. **Model Training**: A RandomForest model is trained using the most important features.  
4. **Prediction**: Predictions are made using the trained model and stored in the database and JSON file.  
5. **Web Display**: The prediction is displayed on a modern, animated webpage.  

---

## 🔧 Installation  
1. Clone the repository:  
```bash
git clone https://github.com/trifon-git/BDS24_MLOps_Assignment1.git
cd BDS24_MLOps_Assignment1
```

2. Install dependencies:  
```bash
pip install -r requirements.txt
```

---

## 📖 Usage  
1. Train the model by running:  
```bash
python scripts/04_train_model.py
```

2. Predict using the API by running:  
```bash
python scripts/05_predict_penguin.py
```

3. To view the prediction, go to your GitHub Pages URL.  

---

## 🌟 GitHub Actions  
- Automated workflow fetches new penguin data daily and updates the prediction page at 7:30 AM UTC.  
- Defined in `.github/workflows/fetch_and_predict.yml`.  

---

## 🌈 Webpage Design  
- Designed using HTML. 
- Displayed using GitHub Pages.  

---

## 💡 Technologies Used  
- Python (Pandas, Scikit-Learn, Joblib, SQLite)  
- JavaScript, HTML, CSS (Styled according to the `Penguins of Madagascar` color palette)  
- GitHub Actions for automation  
- GitHub Pages for hosting the interactive webpage  

---
🐧✨
