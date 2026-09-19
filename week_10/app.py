from flask import Flask, render_template,request

from src.integration import (customer_profile_tool,predict_churn,get_shap_explanation,
    search_knowledge_base,customer_agent)

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/profile", methods=["POST"])
def profile():
    customer_id = request.form["customer_id"]

    customer = customer_profile_tool(customer_id)

    if customer:
        customer = customer[0]
    else:
        customer = None

    return render_template("home.html", customer=customer)


@app.route("/prediction", methods=["GET", "POST"])
def prediction():
    if request.method == "POST":
        customer_id = request.form["customer_id"]

        prediction_result = predict_churn(customer_id)
        shap_result = get_shap_explanation(customer_id)

        return render_template("prediction.html",customer_id=customer_id,prediction=prediction_result,
                               shap_features=shap_result)

    return render_template("prediction.html")


@app.route("/assistant", methods=["GET", "POST"])
def assistant():
    if request.method == "POST":
        customer_id = request.form["customer_id"]
        question = request.form["question"]

        ai_response = customer_agent(customer_id, question)

        return render_template("assistant.html",ai_response=ai_response)

    return render_template("assistant.html")


if __name__ == "__main__":
    app.run()