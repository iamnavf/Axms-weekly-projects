AI Customer Intelligence Platform

This project presents an AI Customer Intelligence Platform developed using Data Analytics, Machine Learning, Explainable AI, NLP, Semantic Search, RAG, and Generative AI. The system analyzes customer information, predicts churn risk, explains predictions, retrieves support knowledge, and generates natural-language responses.

The trained models and integrated AI workflow are deployed using a Flask web application for customer analysis, churn prediction, and AI-assisted customer interaction.

Features

Customer Analytics

* Customer data analysis
* Churn analysis
* SQL-based customer analysis
* Customer segmentation
* Revenue-related analysis

Machine Learning

* Churn prediction
* Multiple model comparison
* Class imbalance handling
* Feature engineering
* Feature selection
* Model evaluation

Explainable AI

* SHAP-based model explanation
* Global feature importance
* Customer-level churn explanation
* Identification of important churn factors

NLP

* Text preprocessing
* Tokenization
* Stopword removal
* TF-IDF
* Text classification
* Sentence embeddings

Semantic Search

* Customer support ticket embeddings
* Knowledge-base embeddings
* FAISS vector search
* Semantic similarity search

RAG

* Knowledge-base retrieval
* Context generation
* Retrieval-Augmented Generation
* Local knowledge-based responses

Generative AI

* Local LLM
* Prompt engineering
* Tool calling
* Simple agent workflow
* GenAI evaluation

Flask Application

* Customer search
* Churn prediction
* SHAP explanation
* AI assistant
* Error handling

Models

Machine Learning Models

* Logistic Regression
* Decision Tree
* K-Nearest Neighbors
* Random Forest
* Gradient Boosting
* XGBoost

Deep Learning Model

* Artificial Neural Network

NLP Models

* TF-IDF
* all-MiniLM-L6-v2

Generative AI Model

* Qwen/Qwen2.5-1.5B-Instruct

Final Churn Model

Weighted Gradient Boosting

* Accuracy: 74.45%
* Precision: 51.21%
* Recall: 79.14%
* F1 Score: 62.18%
* ROC-AUC: 84.11%
* PR-AUC: 65.83%


Project Structure

AI-Customer-Intelligence-Platform/
│
├── app.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── knowledge_base/
│
├── models/
│   ├── model.pkl
│   ├── top_15_features.pkl
│   ├── top_15_indices.pkl
│   ├── ticket_data.pkl
│   ├── ticket_faiss.index
│   ├── kb_faiss.index
│   ├── kb_chunks.pkl
│   └── all-MiniLM-L6-v2/
│
├── notebooks/
│   ├── data_understanding.ipynb
│   ├── eda.ipynb
│   ├── sql_analysis.ipynb
│   ├── embedding_faiss.ipynb
│   ├── evaluation.ipynb
│   ├── explainable_ai.ipynb
│   ├── preprocessing.ipynb
│   ├── feature_engineering.ipynb
│   ├── ml_models.ipynb
│   ├── ann.ipynb
│   ├── nlp.ipynb
│   ├── customer_inlelligence_db.ipynb
│   ├── scaler.pkl
│   ├── encoder.pkl
│   └── rag_llm.ipynb
│
├── src/
│   └── integration.py
│
├── static/
│   └── css/
│       └── style.css
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── prediction.html
│   └── assistant.html
│
├── Pipfile
├── Pipfile.lock
├── requirement.txt
├── customer ai intelligence assistant.odt
└── README.md

Model Improvement

Model performance was improved through different experiments, including:

* Class imbalance handling
* Sample weighting
* Threshold analysis
* Feature selection
* Hyperparameter tuning
* Model comparison
* Cross-validation

The weighted Gradient Boosting model with the selected top 15 features was used as the final churn model.

Explainable AI

SHAP was used to understand the factors contributing to individual churn predictions.

Important features included:

* Contract risk
* Tenure
* Service combination risk
* Monthly charges
* Internet service
* Total charges
* Charge-to-tenure ratio
* Payment method risk

RAG and Semantic Search

Customer support tickets and knowledge-base documents were converted into embeddings using all-MiniLM-L6-v2.

* Ticket embeddings: 8469
* Embedding dimensions: 384
* Knowledge-base documents: 104
* Knowledge-base embeddings: 104
* Vector database: FAISS

Local LLM

The project uses:

Qwen/Qwen2.5-1.5B-Instruct

The local LLM is used for natural-language generation while factual calculations remain with the ML, SHAP, SQL, and RAG components.

Flask Application

The Flask application contains three main pages:

Home

* Customer search
* Customer information

Prediction

* Churn probability
* Churn prediction
* SHAP explanation

AI Assistant

* Customer questions
* Tool calling
* RAG
* Local LLM response

Resource Benchmarking

Model loading times were measured to understand the system's resource requirements.

* ML model: 0.1689 seconds
* Embedding model: 1.8535 seconds
* LLM: 33.3578 seconds

RAG retrieval time, end-to-end response time, and approximate RAM usage were also measured.

Tech Stack

Programming Language - Python

Data Processing - Pandas, NumPy

Data Analysis - Pandas, Matplotlib

Database - SQLite

Machine Learning - Scikit-learn, XGBoost

Explainable AI - SHAP

NLP - NLTK, TF-IDF

Embeddings - Sentence Transformers

Vector Search - FAISS

Generative AI - Hugging Face Transformers, Qwen

Web Development - Flask, HTML, CSS, Bootstrap