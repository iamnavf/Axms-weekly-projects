IMDb Movie Review Sentiment Analysis

An end-to-end Natural Language Processing and Deep Learning project that classifies IMDb movie reviews as Positive or Negative using ANN, RNN, LSTM, GRU, and BiLSTM models.

Project Overview

This project implements a complete sentiment-analysis pipeline:

IMDb Dataset
     ↓
Data Understanding
     ↓
Text Preprocessing
     ↓
Feature Representation
     ↓
Deep Learning Models
     ↓
Model Improvement
     ↓
Evaluation & Comparison
     ↓
Flask Deployment

Objectives

Analyze and preprocess movie reviews.
Convert text into numerical representations.
Build multiple deep learning models.
Compare model performance.
Improve models through hyperparameter tuning.
Analyze model errors.
Deploy the best model using Flask.
Support real-time and batch sentiment prediction.

IMDb Movie Reviews Dataset

Total reviews: 50,000
Classes: Positive and Negative
Binary classification problem.

Data Split

| Dataset    | Samples |
| ---------- | ------: |
| Training   |  34,705 |
| Validation |   7,439 |
| Testing    |   7,438 |

Labels:

text
Negative → 0
Positive → 1


Phase 1 – Data Understanding

The dataset was analyzed for:

* Dataset structure
* Data types
* Missing values
* Duplicate records
* Sentiment distribution
* Review length
* Word frequency

Phase 2 – Text Preprocessing

The reviews were cleaned using the following pipeline:

text
Raw Review
    ↓
Lowercase
    ↓
Remove HTML Tags
    ↓
Remove Punctuation
    ↓
Stopword Handling
    ↓
Tokenization
    ↓
Cleaned Review


A cleaned_review column was created to store the processed reviews.

Phase 3 – Feature Representation

Tokenization & Integer Encoding

A vocabulary size of 20,000 was used.

text
VOCAB_SIZE = 20000


Reviews were converted into integer sequences.

Sequence Padding

A maximum sequence length of 200 was selected.

text
MAX_LEN = 200


Final shapes:

text
X_train → (34705, 200)
X_val   → (7439, 200)
X_test  → (7438, 200)

TF-IDF

TF-IDF was implemented with:

Maximum features: 20,000
N-gram range: (1, 2)

TF-IDF Results

| Metric    |  Score |
| --------- | -----: |
| Accuracy  | 90.09% |
| Precision | 88.97% |
| Recall    | 91.62% |
| F1 Score  | 90.27% |

Word Embedding

An embedding-based representation was also evaluated.

| Metric    |  Score |
| --------- | -----: |
| Accuracy  | 85.33% |
| Precision | 84.62% |
| Recall    | 86.50% |
| F1 Score  | 85.55% |



Phase 4 – Deep Learning Models

Five architectures were implemented:

ANN

text
Embedding → Global Average Pooling → Dense → Output


RNN

text
Embedding → Simple RNN → Dense → Output

LSTM

text
Embedding → LSTM → Dense → Output


GRU

text
Embedding → GRU → Dense → Output


BiLSTM

text
Embedding → Bidirectional LSTM → Dense → Output


Each model was:

* Trained
* Evaluated
* Used for prediction
* Saved for later use

 Phase 5 – Model Improvement

The following techniques were investigated:

* Embedding dimension tuning
* Sequence length tuning
* Hidden units
* Dropout
* Recurrent dropout
* Batch normalization
* Adam optimizer
* RMSprop optimizer
* SGD optimizer
* Learning-rate tuning
* Batch-size tuning
* Early stopping
* Learning-rate scheduling

Hidden-unit configurations included:

text
32
128


Dropout configurations included:

text
0.3
0.5


Some dropout experiments significantly reduced performance, with F1 scores around 0.12–0.15, so those configurations were not selected for the final model.

Phase 6 & 7 – Evaluation & Model Comparison

The models were evaluated using:

* Accuracy
* Precision
* Recall
* F1 Score
* ROC-AUC
* Confusion Matrix
* ROC Curve
* Precision-Recall Curve
* Training/Validation Curves
* Misclassified Review Analysis


Flask Web Application
    Dashboard
    Sentiment Prediction
    Model Comparison
    Text Analytics
    Batch Prediction

#Technologies Used

* Python
* TensorFlow / Keras
* Scikit-learn
* Pandas
* NumPy
* NLTK
* Matplotlib
* WordCloud
* Flask
* HTML
* CSS


#Project Structure

sentiment-analysis/
│
├── app.py
├── models/
├── baseline_model/
├── data/
│   ├── raw/
│   ├── cleaned/
│   ├── seq/
│   └── performance/
├── log/
├── static/
│   ├── css/
│   │    └── style.css
│   └── images/
│ 
├── templates/
│   ├── dashboard.html
│   ├── base.html
│   ├── prediction.html
│   ├── comparison.html
│   ├── analytics.html
│   └── batch_prediction.html
│ 
├── notebooks/
│   ├── phase_1
│   ├── phase_2
│   ├── phase_3
│   ├── phase_4
│   ├── phase_ann_5
│   ├── phase_rnn_5
│   ├── phase_lstm_5
│   ├── phase_bilstm_5
│   ├── phase_gru_5
│   └──  phase_6_7
│ 
├── .gitignore
├── pipfile
├── pipfile.lock
├── requirements.txt
├── WEEK 10 Sentiment Analysis.odt
└── README.md



