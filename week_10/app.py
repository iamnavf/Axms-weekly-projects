from flask import Flask, render_template, request

from src.integration import (
    customer_profile_tool,
    predict_churn,
    get_shap_explanation,
    customer_agent
)


app = Flask(__name__)


#HOME PAGE


@app.route("/")
def home():

    return render_template(
        "home.html",
        customer=None,
        error=None
    )


@app.route("/profile", methods=["POST"])
def profile():

    customer_id = request.form.get("customer_id")

    customer = customer_profile_tool(customer_id)

    error = None

    if customer:

        customer = customer[0]

    else:

        customer = None

        error = f"Customer ID '{customer_id}' was not found."


    return render_template(
        "home.html",
        customer=customer,
        error=error
    )



#PREDICTION PAGE


@app.route("/prediction", methods=["GET", "POST"])
def prediction():

    prediction = None
    shap_features = None
    error = None

    if request.method == "POST":

        customer_id = request.form.get("customer_id")

        # Check whether customer exists
        customer = customer_profile_tool(customer_id)

        if not customer:

            error = f"Customer ID '{customer_id}' was not found."

        else:

            prediction = predict_churn(customer_id)

            shap_features = get_shap_explanation(customer_id)


    return render_template(
        "prediction.html",
        prediction=prediction,
        shap_features=shap_features,
        error=error
    )



#AI ASSISTANT PAGE


@app.route("/assistant", methods=["GET", "POST"])

def assistant():

    ai_response = None

    error = None

    if request.method == "POST":

        customer_id = request.form.get("customer_id").strip()

        question = request.form.get("question").strip()

        if not question:

            error = "Please enter a question."

        else:
            
            ai_response = customer_agent(customer_id, question)

    return render_template(
        "assistant.html",
        ai_response=ai_response,
        error=error
    )


#RUN APPLICATION


if __name__ == "__main__":

    app.run()