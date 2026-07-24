from flask import Flask,render_template,request,send_file

import joblib

from reportlab.platypus import (SimpleDocTemplate,Paragraph,Spacer,Table)

from reportlab.lib.styles import getSampleStyleSheet

import os

import pandas as pd
import numpy as np


styles = getSampleStyleSheet()

style = styles["Normal"]

report_data ={}

app = Flask(__name__)

df = pd.read_csv(r"./data/cleaned/cleand_train.csv")

df_train =pd.read_csv(r"./data/predict_feature/featured_columns.csv")

df_model = pd.read_csv(r"./data/predict_feature/performance.csv",index_col=0)

model = joblib.load(r"./model/model.pkl")

#home
@app.route("/")
def dashboard():
    total_rows= df.shape[0]
    total_col = df.shape[1]

    trained_feature = df_train.shape[1]

    total_model = df_model.shape[1]
    catboost_dict = df_model['catboost'].to_dict()

    model_dict = df_model.to_dict()

    

    return render_template("dashboard.html",total_rows=total_rows,total_col=total_col,
                           trained_feature=trained_feature,total_model=total_model,catboost_dict=catboost_dict,model_dict=model_dict)
    

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

        global report_data
        report_data={"overall-quality":overall_quality,"total_sq":total_sq,
            "ground_living":ground_living,
            "floor_sq":floor_sq,
            "lot_area":lot_area,
            "total_living":total_living,
            "total-bathroom":total_bathroom,
            "year_built":year_built,
            "houseage":houseage,
            "garageage":GarageArea}

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

        result = model.predict(df)[0]#predicting the result
       
        if result<50:
             result = np.expm1(result)
        else:
            result=result


        formated_result =f"{result:,.2f}"

        columns = df_train.columns[0:5].tolist()
        report_data["prediction"]=formated_result
        return render_template("prediction.html",predicted_result=formated_result)
    
    #result =request.args.get("Result")
    return render_template("prediction.html")  #"""predicted_result=result"""

#comparasion
@app.route("/comprasion")
def comprasion():
    model_dict = df_model.to_dict()
    catboost_dict = df_model['catboost'].to_dict()
    return render_template("comprasion.html",model_dict=model_dict,catboost_dict=catboost_dict)

#analytics
@app.route("/analytics")
def analytics():
    total_col = df_train.shape[1]
    high_related =df_train.columns
    high_related=high_related[0]
    return render_template("analytics.html",total_col=total_col,high_related=high_related)

#report
@app.route("/report")
def report():
    return render_template("report.html")

@app.route("/report/prediction")
def prediction_report():

    pdf = SimpleDocTemplate("prediction_report.pdf")

    data = []

    data.append(Paragraph("House Price Prediction Report", style))
    data.append(Spacer(1,20))
    data.append(Paragraph(f"Predicted Price : ${report_data["prediction"]}", style))
    data.append(Paragraph(f"Overall Quality : {report_data["overall-quality"]}", style))
    data.append(Paragraph(f"Ground Living Area : {report_data['ground_living']}", style))
    data.append(Paragraph(f"Lot Area : {report_data['lot_area']}", style))
    pdf.build(data)
    return send_file(
        "prediction_report.pdf",
        as_attachment=True
    )

@app.route("/report/evaluation")
def download_evaluation():
    pdf = SimpleDocTemplate("evaluation_report.pdf")
    story=[]
    catboost_dict = df_model['catboost'].to_dict()
    story.append(Paragraph("Model Evaluation Report",styles["Title"]))
    story.append(Paragraph(f"R² : {catboost_dict['r2']}",styles["Normal"]))
    story.append(Paragraph(f"MAE : {catboost_dict['mae']}",styles["Normal"]))
    story.append(Paragraph(f"MSE : {catboost_dict['mse']}",styles["Normal"]))
    story.append(Paragraph(f"RMSE : {catboost_dict['rmse']}",styles["Normal"]))
    pdf.build(story)
    return send_file("evaluation_report.pdf",as_attachment=True)

if __name__ =="__main__":
    app.run()





