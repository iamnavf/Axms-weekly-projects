from flask import Flask,render_template,redirect,url_for,request
import pandas as pd
import numpy as np
import keras
import tensorflow as tf

app = Flask(__name__)


df = pd.read_csv(r'./data/HAM10000_metadata.csv')
df_performance = pd.read_csv(r'./data/selected_col/performance.csv')
df_performance = df_performance.drop(columns='Unnamed: 0')
model = keras.models.load_model(r'./models/bmodel_cnn_RMS.keras')

@app.route('/')
def dashboard():
    model_table= df_performance.to_dict(orient='records')

    total_images = df.shape[0]
    total_classes =len(df['dx'].unique())
    best_model = 'batch normalization'
    test_accuracy = 79
    train_images = 7009
    validation_images =1503
    test_images =1503
    image_size = (650,450)
    validation_accuracy=67
    test_accuracy=78
    test_loss=0.78

    return render_template('dashboard.html',model_table=model_table,total_images=total_images,total_classes=total_classes,best_model=best_model,
                           test_accuracy=test_accuracy,train_images=train_images,validation_images=validation_images,
                           validation_accuracy=validation_accuracy,image_size=image_size,test_loss=test_loss,test_images=test_images)


@app.route('/diagnosis',methods=['GET','POST'])
def diagnosis():
  if request.method == 'POST':
    image = request.files.get("image")
    image = tf.image.decode_jpeg(image.read(),channels=3)
    image = tf.image.resize(image, (224,224))
    image = tf.cast(image, tf.float32) / 255.0
    image = tf.expand_dims(image, axis=0)

    prediction = model.predict(image)

    predict_score = prediction[0].tolist()

    predicted_class_idx = np.argmax(prediction)

    confidence = np.max(prediction)*100

    dx_class =['Actinic Keratoses','Basal Cell Carcinoma ','Benign Keratosis-like Lesions ',
               'Dermatofibroma','Melanoma','Melanocytic Nevi','Vascular Lesions']
    
    probabilities={}

    probabilities = {
        "class": dx_class,
        "score": predict_score
    }

    predicted_class = dx_class[predicted_class_idx]

    return render_template('diagnosis.html',predicted_class=predicted_class,confidence=confidence,
                           probabilities=probabilities)

  return render_template('diagnosis.html')


@app.route('/prediction')
def prediction():
    return render_template('prediction.html')

@app.route('/analytics')
def analytics():
    model_dict = df_performance.to_dict(orient='records')[0]
    model_table = df_performance.to_dict(orient='records')
    best_model = model_dict['MODEL']
    best_accuracy = model_dict['ACCURACY']
    lowest_loss = model_dict['LOSS']


    return render_template('analytics.html',model_table=model_table,best_model=best_model,best_accuracy = best_accuracy,lowest_loss =lowest_loss)

@app.route('/report')
def report():
    return render_template('report.html')


if __name__ == '__main__':
    app.run(debug = True)
