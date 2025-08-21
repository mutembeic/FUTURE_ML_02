from fpdf import FPDF
from datetime import date
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define a PDF class with Header and Footer
class PDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 15)
        self.cell(0, 10, 'Customer Churn Prediction: Final Report', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

# Helper functions to add content
def add_title(pdf, text):
    pdf.set_font('helvetica', 'B', 16)
    pdf.set_text_color(22, 77, 129)
    pdf.cell(0, 10, text, 0, 1, 'L')
    pdf.set_text_color(0, 0, 0)
    pdf.ln(4)

def add_body_text(pdf, text):
    pdf.set_font('helvetica', '', 11)
    cleaned_text = text.replace('**', '').encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 6, cleaned_text)
    pdf.ln(3)

def add_tiered_insight(pdf, tier_title, points):
    pdf.set_font('helvetica', 'B', 11)
    pdf.multi_cell(0, 6, tier_title.replace('**', '').encode('latin-1', 'replace').decode('latin-1'))
    pdf.ln(1)
    
    for point_title, point_text in points.items():
        cleaned_title = point_title.replace('**', '').encode('latin-1', 'replace').decode('latin-1')
        cleaned_text = point_text.replace('**', '').encode('latin-1', 'replace').decode('latin-1')
        
        pdf.set_font('helvetica', '', 11)
        pdf.write(6, '  - ') 
        pdf.set_font('', 'B')
        pdf.write(6, cleaned_title)
        pdf.set_font('', '')
        pdf.write(6, cleaned_text)
        pdf.ln(6)  
    pdf.ln(3)

def add_recommendation(pdf, title, insight, action):
    pdf.set_font('helvetica', 'B', 12)
    pdf.multi_cell(0, 6, title.encode('latin-1', 'replace').decode('latin-1'))
    
    cleaned_insight = insight.replace('**', '').encode('latin-1', 'replace').decode('latin-1')
    cleaned_action = action.replace('**', '').encode('latin-1', 'replace').decode('latin-1')

    pdf.set_font('helvetica', 'B', 11)
    pdf.write(6, 'Insight: ')
    pdf.set_font('', '')
    pdf.write(6, cleaned_insight)
    pdf.ln(6)  

    pdf.set_font('helvetica', 'B', 11)
    pdf.write(6, 'Action: ')
    pdf.set_font('', '')
    pdf.multi_cell(0, 6, cleaned_action)   
    pdf.ln(5)

# Main function to create the report
def create_report_pdf():
    """Generates the PDF report and returns its file path."""
    pdf = PDF()
    pdf.add_page()
    
    # 1. Executive Summary
    add_title(pdf, '1. Executive Summary')
    summary_text = (
        "This report outlines the development of an AI-powered churn prediction model designed to proactively identify customers at risk of leaving. "
        "The final model, an XGBoost Classifier, can distinguish between churning and loyal customers with a high degree of confidence (0.83 AUC).\n\n"
        "Our analysis reveals that churn is not random; it is driven by a clear set of factors. The highest risk profile is a new customer on a flexible month-to-month contract, who is paying a relatively high monthly fee and has not subscribed to value-added 'sticky' services like Tech Support or Online Security. "
        "This report provides concrete, data-driven recommendations to address these specific risk factors and improve customer retention."
    )
    add_body_text(pdf, summary_text)

    # 2. Key Drivers of Customer Churn
    add_title(pdf, '2. Key Drivers of Customer Churn')
    add_body_text(pdf, "The predictive model identified the most influential factors in a customer's decision to churn. These drivers can be grouped into three strategic themes:")
    
    feature_importance_path = os.path.join(BASE_DIR, 'reports', 'feature_importance.png')
    if os.path.exists(feature_importance_path):
        pdf.image(feature_importance_path, x=(210-160)/2, w=160)
        pdf.ln(5)
    else:
        add_body_text(pdf, f"[Image not found at '{feature_importance_path}']")
    
    add_tiered_insight(pdf, "Tier 1: Financial & Loyalty Core", {
        "TotalCharges & tenure:": " The customer's financial lifetime value and length of service are the strongest indicators of loyalty. New customers are the most vulnerable.",
        "MonthlyCharges:": " High monthly fees, especially for new customers, significantly increase churn risk."
    })
    
    add_tiered_insight(pdf, "Tier 2: Contractual & Service Red Flags", {
        "Contract_Month-to-month:": " The lack of a long-term commitment is the single largest risk factor, providing an easy exit path for dissatisfied customers.",
        "InternetService_Fiber optic:": " This premium service is paradoxically linked to higher churn, suggesting potential issues with its price, performance, or customer support."
    })

    add_tiered_insight(pdf, "Tier 3: Ecosystem 'Stickiness' Factors", {
        "Absence of Add-ons:": " Customers without services like Online Security, Tech Support, and Online Backup are less integrated into our platform and have fewer reasons to stay."
    })

    pdf.add_page()

    # 3. Predictive Model Performance
    add_title(pdf, '3. Predictive Model Performance')
    add_body_text(pdf, "An XGBoost model was selected for its superior predictive power. It provides a strong balance between identifying potential churners and avoiding false alarms.\n\nKey Metrics:")
    
    add_tiered_insight(pdf, "", {
        "Accuracy:": " 79.1% (Overall correct predictions).",
        "Precision:": " 63.4% (When we predict a customer will churn, we are correct 63.4% of the time).",
        "Recall:": " 49.5% (The model successfully identifies 49.5% of all customers who are actually going to churn).",
        "ROC AUC Score:": " 0.826 (Excellent ability to distinguish between churners and non-churners)."
    })
    
    pdf.ln(5)

    # 4. Actionable Recommendations
    add_title(pdf, '4. Actionable Business Recommendations')
    
    add_recommendation(
        pdf, "1. Launch a 'Loyalty Contract' Initiative.",
        "Month-to-month contracts are the biggest churn driver.",
        "Proactively offer a 10% discount or a free premium service (like Online Backup) to high-risk, month-to-month customers if they convert to a 1-year contract. This directly addresses the main risk factor and increases customer 'stickiness'."
    )
    
    add_recommendation(
        pdf, "2. Implement a 'First 90 Days' Onboarding Program.",
        "Low tenure is the second-largest predictor of churn.",
        "Create an automated email and SMS campaign for new customers that includes a welcome call, service usage tips, and a satisfaction survey at the 30-day mark. The goal is to address problems early and demonstrate value before they consider leaving."
    )

    add_recommendation(
        pdf, "3. Create a 'Peace of Mind' Service Bundle.",
        "Lack of add-on services like Tech Support and Online Security correlates with higher churn.",
        "Market a discounted bundle of these 'sticky' services to customers who only have a basic internet or phone plan. This increases their integration with our ecosystem and raises the switching cost."
    )
    
    add_recommendation(
        pdf, "4. Investigate the Fiber Optic Experience.",
        "Fiber optic customers, despite being on a premium plan, are a high-churn segment.",
        "Deploy a targeted survey to current and former fiber customers to diagnose the root cause. The issue could be related to pricing, reliability, or competitor offers. The findings should inform potential price adjustments or service improvements."
    )
    
    # Save the PDF 
    report_folder = os.path.join(BASE_DIR, 'reports')
    if not os.path.exists(report_folder):
        os.makedirs(report_folder)
    
    report_filename = f'Churn_Prediction_Report_{date.today()}.pdf'
    report_path = os.path.join(report_folder, report_filename)
    pdf.output(report_path)
    print(f"Report successfully generated: {report_path}")
    return report_path

 
if __name__ == '__main__':
    create_report_pdf()