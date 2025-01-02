import streamlit as st

def home_page():
    st.title("Net Guard Dashboard")
    st.subheader("A Comprehensive Solution for Anomaly Detection in Network Logs")
    st.write("""
    Welcome to the **Net Guard Dashboard**! This platform guides you through the entire process of network anomaly detection, 
    from raw dataset loading to advanced clustering and anomaly detection using autoencoders. Explore each step in detail by 
    navigating through the options below.
    """)
    st.markdown("### Features of the Dashboard")
    st.write("""
    - **Load Raw Datasets**: Import and inspect your network log data.
    - **Handle Missing Values**: Check and impute missing entries for a clean dataset.
    - **Encode Categorical Data**: Transform categorical features for compatibility with models.
    - **Apply KNN Imputation**: Ensure data integrity using advanced imputation techniques.
    - **Cluster Analysis**: Perform clustering to understand network patterns.
    - **Anomaly Detection**: Detect irregularities using autoencoder models.
    """)
