# Retainlytics: Customer Retention Pipeline

**🚀 LIVE DASHBOARD:** [Click here to view the live Streamlit Command Center](https://your-custom-url.streamlit.app/)

## Executive Summary
Retainlytics is an end-to-end data science and engineering leadership capstone project (RCEL-506). It predicts telecom customer churn using an XGBoost model accelerated by T4 GPUs. The project operationalizes these predictions using a custom **Technical Friction Index (TFI)** and a **70/50 Cost-Benefit Decision Gate**.

## Repository Structure
- `FinalCapstoneProject_Retainlytics.ipynb`: The core Google Colab pipeline (Data Ingestion, TFI Engineering, GPU Modeling, Diagnostics).
- `app.py`: The Streamlit Command Center dashboard.
- `outputs/figures/`: Presentation-ready data visualizations (ROC-AUC, Triage Plots, Waterfall Charts).
- `outputs/data/`: Leakage-free holdout datasets scored by the model for the dashboard.
- `requirements.txt`: Python dependencies for replication.

## Running the Code
The data pipeline was executed in Google Colab using NVIDIA T4 GPU acceleration. To replicate the model training:
1. Open `FinalCapstoneProject_Retainlytics.ipynb` in Google Colab.
2. Ensure the hardware accelerator is set to T4 GPU.
3. Run all cells sequentially to generate the metrics, graphs, and the updated `dashboard_scoring_data.csv`.

## Local App Deployment
To run the Streamlit app locally instead of via the cloud link above:
1. Ensure Python is installed.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `streamlit run app.py`
