House Price Prediction System using Machine Learning
Overview

The House Price Prediction System is a Machine Learning-based web application developed using Python, CatBoost, and Flask. The system predicts the selling price of a residential property based on user-provided house features. It also provides model analysis, comparison dashboards, analytics, and downloadable reports.

The project uses the  Housing Dataset from Kaggle and compares multiple regression algorithms to identify the best-performing model. After evaluation, the CatBoost Regressor was selected as the final deployment model.

Features
House price prediction
Interactive Flask dashboard
Dataset overview
Model comparison dashboard
Analytics dashboard
Feature importance visualization
Actual vs Predicted analysis
Residual analysis
Download Prediction Report (PDF)
Download Model Evaluation Report (PDF)
Download Model Comparison Report (PDF)


House-Price-Prediction/
│
├── app.py
├── requirements.txt
├── model/
│   ├── model.pkl
│   ├── model_feature.pkl
|   └── ordianl_encoder.pkl
│
├── data/
|   ├── raw/
│   │   ├── train.csv
│   │   └── test.csv
|   ├── cleaned/
│   │   ├── cleaned_train.csv
│   │   └── cleaned_test.csv
|   ├── encoded/
│   │   ├── encoded_train.csv
│   │   └── encoded_test.csv
|   ├── predict_feature/
│   │   ├── featured_column.csv
│   │   ├── performance.csv
│   │   └── featured_test_column.csv
|   └── selected/
│       ├── selected_tarin.csv
│       ├── tarin_y.csv
│       └── selected_test.csv
│
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── prediction.html
│   ├── comparison.html
│   ├── analytics.html
│   └── report.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── images/
│
├── notebook/
│   ├── data_cleaning.ipynb
│   ├── EDD.ipynb
│   ├── model_development.ipynb
│   ├── best_model.ipynb
│   └── data_understanding.ipynb
└── README.md

stack used
    Programming Language
    Python 3.12
    Machine Learning
    CatBoost
    Scikit-Learn
    XGBoost
    LightGBM
    Pandas
    NumPy
    Data Visualization
    Matplotlib
    Seaborn
    Web Framework
    Flask
    Frontend
    HTML5
    CSS3
    Bootstrap
    Font Awesome
    Report Generation
    ReportLab

Machine Learning Workflow
    Business Understanding
    Dataset Understanding
    Data Cleaning
    Missing Value Handling
    Feature Engineering
    Feature Selection
    Exploratory Data Analysis
    Model Building
    Hyperparameter Tuning
    Model Comparison
    Model Evaluation
    Flask Deployment

Models Compared
    Linear Regression
    Decision Tree Regressor
    Random Forest Regressor
    Gradient Boosting Regressor
    XGBoost Regressor
    LightGBM Regressor
    CatBoost Regressor

Final Model

CatBoost Regressor

Evaluation Metrics

R² Score: 0.9062
MAE: Best among all models
MSE: Lowest among all models
RMSE: Lowest among all models

The CatBoost model achieved the highest prediction accuracy and was selected as the final deployment model.


Input Features

The deployed model uses the following features:

Overall Quality
Total Square Footage
Ground Living Area
First Floor Area
Lot Area
Total Living Area
Total Bathrooms
Year Built
House Age
Garage Area


Application Modules
    Dashboard
        Dataset overview
        Total records
        Total features
        Selected model
        Model performance summary
    Prediction
        Enter property details
        Predict house price
        Display prediction result
    Model Comparison
        Compare regression models
        Evaluation metrics
        Best model identification
    Analytics
        Correlation heatmap
        Feature distributions
        Feature importance
        Actual vs Predicted plot
        Residual plot
    Reports
        Prediction Report
        Model Evaluation Report
        Model Comparison Report

Python Libraries
Flask
Pandas
NumPy
Matplotlib
Seaborn
Scikit-Learn
CatBoost
XGBoost
LightGBM
Joblib
ReportLab