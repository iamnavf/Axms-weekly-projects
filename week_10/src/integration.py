import numpy as np 
import pandas as pd
import sqlite3
import joblib 

import faiss
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer,AutoModelForCausalLM


model = joblib.load(r"./models/model.pkl")
top_15_feature = joblib.load(r"./models/top_15_features.pkl")
encoder = joblib.load(r"./notebook/encoder.pkl")
scaler = joblib.load(r"./notebook/scaler.pkl")

kb_index = faiss.read_index(r"./models/kb_faiss.index")
kb_chunks_df = pd.read_pickle(r"./models/kb_chunks.pkl")
embedding_model = SentenceTransformer(r"./models/all-MiniLM-L6-v2")

model_name = "Qwen/Qwen2.5-1.5B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
llm = AutoModelForCausalLM.from_pretrained(model_name,torch_dtype="auto")

conn = sqlite3.connect(r"./notebook/customer_intelligence.db")

#sql user profile 

def get_customer_profile(customer_id):
    query = """SELECT * FROM customers WHERE customerID = ?"""
    customer = pd.read_sql_query(query,conn,params=(customer_id,))
    return customer

customer = get_customer_profile("5129-JLPIS")

customer['TotalCharges'] = pd.to_numeric(customer['TotalCharges'],errors='coerce')

customer['TotalCharges'] = customer['TotalCharges'].fillna(0)

def feature_engineering(customer):

    customer = customer.copy()

    customer['TotalCharges'] = pd.to_numeric(customer['TotalCharges'],errors='coerce').fillna(0)

    customer['tenure_group'] = pd.cut(customer['tenure'],bins=[-1, 12, 24, 48, 72],
                                      labels=['New', 'Short-term', 'Mid-term', 'Long-term'])

    customer['is_new_customer'] = (customer['tenure'] <= 12).astype(int)

    customer['is_long_term_customer'] = (customer['tenure'] > 48).astype(int)

    service_cols = ['PhoneService', 'MultipleLines', 'OnlineSecurity','OnlineBackup', 'DeviceProtection',
                     'TechSupport',
        'StreamingTV', 'StreamingMovies']

    customer['num_subscribed_services'] = (
        customer[service_cols] == 'Yes'
    ).sum(axis=1)

    optional_service_cols = [
        'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
        'TechSupport', 'StreamingTV', 'StreamingMovies'
    ]

    customer['num_optional_services'] = (
        customer[optional_service_cols] == 'Yes'
    ).sum(axis=1)

    customer['has_internet_service'] = (
        customer['InternetService'] != 'No'
    ).astype(int)

    customer['monthly_charge_group'] = pd.cut(
        customer['MonthlyCharges'],
        bins=[0, 35, 70, float('inf')],
        labels=['Low', 'Medium', 'High']
    )

    customer['total_charge_group'] = pd.cut(
        customer['TotalCharges'],
        bins=[-1, 1000, 3000, 6000, float('inf')],
        labels=['Low', 'Medium', 'High', 'Very High']
    )

    customer['charge_to_tenure_ratio'] = (
        customer['TotalCharges'] /
        customer['tenure'].replace(0, np.nan)
    ).fillna(0)

    customer['contract_risk'] = (
        customer['Contract'] == 'Month-to-month'
    ).astype(int)

    customer['payment_method_risk'] = (
        customer['PaymentMethod'] == 'Electronic check'
    ).astype(int)

    customer['service_combination_risk'] = (
        (customer['OnlineSecurity'] == 'No') &
        (customer['TechSupport'] == 'No')
    ).astype(int)

    customer['high_value_high_risk'] = (
        (customer['TotalCharges'] >= 6000) &
        (customer['contract_risk'] == 1)
    ).astype(int)

    return customer