from fpdf import FPDF
from datetime import date
import os

class PDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 15)
        self.cell(0, 10, 'Customer Churn Prediction: Final Report', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def add_title(pdf, text):
    pdf.set_font('helvetica', 'B', 16)
    pdf.cell(0, 10, text, 0, 1, 'L')
    pdf.ln(5)

def add_body_text(pdf, text):
    pdf.set_font('helvetica', '', 12)
    pdf.multi_cell(0, 6, text)
    pdf.ln()

def create_report_pdf():
    """Generates the PDF report and returns its file path."""
    pdf = PDF()
    pdf.add_page()
    
    #Executive Summary
    add_title(pdf, '1. Executive Summary')
    summary_text = (
        "This report details the findings of a predictive modeling project aimed at identifying telecom customers "
        "at risk of churning. By analyzing historical customer data, we have developed a machine learning model "
        "that predicts churn with a high degree of accuracy (AUC: 0.83).\n\n"
        "The primary drivers of churn were identified as short customer tenure, month-to-month contracts, and "
        "the type of internet service. Based on these findings, we recommend targeted retention campaigns focusing on new "
        "customers and those on flexible contracts to improve long-term customer loyalty and reduce revenue loss."
    )
    add_body_text(pdf, summary_text)

    #Key Churn Drivers (Feature Importance)
    add_title(pdf, '2. Key Drivers of Customer Churn')
    add_body_text(pdf, "The following chart displays the top features that most strongly influence a customer's decision to churn. Contract type and tenure are the most significant factors.")
    
    feature_importance_path = 'reports/feature_importance.png'
    if os.path.exists(feature_importance_path):
        pdf.image(feature_importance_path, x=30, w=150)
        pdf.ln(5)
    else:
        add_body_text(pdf, f"[Image not found at '{feature_importance_path}']")

    #Model Performance
    add_title(pdf, '3. Predictive Model Performance')
    performance_text = (
        "We evaluated three models, with XGBoost selected for deployment due to its robust performance.\n\n"
        "Key Metrics (XGBoost Model):\n"
        "  - Accuracy: 79.1%\n"
        "  - Precision: 63.4% (Of all customers we predict will churn, 63.4% actually do).\n"
        "  - Recall: 49.5% (We successfully identify 49.5% of all customers who are about to churn).\n"
        "  - ROC AUC Score: 0.826 (Excellent ability to distinguish between churners and non-churners)."
    )
    add_body_text(pdf, performance_text)
    
    #Actionable Recommendations
    add_title(pdf, '4. Actionable Recommendations')
    recommendations = (
        "1.  **Target Month-to-Month Customers:** Launch a campaign offering a small discount for switching to a 1-year contract.\n\n"
        "2.  **Enhance New Customer Onboarding:** Implement a 'First 90 Days' program with proactive check-ins to address issues early.\n\n"
        "3.  **Investigate Fiber Optic Churn:** Survey former fiber optic customers to identify and fix service or pricing pain points.\n\n"
        "4.  **Bundle 'Sticky' Services:** Promote bundles that include high-retention services like Online Security and Tech Support."
    )
    add_body_text(pdf, recommendations)
    
    # Save the PDF to a reliable path
    report_folder = 'reports'
    if not os.path.exists(report_folder):
        os.makedirs(report_folder)
    
    report_filename = f'Churn_Prediction_Report_{date.today()}.pdf'
    report_path = os.path.join(report_folder, report_filename)
    pdf.output(report_path)
    print(f"Report successfully generated: {report_path}")
    return report_path

 
if __name__ == '__main__':
    create_report_pdf()