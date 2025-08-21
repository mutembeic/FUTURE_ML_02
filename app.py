import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
import os
from generate_report import create_report_pdf  

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#Page Configuration
st.set_page_config(
    page_title="Churn Prediction System",
    page_icon="🚀",
    layout="wide"
)

#Custom CSS for Styling 
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Check if the CSS file exists before trying to load it
if os.path.exists('.streamlit/style.css'):
    load_css('.streamlit/style.css')
else:
    st.warning("Custom CSS file not found. App will use default styling.")

#  Load Model
# Use st.cache_resource for one-time loading of heavy objects like models
@st.cache_resource
def load_model():
    try:
        pipeline = joblib.load('models/churn_predictor.joblib')
        return pipeline
    except FileNotFoundError:
        return None

pipeline = load_model()
if pipeline is None:
    st.error("Model file not found. Please ensure 'models/churn_predictor.joblib' exists.")
    st.stop()


#App Layout 
st.title('🚀 Customer Churn Prediction System')
st.markdown("""
Welcome to the interactive Churn Prediction dashboard. Use the sidebar to enter a customer's details and our AI model will predict their churn probability. 
Navigate to the **Dashboard & Visualizations** page for an overview of churn drivers.
""")

#Sidebar for User Input 
with st.sidebar:
    st.header('Customer Information')

    # Create a dictionary to hold user inputs
    user_inputs = {}

    # Define input fields based on the model's features
    user_inputs['gender'] = st.selectbox('Gender', ('Male', 'Female'))
    user_inputs['Partner'] = st.selectbox('Has a Partner?', ('Yes', 'No'))
    user_inputs['Dependents'] = st.selectbox('Has Dependents?', ('Yes', 'No'))
    user_inputs['PhoneService'] = st.selectbox('Has Phone Service?', ('Yes', 'No'))
    user_inputs['MultipleLines'] = st.selectbox('Has Multiple Lines?', ('No', 'Yes', 'No phone service'))
    user_inputs['InternetService'] = st.selectbox('Internet Service Type', ('DSL', 'Fiber optic', 'No'))
    user_inputs['OnlineSecurity'] = st.selectbox('Has Online Security?', ('No', 'Yes', 'No internet service'))
    user_inputs['OnlineBackup'] = st.selectbox('Has Online Backup?', ('No', 'Yes', 'No internet service'))
    user_inputs['DeviceProtection'] = st.selectbox('Has Device Protection?', ('No', 'Yes', 'No internet service'))
    user_inputs['TechSupport'] = st.selectbox('Has Tech Support?', ('No', 'Yes', 'No internet service'))
    user_inputs['StreamingTV'] = st.selectbox('Has Streaming TV?', ('No', 'Yes', 'No internet service'))
    user_inputs['StreamingMovies'] = st.selectbox('Has Streaming Movies?', ('No', 'Yes', 'No internet service'))
    user_inputs['Contract'] = st.selectbox('Contract Type', ('Month-to-month', 'One year', 'Two year'))
    user_inputs['PaperlessBilling'] = st.selectbox('Uses Paperless Billing?', ('Yes', 'No'))
    user_inputs['PaymentMethod'] = st.selectbox('Payment Method', ('Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)'))
    
    # Numerical features
    user_inputs['tenure'] = st.slider('Tenure (months)', 0, 72, 12)
    user_inputs['MonthlyCharges'] = st.number_input('Monthly Charges ($)', min_value=0.0, max_value=150.0, value=70.0, step=1.0)
    user_inputs['TotalCharges'] = st.number_input('Total Charges ($)', min_value=0.0, max_value=10000.0, value=1000.0, step=50.0)
    
    is_senior = st.checkbox('Is Senior Citizen?')
    user_inputs['SeniorCitizen'] = 1 if is_senior else 0


#Main Area for Prediction Output and Report 
col1, col2 = st.columns([0.6, 0.4], gap="large")

with col1:
    st.header("Churn Prediction")
    if st.button('Predict Churn', use_container_width=True):
        input_df = pd.DataFrame([user_inputs])
        prediction_proba = pipeline.predict_proba(input_df)[0]
        churn_probability = prediction_proba[1]

        #SAVE TO SESSION STATE
        st.session_state['last_prediction_inputs'] = user_inputs
        st.session_state['last_prediction_probability'] = churn_probability

        # Display the result with a dynamic message
        if churn_probability > 0.7:
            st.error(f'🔴 High Risk of Churn (Probability: {churn_probability:.1%})')
            st.warning('Recommendation: Immediate intervention required. Offer a premium discount or a dedicated support agent.')
        elif churn_probability > 0.4:
            st.warning(f'🟡 Medium Risk of Churn (Probability: {churn_probability:.1%})')
            st.info('Recommendation: Target with a retention campaign, like a service upgrade or a small loyalty discount.')
        else:
            st.success(f'🟢 Low Risk of Churn (Probability: {churn_probability:.1%})')
            st.info('Recommendation: No immediate action needed. Continue with standard customer engagement.')
            
        # Probability Gauge
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = churn_probability * 100,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Churn Probability (%)", 'font': {'size': 24}},
            gauge = {
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "#262730"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 40], 'color': 'rgba(44, 160, 44, 0.7)'}, # Green
                    {'range': [40, 70], 'color': 'rgba(255, 127, 14, 0.7)'}, # Orange
                    {'range': [70, 100], 'color': 'rgba(214, 39, 40, 0.7)'}  # Red
                ]
            }))
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.header("Download Full Report")
    st.markdown("Generate a comprehensive PDF report with project methodology, key findings, and business recommendations.")
    
    # When the user clicks, generate the PDF and provide it for download.
    # The file is generated on-the-fly.
    report_path = create_report_pdf()
    with open(report_path, "rb") as pdf_file:
        PDFbyte = pdf_file.read()
    
    st.download_button(
        label="Download Report PDF",
        data=PDFbyte,
        file_name=os.path.basename(report_path),
        mime='application/pdf',
        use_container_width=True
    )