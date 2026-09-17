import numpy as np 
import pandas as pd
import sqlite3
import joblib 
import shap

import faiss
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer,AutoModelForCausalLM


model = joblib.load(r"./models/model.pkl")
top_15_feature = joblib.load(r"./models/top_15_features.pkl")
top_15_indices = joblib.load(r"./models/top_15_indices.pkl")
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

#feature engineering
def feature_engineering(customer):

    customer = customer.copy()

    customer['TotalCharges'] = pd.to_numeric(customer['TotalCharges'],errors='coerce').fillna(0)

    customer['tenure_group'] = pd.cut(customer['tenure'],bins=[-1, 12, 24, 48, 72],
                                      labels=['New', 'Short-term', 'Mid-term', 'Long-term'])

    customer['is_new_customer'] = (customer['tenure'] <= 12).astype(int)

    customer['is_long_term_customer'] = (customer['tenure'] > 48).astype(int)

    service_cols = ['PhoneService', 'MultipleLines', 'OnlineSecurity','OnlineBackup', 'DeviceProtection',
                     'TechSupport','StreamingTV', 'StreamingMovies']

    customer['num_subscribed_services'] = (customer[service_cols] == 'Yes').sum(axis=1)

    optional_service_cols = ['OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
                             'TechSupport', 'StreamingTV', 'StreamingMovies']

    customer['num_optional_services'] = (customer[optional_service_cols] == 'Yes').sum(axis=1)

    customer['has_internet_service'] = (customer['InternetService'] != 'No').astype(int)

    customer['monthly_charge_group'] = pd.cut(customer['MonthlyCharges'],bins=[0, 35, 70, float('inf')],
                                    labels=['Low', 'Medium', 'High'])

    customer['total_charge_group'] = pd.cut(customer['TotalCharges'],bins=[-1, 1000, 3000, 6000, float('inf')],
                                    labels=['Low', 'Medium', 'High', 'Very High'])

    customer['charge_to_tenure_ratio'] = (customer['TotalCharges'] / customer['tenure'].replace(0, np.nan)
                                          ).fillna(0)

    customer['contract_risk'] = (customer['Contract'] == 'Month-to-month').astype(int)

    customer['payment_method_risk'] = (customer['PaymentMethod'] == 'Electronic check').astype(int)

    customer['service_combination_risk'] = ((customer['OnlineSecurity'] == 'No') &
                                            (customer['TechSupport'] == 'No')).astype(int)

    customer['high_value_high_risk'] = ((customer['TotalCharges'] >= 6000) &(customer['contract_risk'] == 1)
                                        ).astype(int)

    return customer

#data scaling and encode and top 15 cols
def preprocess_customer(customer):
    customer = customer.drop(['customerID','Churn'], axis=1)
    numeric_cols = customer.select_dtypes(include=np.number).columns.tolist()
    categorical_cols = customer.select_dtypes(exclude=np.number).columns.tolist()
    
    customer_cat = encoder.transform(customer[categorical_cols])
    customer_num = scaler.transform(customer[numeric_cols])

    customer_processed = np.hstack([customer_num,customer_cat])
    customer_top15 = customer_processed[:, top_15_indices]

    return customer_top15

customer = get_customer_profile("9305-CDSKC")
#totalchanges datatype change
customer['TotalCharges'] = pd.to_numeric(customer['TotalCharges'],errors='coerce')
customer['TotalCharges'] = customer['TotalCharges'].fillna(0)

customer = feature_engineering(customer)
customer_top15 = preprocess_customer(customer)

churn_probability = model.predict_proba(customer_top15)[0][1]

churn_prediction = model.predict(customer_top15)[0]

explainer = shap.TreeExplainer(model)

customer_shap = explainer(customer_top15)

shap_values_customer = customer_shap.values[0]


shap_text = "\n".join(f"{feature}: {'increases' if value > 0 else 'decreases'} churn risk"
    for feature, value in zip(top_15_feature, shap_values_customer))
    
def retrieve_knowledge(query, top_k=5):
    query_vector = embedding_model.encode([query]).astype("float32")
    distances, indices = kb_index.search(query_vector,top_k)
    results = kb_chunks_df.iloc[indices[0]]
    return results

def build_rag_context(rag_results):
    context = ""
    for _, row in rag_results.iterrows():
        context += f"""Category: {row['category']}
            Title: {row['title']}
            Information: {row['text']} """
    return context

query = "How can I cancel my subscription?"
rag_results = retrieve_knowledge(query)
context = build_rag_context(rag_results)

def generate_response(customer_id, churn_probability, shap_text,context, question):
    prompt = prompt = f"""Use ONLY the Model explanation to answer the question.Do not interpret, 
    explain, rename, combine, or infer any feature.Copy feature names exactly as written.
    Only mention features marked "increases churn risk".Do not use the Support information for this question.
    Do not give advice.
        Customer ID: {customer_id}
        Churn probability: {churn_probability:.2%}
        Model explanation:{shap_text}
        Support:{context}
        Question:{question}
        Answer:"""

    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = llm.generate(**inputs,max_new_tokens=100)
    return tokenizer.decode(outputs[0],skip_special_tokens=True)

question = "Why am I at such high risk of being cancelled?"

response = generate_response("5129-JLPIS",churn_probability,shap_text,context,question)

print(response)