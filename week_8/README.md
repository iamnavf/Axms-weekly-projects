Electricity Demand Forecasting System

This project presents an Electricity Demand Forecasting System developed using Time-Series Forecasting and Deep Learning. The system predicts future electricity demand using historical consumption data and compares multiple forecasting models.

The trained model is deployed using a Flask web application for forecasting, analytics, and validation.

Features

Dashboard

* Latest electricity demand
* Best model performance
* Forecast summary

Forecasting

* Generate 24-hour demand forecast
* Display forecast values
* Display forecast intervals
* Maximum and minimum forecast demand

Analytics

* Actual vs Forecast
* Daily, weekly and monthly trends
* Peak demand analysis
* Forecast error analysis
* Model comparison

Validation

* 30-day and 60-day validation
* Actual vs Predicted demand
* MAE, RMSE and MAPE

Models

* Naive
* Moving Average
* RNN
* LSTM
* GRU
* Bi-LSTM

Best Deep Learning Model:GRU

* MAE: 1338.70 MW
* RMSE: 1915.71 MW
* MAPE: 4.18%
* R²: 91.16%

Project Phases

1. Data Understanding
2. Data Preprocessing
3. EDA
4. Baseline Models
5. Model Development
6. Model Improvement & Tuning
7. Model Validation
8. Model Evaluation
9. Forecasting Dashboard

Project Structure
week_8/
│
├── app.py
│
├── data/
│   └── cleaned/
│       ├── cleaned.csv
│       ├── performance.csv
│       ├── test.csv
│       ├── train.csv
│       ├── val.csv
│       └── validation_predictions.csv
│   └──raw/
│       ├── PJME.csv
│       ├── APE.csv
│       ├── COMED.csv
│       ├── DAYTON.csv
│       ├── DEOK.csv
│       ├── DOM.csv
│       ├── DUQ.csv
│       ├── EKPC.csv
│       ├── FE.csv
│       ├── NI.csv
│       ├── pjm.csv
│       ├── PJM_Load.csv
│       └── PJMW.csv
│
│
├── notebook/
│   ├── scaler.pkl
│   ├── baseline_model.ipynb
│   ├── bilstm.ipynb
│   ├── comparaison.ipynb
│   ├── data_understanding.ipynb
│   ├── EDA.ipynb
│   ├── gru_improvement.ipynb
│   ├── improvement.ipynb
│   ├── lstm_improvement.ipynb
│   ├── model_development.ipynb
│   ├── phase_7.ipynb
│   ├── preprocessing.ipynb
│   └── target_scaler.pkl
│   models/
│   └── gru_16.keras
│   hyper_tuning/
│   rnn_tuning/
│   
│
├── static/
│   └── css/
│       └──style.css
│   └── images/
│       ├── ac_vs_pr.png
│       ├── 30_day.png
│       ├── day.png
│       ├── weekly.png
│       ├── monthly.png
│       ├── demand.png
│       └── forecast.png
│
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── forecast.html
│   ├── analytics.html
│   └── validation.html
│
├── pipfile
├── pipfile.lock
├── summary.txt
├── week_8.docx
│
└── README.md

Model Improvement

Model performance was improved through different experiments, including:

Dropout
Batch Normalization
Optimizer selection
Learning-rate adjustment
Early stopping
Batch-size experiments
Number of recurrent layers
Hyperparameter tuning

Different configurations were tested to determine the most effective model setup.

The best deep learning configuration was the GRU model, which was selected for integration into the forecasting dashboard.


Tech Stack

Programming Language - Python
Deep Learning - TensorFlow, Keras
Machine Learning - Scikit-learn
Data Processing - Pandas, NumPy
Visualization - Matplotlib, Seaborn
Web Development - Flask, HTML, CSS, Bootstrap