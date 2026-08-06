This project presents a Skin Disease Classification System developed using Deep Learning and Explainable Artificial Intelligence (XAI). The system classifies dermoscopic skin lesion images into seven disease categories using Dropout CNN, provides visual explanations through Grad-CAM, and deploys the model using a Flask web application.

The application allows users to upload a skin lesion image, receive a predicted disease class, confidence score, probability distribution, Grad-CAM heatmap, model analytics, and downloadable PDF reports.

Features
Dashboard
Dataset summary
Training, Validation and Test statistics
Model comparison
Performance overview

Image Diagnosis
Upload skin lesion image
Predict disease class
Display confidence score
Display probability of all classes

Explain Prediction
Generate Grad-CAM heatmap
Highlight affected lesion region
Visual explanation of prediction
Confidence score visualization

Model Analytics
Accuracy Comparison
Loss Comparison
ROC Curves
Confusion Matrix
Performance Summary

Reports

Generate downloadable PDF reports.

Diagnosis Report

Contains:
Predicted Disease
Confidence Score
Probability Table
Prediction Explanation


Model Comparison Report

Contains:

Model Performance
Model explanation

Dataset

Dataset Name

HAM10000 (Human Against Machine with 10000 Training Images)

Technologies Used

Programming Language
Python

Deep Learning
TensorFlow
Keras

Transfer Learning
MobileNetV2
EfficientNetB0
ResNet50
DenseNet121
Machine Learning
Scikit-learn

Image Processing
OpenCV
NumPy

Data Visualization
Matplotlib
Seaborn

Web Development
Flask
HTML
CSS
Bootstrap

Report Generation
ReportLab

Models Developed

Custom CNN Models
Basic CNN
Deep CNN
CNN with Batch Normalization
CNN with Dropout

Transfer Learning Models

MobileNetV2
EfficientNetB0
ResNet50
DenseNet121

Model Improvement Techniques

Image Augmentation
Batch Normalization
Dropout
Early Stopping
Learning Rate Scheduling
Hyperparameter Tuning
Fine-Tuning
Optimizer Comparison
Batch Size Comparison

Explainable AI

The project integrates Grad-CAM to explain the model predictions.

Grad-CAM provides:

Heatmap generation
Highlighted lesion region
Visual explanation
Increased model transparency

PROJECT STRUCTURE

WEEK 7
│
├── app.py
├── gitignore
├── pipfile
├── pipfile.lock
│
├── explain/
│   └── gradcam.py
│
├── models/
│   └── hyper_effecient.keras
│ 
├── notebook/
│   ├── data preprocessing.ipynb
│   ├── data understanding.ipynb
│   ├── densenet.ipynb
│   ├── effecientnet.ipynb
│   ├── metrices.ibpynb
│   ├── mobilnet.ipynb
│   ├── modeldevelopment.ipynb
│   ├── model improvement.ibpynb
│   └── resnet.ipynb
│
├── static/
│   ├── css/
│   ├── uploads/
│   ├── gradcam/
│   └── images/
│
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── diagnosis.html
│   ├── prediction.html
│   ├── analytics.html
│   └── report.html
│
├── data/
│   ├── HAM10000_metadata.csv
│   └── performance.csv
│
└── README.md