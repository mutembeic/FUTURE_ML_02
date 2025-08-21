import streamlit as st

st.set_page_config(page_title="About", layout="centered")

st.title("📄 About This Project")

st.markdown("""
### The Business Problem
Customer churn is a major challenge for telecommunication companies. This project aims to build a machine learning system that can accurately predict which customers are likely to churn. By identifying these customers in advance, the business can take proactive steps to retain them, thereby reducing revenue loss and improving customer loyalty.

### The Dataset
The model was trained on the **Telco Customer Churn** dataset from Kaggle. It contains 7,043 customer records with 21 attributes, including:
- **Demographic Info:** Gender, Senior Citizen, Partner, Dependents.
- **Account Info:** Tenure, Contract, Payment Method, Paperless Billing, Monthly Charges, Total Charges.
- **Services Subscribed:** Phone Service, Multiple Lines, Internet Service, Online Security, etc.

### Methodology
1.  **Exploratory Data Analysis (EDA):** We analyzed the data to uncover patterns. Key findings showed that customers on **month-to-month contracts**, with **low tenure**, and using **fiber optic internet** were most likely to churn.
2.  **Data Preprocessing:** Categorical features were one-hot encoded and numerical features were standardized to prepare the data for modeling.
3.  **Model Training & Selection:** We trained and compared three models: Logistic Regression, Random Forest, and XGBoost. The **XGBoost Classifier** was selected for its superior performance, particularly its ability to distinguish between churners and non-churners (ROC-AUC score of 0.826).
4.  **Deployment:** The final model pipeline was saved and deployed as this interactive Streamlit web application.

### Tools and Libraries Used
- **Python:** The core programming language.
- **Pandas & NumPy:** For data manipulation.
- **Scikit-learn:** For data preprocessing and modeling.
- **XGBoost:** For the final classification model.
- **Plotly & Matplotlib/Seaborn:** For data visualization.
- **Streamlit:** For building this interactive web app.
- **FPDF2:** For generating the summary report.
""")