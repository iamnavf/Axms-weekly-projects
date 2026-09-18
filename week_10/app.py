from flask import Flask, render_template, request

from src.integration import (
    customer_profile_tool,
    predict_churn,
    get_shap_explanation,
    search_knowledge_base,
    customer_agent
)

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    customer_id = request.form["customer_id"]
    question = request.form["question"]

    # Customer profile
    profile_result = customer_profile_tool(customer_id)

    if not profile_result:
        return "Customer not found"

    customer = profile_result[0]

    # Churn prediction
    prediction = predict_churn(customer_id)

    churn_probability = prediction["churn_probability"]

    if churn_probability >= 0.70:
        risk_level = "High"
    elif churn_probability >= 0.40:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    model_prediction = (
        "Likely to Churn"
        if prediction["churn_prediction"] == 1
        else "Not Likely to Churn"
    )

    # SHAP explanation
    shap_result = get_shap_explanation(customer_id)

    # Knowledge base
    knowledge_result = search_knowledge_base(question)

    # AI response
    ai_response = customer_agent(customer_id, question)

    return render_template(
        "result.html",
        customer=customer,
        churn_probability=churn_probability,
        risk_level=risk_level,
        model_prediction=model_prediction,
        shap_features=shap_result.split("\n"),
        churn_reasons=shap_result.split("\n"),
        question=question,
        ai_response=ai_response
    )


if __name__ == "__main__":
    app.run(debug=True)