from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import keras
import joblib

df = pd.read_csv(r"./data/cleaned/cleaned.csv")

df["Datetime"] = pd.to_datetime(df["Datetime"])

feature_scaler = joblib.load(r"./notebook/scaler.pkl")

target_scaler = joblib.load(r"./notebook/target_scaler.pkl")

model = keras.models.load_model(r'./models/gru_16.keras')

df_performance = pd.read_csv(r"./data/cleaned/performance.csv")

df_validation = pd.read_csv(r"./data/cleaned/validation_predictions.csv")

app = Flask(__name__)

@app.route("/")
def dashboard():
    latest_demand = df["PJME_MW"].iloc[-1]
    
    best_model = "GRU"
    best_mae = 1338.70
    best_rmse = 1915.71
    best_mape = 4.18
    best_r2 = 91.16
    
    forecast_horizon = 1
    forecast_demand = 30360
        
    return render_template("dashboard.html",latest_demand=latest_demand,best_model=best_model,forecast_demand=forecast_demand,
    best_mae=best_mae,best_rmse=best_rmse,best_mape=best_mape,best_r2=best_r2,forecast_horizon=forecast_horizon)

@app.route("/forecast", methods=["GET", "POST"])
def forecast():

    forecast_values = []
    forecast_labels = []
    lower_bounds = []
    upper_bounds = []
    horizon = 24

    if request.method == "POST":

        horizon = int(request.form["horizon"])

        if horizon != 24:
            return render_template("forecast.html",forecast_values=[],forecast_labels=[],lower_bounds=[],
                        upper_bounds=[],horizon=horizon,error="Currently only 24-hour forecasting is supported.")
            
        feature_cols = ["PJME_MW","year","month","hour","day_num","day_of_month","week_of_year",
                        "is_weekend","lag_1","lag_24","lag_168","rolling_mean_24","rolling_std_24"]

        latest_data = df.tail(24).copy()
        X_latest = latest_data[feature_cols]
        y_val_mw = latest_data["PJME_MW"]
        X_latest_scaled = feature_scaler.transform(X_latest)

        X_latest_seq = X_latest_scaled.reshape(1,24,13)

        print("Input shape:", X_latest_seq.shape)
        y_pred_scaled = model.predict(X_latest_seq)

        print("Prediction shape:",y_pred_scaled.shape)
        y_pred_mw = target_scaler.inverse_transform(y_pred_scaled.reshape(-1, 1)).flatten()
        print("Forecast shape:", y_pred_mw.shape)

        last_datetime = df["Datetime"].iloc[-1]
        future_dates = pd.date_range(start=last_datetime + pd.Timedelta(hours=1),periods=24,freq="h")
        forecast_labels = future_dates.strftime("%Y-%m-%d %H:%M").tolist()
        forecast_values = y_pred_mw.tolist()

        errors = (y_val_mw - y_pred_mw.flatten())
        lower_error = np.percentile(errors,5)
        upper_error = np.percentile(errors,95)
        lower_bounds = (y_pred_mw + lower_error).tolist()
        upper_bounds = (y_pred_mw + upper_error).tolist()

        print("Lower error:",lower_error)
        print("Upper error:",upper_error)
        return render_template("forecast.html",forecast_values=forecast_values,forecast_labels=forecast_labels,
                            lower_bounds=lower_bounds,upper_bounds=upper_bounds,horizon=horizon)
        
    return render_template("forecast.html",forecast_values=forecast_values,forecast_labels=forecast_labels,
                                lower_bounds=lower_bounds,upper_bounds=upper_bounds,horizon=horizon)
@app.route('/analytics')
def analytics():
   model_comparison = df_performance.to_dict(orient='records')
   best_model ='GRU'
   best_r2 = 91.16
   best_mae = 1338.70
   best_rmse = 1915.71
   return render_template("analytics.html",model_comparison=model_comparison,best_model=best_model,best_r2=best_r2,
                          best_mae =best_mae,best_rmse=best_rmse)

@app.route("/validation", methods=["GET", "POST"])
def validation():

    days = 30
    actual_values = []
    predicted_values = []
    mae = None
    rmse = None
    mape = None

    if request.method == "POST":
    
        days = int(request.form["days"])
        hours = days * 24
        actual = df_validation["Actual"].values[:hours]
        predicted = df_validation["Predicted"].values[:hours]
        mae = np.mean(np.abs(actual - predicted))
        rmse = np.sqrt(np.mean((actual - predicted) ** 2))
        mape = np.mean(np.abs((actual - predicted) / actual)) * 100

        actual_values = actual.tolist()
        predicted_values = predicted.tolist()
        
        return render_template("validation.html",days=days,actual_values=actual_values,
                                   predicted_values=predicted_values,mae=mae,rmse=rmse,mape=mape)

    return render_template("validation.html",days=days,actual_values=actual_values,
                           predicted_values=predicted_values,mae=mae,rmse=rmse,mape=mape)

if __name__ == "__main__":
    app.run()