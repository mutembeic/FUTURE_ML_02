import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler

st.set_page_config(page_title="Churn Visualizations", layout="wide")

#Load and Cache Data 
@st.cache_data
def load_data():
    df = pd.read_csv('data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv')
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    df.dropna(inplace=True)
    df['Churn_numeric'] = df['Churn'].apply(lambda x: 1 if x == 'Yes' else 0)
    return df

df = load_data()

#Custom Styling 
st.markdown(
    """
    <style>
    [data-testid="stMetric"] {
        background-color: #262730;
        border: 1px solid #444;
        border-radius: 10px;
        padding: 15px;
    }
    [data-testid="stMetricLabel"] {
        color: #aaa;
    }
    </style>
    """, unsafe_allow_html=True
)

st.title('📊 Churn Insights Dashboard')
st.markdown("Analyze the key factors driving customer churn across different segments.")

# Section for Predicted Customer Analysis
if 'last_prediction_inputs' in st.session_state:
    st.subheader("Analysis for Last Predicted Customer")
    
    last_customer = st.session_state['last_prediction_inputs']
    last_prob = st.session_state['last_prediction_probability']
    
    # Data for Radar Chart
    # Define features for comparison
    radar_features = ['tenure', 'MonthlyCharges', 'TotalCharges']
    
    # Calculate averages for different groups
    avg_all = df[radar_features].mean().values
    avg_churn = df[df['Churn_numeric'] == 1][radar_features].mean().values
    avg_loyal = df[df['Churn_numeric'] == 0][radar_features].mean().values
    customer_values = [last_customer[f] for f in radar_features]
    
    # Scale all data for fair comparison on the radar chart
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform([avg_all, avg_churn, avg_loyal, customer_values])

    # Create Radar Chart
    fig_radar = go.Figure()

    fig_radar.add_trace(go.Scatterpolar(
        r=scaled_data[3], theta=radar_features, fill='toself', name='Predicted Customer',
        line_color='cyan'
    ))
    fig_radar.add_trace(go.Scatterpolar(
        r=scaled_data[0], theta=radar_features, name='Average Customer', line_color='grey'
    ))
    fig_radar.add_trace(go.Scatterpolar(
        r=scaled_data[1], theta=radar_features, name='Average Churned Customer', line_color='red'
    ))

    fig_radar.update_layout(
      polar=dict(radialaxis=dict(visible=False, range=[0, 1])),
      showlegend=True,
      template="plotly_dark",
      title="Predicted Customer Profile vs. Averages"
    )
    
    #Display Predicted Customer Info and Radar Chart 
    col1, col2 = st.columns([1, 1])
    with col1:
        st.metric(label="Predicted Churn Probability", value=f"{last_prob:.1%}")
        st.write("#### Customer Profile:")
        # Display the customer's attributes neatly
        profile_df = pd.DataFrame([last_customer]).T.rename(columns={0: 'Value'})
        st.dataframe(profile_df)
        
    with col2:
        st.plotly_chart(fig_radar, use_container_width=True)
    st.markdown("---")


#Main Dashboard Section 
st.subheader("Overall Customer Base Analysis")

#Interactive Filters for the main dashboard 
st.sidebar.header("Dashboard Filters")
contract_filter = st.sidebar.multiselect(
    'Filter by Contract Type:',
    options=df['Contract'].unique(),
    default=df['Contract'].unique()
)
internet_filter = st.sidebar.multiselect(
    'Filter by Internet Service:',
    options=df['InternetService'].unique(),
    default=df['InternetService'].unique()
)

df_selection = df.query(
    "Contract == @contract_filter & InternetService == @internet_filter"
)

#KPIs
total_customers = df_selection.shape[0]
churn_rate = (df_selection['Churn'] == 'Yes').sum() / total_customers * 100 if total_customers > 0 else 0
avg_monthly_charges = df_selection['MonthlyCharges'].mean()

kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    st.metric("Total Customers", f"{total_customers:,}")
with kpi2:
    st.metric("Overall Churn Rate", f"{churn_rate:.2f}%")
with kpi3:
    st.metric("Avg. Monthly Charge", f"${avg_monthly_charges:.2f}")

st.markdown("---")

#Visualization
col1, col2 = st.columns(2)
with col1:
    st.write("#### Churn by Contract Type")
    fig_contract = px.histogram(df_selection, x='Contract', color='Churn',
                                barmode='group', text_auto=True,
                                color_discrete_map={'Yes': '#d62728', 'No': '#00A6FF'},
                                template="plotly_dark")
    st.plotly_chart(fig_contract, use_container_width=True)

with col2:
    st.write("#### Internet Service Distribution")
    fig_internet = px.pie(df_selection, names='InternetService', hole=0.4,
                          template="plotly_dark")
    st.plotly_chart(fig_internet, use_container_width=True)

st.write("#### Monthly Charges vs. Tenure by Churn")
fig_scatter = px.scatter(df_selection, x='tenure', y='MonthlyCharges', color='Churn',
                         title="Higher monthly charges for shorter tenures correlate with churn",
                         color_discrete_map={'Yes': '#d62728', 'No': '#00A6FF'},
                         template="plotly_dark")
st.plotly_chart(fig_scatter, use_container_width=True)