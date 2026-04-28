import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE CONFIG & CUSTOM CSS ---
st.set_page_config(page_title="Retainlytics Command Center", page_icon="📈", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    /* Add a slight colored top border to mimic an enterprise dashboard */
    .block-container { border-top: 4px solid #2a9d8f; padding-top: 2rem; }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.title("📈 Retainlytics Command Center")
st.markdown("### Engineering Leadership in Customer Retention")

# --- LOAD DATA ---
@st.cache_data
def load_data():
    # Built-in fallback in case GitHub folder structures get flattened during upload
    try:
        return pd.read_csv('outputs/data/dashboard_scoring_data.csv')
    except FileNotFoundError:
        try:
            return pd.read_csv('dashboard_scoring_data.csv')
        except FileNotFoundError:
            st.error("⚠️ Data file not found. Ensure 'dashboard_scoring_data.csv' is uploaded to GitHub.")
            return pd.DataFrame()

df = load_data()

if not df.empty:
    # --- SIDEBAR: INTERACTIVE CONTROLS ---
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2010/2010990.png", width=60) # Generic dashboard icon
    st.sidebar.header("⚙️ Strategy Controls")
    st.sidebar.markdown("Adjust the decision gates to instantly model the financial impact of your retention strategy.")
    
    # Interactive sliders replacing the hardcoded 70/50 rule
    prob_threshold = st.sidebar.slider("Minimum Churn Probability Gate (%)", min_value=50, max_value=95, value=70, step=5) / 100.0
    rev_threshold = st.sidebar.slider("Minimum Revenue Gate ($)", min_value=10, max_value=150, value=50, step=5)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("**The Triage Logic:**")
    st.sidebar.markdown("🔴 **Whales:** Intervene (High Risk / High ROI)\n\n🟠 **Minnows:** Monitor (High Risk / Low ROI)\n\n🔘 **Safe:** Ignore (Low Risk)")

    # --- CORE LOGIC & FILTERING ---
    df['Segment'] = 'Safe (Ignore)'
    df.loc[(df['Churn_Probability'] >= prob_threshold) & (df['MonthlyRevenue'] < rev_threshold), 'Segment'] = 'Minnows (Monitor)'
    df.loc[(df['Churn_Probability'] >= prob_threshold) & (df['MonthlyRevenue'] >= rev_threshold), 'Segment'] = 'Whales (Intervene)'
    
    whales = df[df['Segment'] == 'Whales (Intervene)']
    
    # --- KPI METRIC CARDS ---
    st.markdown("### 💰 Financial Impact (Live Projection)")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Customers Scored", f"{len(df):,}")
    with col2:
        st.metric("High-Risk Churners", f"{len(df[df['Churn_Probability'] >= prob_threshold]):,}")
    with col3:
        # Using delta to show it as an actionable item
        st.metric("Targeted 'Whales'", f"{len(whales):,}", delta="Priority Action Required", delta_color="inverse")
    with col4:
        st.metric("Revenue at Risk", f"${whales['MonthlyRevenue'].sum():,.0f}", delta="Potential ROI", delta_color="normal")

    st.markdown("---")

    # --- TWO-COLUMN VISUAL LAYOUT ---
    col_chart, col_data = st.columns([1.2, 1])

    with col_chart:
        st.markdown("### 🎯 Interactive Triage Plot")
        st.markdown("Hover over customers to view their Technical Friction Index (TFI) and usage.")
        
        # Interactive Plotly Scatter Plot
        color_map = {'Whales (Intervene)': '#e63946', 'Minnows (Monitor)': '#f4a261', 'Safe (Ignore)': '#8d99ae'}
        
        # We sample the data slightly for rendering speed if it's massive, but Plotly handles it well
        plot_df = df.sample(n=min(3000, len(df)), random_state=42)
        
        fig = px.scatter(
            plot_df, x='Churn_Probability', y='MonthlyRevenue', color='Segment',
            color_discrete_map=color_map, opacity=0.7,
            hover_data=['TFI', 'DroppedCalls', 'OverageMinutes'],
            labels={'Churn_Probability': 'Churn Probability', 'MonthlyRevenue': 'Monthly Revenue ($)'}
        )
        
        # Add dynamic dashed lines that move when the user drags the sliders
        fig.add_hline(y=rev_threshold, line_dash="dash", line_color="#1d3557", annotation_text=f"${rev_threshold} Gate")
        fig.add_vline(x=prob_threshold, line_dash="dash", line_color="#1d3557", annotation_text=f"{int(prob_threshold*100)}% Gate")
        
        fig.update_layout(
            xaxis_tickformat='.0%',
            plot_bgcolor='rgba(240, 242, 246, 0.5)', # Soft grey background
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=0, r=0, t=30, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_data:
        st.markdown("### 🚨 Priority Action Roster")
        st.markdown("Ranked by highest probability and revenue.")
        
        display_cols = ['Churn_Probability', 'MonthlyRevenue', 'TFI', 'DroppedCalls']
        display_df = whales[display_cols].sort_values(by=['Churn_Probability', 'MonthlyRevenue'], ascending=[False, False])
        
        # Streamlit's new highly aesthetic column configuration
        st.dataframe(
            display_df.head(100),
            column_config={
                "Churn_Probability": st.column_config.ProgressColumn(
                    "Risk Level", help="XGBoost Churn Probability", format="%.2f", min_value=0, max_value=1
                ),
                "MonthlyRevenue": st.column_config.NumberColumn(
                    "Revenue", format="$%.2f"
                ),
                "TFI": st.column_config.NumberColumn(
                    "Friction (TFI)", help="Technical Friction Index", format="%.1f"
                ),
                "DroppedCalls": st.column_config.NumberColumn(
                    "Drops"
                )
            },
            hide_index=True,
            height=450,
            use_container_width=True
        )
