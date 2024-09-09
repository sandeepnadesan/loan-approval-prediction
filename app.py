import streamlit as st
import pandas as pd
import joblib

# Load the trained model
model = joblib.load('loan-predict.pkl')

# Define function to make predictions
def predict_loan_eligibility(data):
    # Predict using the loaded model
    prediction = model.predict(data)
    return "Eligible for Loan" if prediction[0] == 1 else "Not Eligible for Loan"

# Streamlit app layout
st.title("Loan Eligibility Predictor")

# Input fields for the user
gender = st.selectbox("Gender", ['Male', 'Female'])
married = st.selectbox("Married", ['No', 'Yes'])
dependents = st.selectbox("Dependents", ['0', '1', '2', '3+'])
education = st.selectbox("Education", ['Graduate', 'Not Graduate'])
self_employed = st.selectbox("Self Employed", ['No', 'Yes'])
applicant_income = st.number_input("Applicant Income", min_value=0)
coapplicant_income = st.number_input("Coapplicant Income", min_value=0)
loan_amount = st.number_input("Loan Amount", min_value=0)
loan_amount_term = st.number_input("Loan Amount Term (in months)", min_value=0)
credit_history = st.selectbox("Credit History", [1.0, 0.0])
property_area = st.selectbox("Property Area", ['Urban', 'Semiurban', 'Rural'])

# Encoding input features to match training data
def encode_inputs():
    inputs = {
        'Gender': 1 if gender == 'Male' else 0,
        'Married': 1 if married == 'Yes' else 0,
        'Dependents': {'0': 0, '1': 1, '2': 2, '3+': 3}[dependents],
        'Education': 1 if education == 'Graduate' else 0,
        'Self_Employed': 1 if self_employed == 'Yes' else 0,
        'ApplicantIncome': applicant_income,
        'CoapplicantIncome': coapplicant_income,
        'LoanAmount': loan_amount,
        'Loan_Amount_Term': loan_amount_term,
        'Credit_History': credit_history,
        'Property_Area': {'Urban': 2, 'Semiurban': 1, 'Rural': 0}[property_area]
    }
    return pd.DataFrame([inputs])

# Button to predict loan eligibility
if st.button("Predict Loan Eligibility"):
    # Prepare input data
    input_data = encode_inputs()
    # Make prediction
    result = predict_loan_eligibility(input_data)
    # Display the result
    st.success(f"The applicant is: {result}")
