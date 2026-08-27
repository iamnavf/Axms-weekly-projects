from flask import Flask, request,render_template, send_file
import numpy as np
import pandas as pd
import tensorflow as tf
import pickle
import keras
import io
from tensorflow.keras.preprocessing.sequence import pad_sequences


app = Flask(__name__)
with open(r"./notebook/tokenizer.pkl","rb") as handle:
    tokenizer = pickle.load(handle)

model = keras.models.load_model(r"./models/gru_early.keras")

df = pd.read_csv(r"./data/performance/result.csv")
df = df.to_dict(orient="records")

batch_results = None
@app.route("/")
def dashboard():

    return render_template("dashboard.html",performance=df)

@app.route("/prediction", methods=["GET", "POST"])
def prediction():

    sentiment = None
    confidence = None
    probabilities = None
    review = ""

    if request.method == "POST":

        review = request.form["review"]

        # Convert review into sequence
        sequence = tokenizer.texts_to_sequences([review])

        # Padding
        padded_sequence = pad_sequences(
            sequence,
            maxlen=200,
            padding="post",
            truncating="post"
        )

        # Prediction
        prediction = model.predict(padded_sequence)

        probability = float(prediction[0][0])

        # Sentiment
        if probability >= 0.5:
            sentiment = "Positive"
            confidence = probability * 100
        else:
            sentiment = "Negative"
            confidence = (1 - probability) * 100

        # Probabilities
        probabilities = {
            "positive": probability * 100,
            "negative": (1 - probability) * 100
        }

    return render_template("prediction.html",review=review,sentiment=sentiment,confidence=confidence,
                           probabilities=probabilities)

@app.route("/comparison")
def comparison():

    df_baseline = pd.read_csv(r"./data/performance/base_model_performance.csv").to_dict(orient="records")

    return render_template("comparison.html",performance=df,baseline_performance=df_baseline)

@app.route("/analytics")
def analytics():

    return render_template("analytics.html")

@app.route("/batch-prediction", methods=["GET", "POST"])
def batch_prediction():

    global batch_results
    results = None
    summary = None

    if request.method == "POST":

        file = request.files["file"]

        if file.filename == "":
            return render_template(
                "batch_prediction.html",
                error="Please select a CSV file."
            )

        data = pd.read_csv(file)

        # Get reviews from CSV
        reviews = data["review"].astype(str).tolist()

        # Tokenize
        sequences = tokenizer.texts_to_sequences(reviews)

        # Padding
        padded_sequences = pad_sequences(
            sequences,
            maxlen=200,
            padding="post",
            truncating="post"
        )

        # Prediction
        predictions = model.predict(padded_sequences)

        positive_probability = predictions.flatten()
        negative_probability = 1 - positive_probability

        # Sentiment
        sentiments = np.where(
            positive_probability >= 0.5,
            "Positive",
            "Negative"
        )

        # Add results
        data["Sentiment"] = sentiments
        data["Positive_Probability"] = positive_probability
        data["Negative_Probability"] = negative_probability

        # Summary
        total_reviews = len(data)
        positive_count = np.sum(sentiments == "Positive")
        negative_count = np.sum(sentiments == "Negative")

        summary = {
            "total": total_reviews,
            "positive": int(positive_count),
            "negative": int(negative_count)
        }

        results = data.to_dict(orient="records")

        batch_results = data

    return render_template("batch_prediction.html",results=results,summary=summary)


@app.route("/download-results")
def download_results():

    global batch_results
    if batch_results is None:
        return "No prediction results available."

    output = io.BytesIO()

    batch_results.to_csv(output,index=False)

    print(output)

    output.seek(0)



    return send_file(output,mimetype="text/csv",as_attachment=True,download_name="sentiment_predictions.csv")

if __name__ == "__main__":
    app.run()

                