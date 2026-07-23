from flask import Flask,render_template,request

import pandas as pd

app = Flask(__name__)

df = pd.read_csv(r"./data/cleaned/cleand_train.csv")
#home
@app.route("/")
def home():
    total_rows= df.shape[0]
    total_col = df.shape[1]

    return render_template(total_rows=total_rows,total_col=total_col)
    

#module
@app.route("/prediction")
def model():
    pass

#comparasion
@app.route("/comparasion")
def comparasion():
    pass

#analytics
@app.route("/analytics")
def analytics():
    pass

#report
@app.route("/report")
def report():
    pass

if __name__ =="__main__":
    app.run(debug=True)