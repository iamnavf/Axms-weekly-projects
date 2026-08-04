from flask import Flask,render_template,redirect,url_for,request,session
import pandas as pd
import numpy as np
import keras
import tensorflow as tf

from reportlab.platypus import SimpleDocTemplate, Paragraph ,  Table
from reportlab.lib.styles import getSampleStyleSheet
from flask import send_file

import os
from werkzeug.utils import secure_filename

from explain.gradcam import GradCAM


app = Flask(__name__)

app.secret_key = 'this is my app'

df = pd.read_csv(r'./data/HAM10000_metadata.csv')
df_performance = pd.read_csv(r'./data/selected_col/performance.csv')
df_performance = df_performance.drop(columns='Unnamed: 0')
model = keras.models.load_model(r'./models/dropout_rms.keras')

@app.route('/')
def dashboard():
    model_table= df_performance.to_dict(orient='records')

    total_images = df.shape[0]
    total_classes =len(df['dx'].unique())
    best_model = 'DROP OUT CNN'
    test_accuracy = 71
    train_images = 7009
    validation_images =1503
    test_images =1503
    image_size = (650,450)
    validation_accuracy=69
    test_accuracy=63
    test_loss=1.17

    return render_template('dashboard.html',model_table=model_table,total_images=total_images,
                           total_classes=total_classes,best_model=best_model,test_accuracy=test_accuracy,
                           train_images=train_images,validation_images=validation_images,
                           validation_accuracy=validation_accuracy,image_size=image_size,
                           test_loss=test_loss,test_images=test_images)


@app.route('/diagnosis',methods=['GET','POST'])
def diagnosis():
  if request.method == 'POST':

    image_file = request.files.get("image")


    filename = secure_filename(image_file.filename)
    upload_path = os.path.join("static/uploads", filename)

    image_file.save(upload_path)

    session["filename"] = filename

    image_bytes = tf.io.read_file(upload_path)
    image = tf.io.decode_image(image_bytes, channels=3)
    image = tf.image.resize(image, (224, 224))
    image = tf.cast(image, tf.float32) / 255.0
    image = tf.expand_dims(image, axis=0)

    prediction = model.predict(image)

    print("="*60)
    print("Filename :", filename)
    print("Prediction Vector :", prediction[0])
    print("Predicted Index :", np.argmax(prediction))
    print("Confidence :", np.max(prediction)*100)
    print("="*60)

    predict_score = prediction[0].tolist()

    predicted_class_idx = int(np.argmax(prediction))

    confidence = np.max(prediction)*100

    dx_class =['Actinic Keratoses','Basal Cell Carcinoma ','Benign Keratosis-like Lesions ',
               'Dermatofibroma','Melanoma','Melanocytic Nevi','Vascular Lesions']
    
    probabilities={}

    probabilities = {
        "class": dx_class,
        "score": predict_score
    }

    predicted_class = dx_class[predicted_class_idx]

    print(upload_path)

    return render_template('diagnosis.html',predicted_class=predicted_class,confidence=confidence,
                           probabilities=probabilities)

  return render_template('diagnosis.html')


@app.route('/prediction')
def prediction():

    filename = session.get("filename")

    if filename is None:
        return redirect(url_for("diagnosis"))

    upload_path = os.path.join("static", "uploads", filename)

    gradcam_path = os.path.join("static", "gradcam", filename)

    gradcam = GradCAM(r'./models/dropout_rms.keras')

    result = gradcam.generate(
        image_path=upload_path,
        save_path=gradcam_path
    )

    explanation = (
        f"The model predicted '{result['prediction']}' because it focused "
        "mainly on the highlighted lesion region. The red and yellow "
        "areas contributed the most to the final prediction."
    )
    session["prediction"] = result["prediction"]

    session["confidence"] = result["confidence"]

    session["probabilities"] = result["probabilities"]

    session["gradcam"] = "gradcam/" + filename

    print(result)

    return render_template("prediction.html",image_path="uploads/" + filename,gradcam_path="gradcam/" + filename,
            prediction=result["prediction"],confidence=result["confidence"],probabilities=result["probabilities"],
            explanation=explanation,model_name="Dropout CNN")

@app.route('/analytics')
def analytics():
    model_dict = df_performance.to_dict(orient='records')[3]
    model_table = df_performance.to_dict(orient='records')
    best_model = model_dict['MODEL']
    best_accuracy = model_dict['ACCURACY']
    lowest_loss = 1.17


    return render_template('analytics.html',model_table=model_table,best_model=best_model,best_accuracy = best_accuracy,lowest_loss =lowest_loss)

@app.route('/report')
def report():
    return render_template('report.html')


@app.route("/diagnosis_report")
def diagnosis_report():

    filename = "Diagnosis_Report.pdf"
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("<b>Skin Disease Diagnosis Report</b>", styles["Title"]))
    story.append(Paragraph(f"<b>Prediction:</b> {session.get('prediction')}",styles["Normal"]))

    confidence = session.get("confidence", 0.0)

    story.append(Paragraph(f"<b>Confidence:</b> {float(confidence):.2f} %",styles["Normal"])) 
    doc.build(story)

    return send_file(filename,as_attachment=True)


@app.route("/model_comparison_report")
def model_comparison_report():

    styles = getSampleStyleSheet()

    filename = "Model_Comparison_Report.pdf"

    doc = SimpleDocTemplate(filename)

    story = []

    story.append(Paragraph("<b>Skin Disease Classification</b>",styles["Title"]))
    story.append(Paragraph("<b>Model Comparison Report</b>",styles["Heading1"]))


    data = [

        ["Model", "Accuracy", "Loss"],

        ["Baseline CNN", "0.48", "1.34"],

        ["Deep CNN", "0.65", "1.91"],

        ["CNN + BatchNorm", "0.50", "1.70"],

        ["CNN + Dropout", "0.46", "1.35"],

        ["MobileNetV2", "0.61", "0.96"],

        ["EfficientNetB0", "0.67", "0.74"],

        ["ResNet50", "0.66", "1.21"],

        ["DenseNet121", "0.58", "1.07"]]

    table = Table(data)

    story.append(table)
    story.append(Paragraph("<br/><b>Observation</b>", styles["Heading2"]))

    story.append(
        Paragraph(
            "Dropout CNN achieved the highest validation accuracy "
            "(67%) with the lowest validation loss (1.17), making it "
            "the best-performing architecture among all evaluated models. "
            "Therefore, EfficientNetB0 was selected as the final model "
            "for skin disease diagnosis and Explainable AI analysis.",
            styles["BodyText"]))

    doc.build(story)
    return send_file(filename,as_attachment=True)


if __name__ == '__main__':
    app.run()
