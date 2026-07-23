from flask import Flask,render_template,request,redirect,url_for

import joblib


import pandas as pd
import numpy as np

app = Flask(__name__)

df = pd.read_csv(r"./data/cleaned/cleand_train.csv")

df_train =pd.read_csv(r"./data/predict_feature/featured_columns")

df_model = pd.read_csv(r"./data/predict_feature/performsnce.csv")

model = joblib.load(r"./model/model.pkl")

#home
@app.route("/")
def dashboard():
    total_rows= df.shape[0]
    total_col = df.shape[1]

    trained_feature = df_train.shape[1]

    total_model = df_model.shape[1]

    return render_template("dashboard.html",total_rows=total_rows,total_col=total_col,
                           trained_feature=trained_feature,total_model=total_model)
    

#prediction module
@app.route("/prediction",methods =["GET","POST"])
def prediction():
    if request.method == "POST":
        #getting the 10 user input
        overall_quality = int(request.form.get("OverallQual"))
        total_sq = float(request.form.get("TotalSf"))#model tained by it as float
        ground_living =int(request.form.get("GrLivArea"))
        floor_sq = int(request.form.get("1stFlrSF"))
        lot_area = int( request.form.get("LotArea"))
        total_living = float(request.form.get("TotalLivArea"))#model tained by it as float
        total_bathroom = float(request.form.get("TotalBathrooms"))#model tained by it as float
        year_built = int(request.form.get("YearBuilt"))
        houseage = int(request.form.get("HouseAge"))
        GarageArea = int(request.form.get("GarageArea"))

        #these are being skewd in the cleaning
        ground_living = np.log1p(ground_living)
        floor_sq = np.log1p(floor_sq)
        lot_area = np.log1p(lot_area)

        #creating dictionary
        sample_data = {
                        "OverallQual":[overall_quality],
                        "TotalSf": [total_sq],
                        "GrLivArea": [ground_living],
                        "1stFlrSF": [floor_sq],
                        "LotArea": [lot_area],
                        "TotalLivArea": [total_living],
                        "TotalBathrooms": [total_bathroom],
                        "YearBuilt":[year_built],
                        "HouseAge": [houseage],
                        "GarageArea":  [GarageArea]
                    }
        df = pd.DataFrame(sample_data)#data frmes with created dictionary

        result = model.predict(df)#predicting the result
        result = f"{result}"

        return redirect(url_for("prediction",Result=result))

    return render_template("prediction.html")

#comparasion
@app.route("/comprasion")
def comprasion():
    return render_template("comprasion.html")

#analytics
@app.route("/analytics")
def analytics():
    return render_template("analytics.html")

#report
@app.route("/report")
def report():
    return render_template("report.html")

if __name__ =="__main__":
    app.run(debug=True)