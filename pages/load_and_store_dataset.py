import streamlit as st
import pandas as pd
import time
from pathlib import Path
import os
import plotly.express as px
from src.preprocessing.store_raw_dataset import store_raw_dataset
from src.preprocessing.raw_dataset_loader import raw_dataset_loader

def load_and_store_dataset():
    # Set page config
    st.set_page_config(layout="wide", page_title="Network Security Dataset Explorer")
    
    # Custom CSS for better styling
    st.markdown("""
        <style>
        .main {
            padding: 2rem;
        }
        .stButton>button {
            width: 100%;
            margin-top: 1rem;
        }
        .stats-box {
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
            margin: 10px 0;
        }
        </style>
    """, unsafe_allow_html=True)

    # Title with custom styling
    st.markdown("""
        <h1 style='text-align: center; color: #2e4057;'>
            Network Security Dataset Explorer 🔒
        </h1>
    """, unsafe_allow_html=True)

    # Introduction in a collapsible section
    with st.expander("ℹ️ About Network Security Datasets", expanded=True):
        st.markdown("""
            **Network Logs and Anomaly Detection**

            Network logs are crucial for analyzing traffic patterns and identifying unusual activity, such as unauthorized access or malware, within a network. These logs contain data such as IP addresses, timestamps, event types, and other network activity.
        """)
        
        # Create two columns for dataset info
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
                ### 📊 UNSW-NB15 Dataset Features
                - Over 2.5 million records
                - 49 features per record
                - Mix of categorical and numerical data
                - Real network traffic patterns
                - Labeled attack types
            """)
            
        with col2:
            st.markdown("""
                ### 🚫 Attack Categories
                1. DoS (Denial of Service)
                2. Exploits
                3. Fuzzers
                4. Backdoors
                5. Shellcode
                6. Worms
                7. Generic attacks
                8. Reconnaissance
                9. Analysis
            """)

    # Dataset loading section
    st.markdown("---")
    st.header("📥 Dataset Operations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        load_button = st.button("🔄 Load Dataset", key="load")
    with col2:
        store_button = st.button("💾 Store Dataset", key="store")

    if load_button:
        with st.spinner("Loading dataset... please wait."):
            time.sleep(1)
            train_df, test_df, combined_df = raw_dataset_loader()
            
            if train_df is not None and test_df is not None and combined_df is not None:
                st.success("✅ Datasets loaded successfully!")
                
                # Dataset Overview Section
                st.markdown("## 📊 Dataset Overview")
                
                tabs = st.tabs(["Training Data", "Testing Data", "Combined Data"])
                
                with tabs[0]:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Records", f"{len(train_df):,}")
                    with col2:
                        st.metric("Features", f"{len(train_df.columns)}")
                    with col3:
                        attack_ratio = (train_df['label'].sum() / len(train_df)) * 100
                        st.metric("Attack Ratio", f"{attack_ratio:.2f}%")
                    
                    # Show interactive dataframe
                    st.dataframe(train_df.head(10), use_container_width=True)
                    
                    # Add basic visualizations
                    if st.checkbox("Show Training Data Distribution"):
                        fig = px.histogram(train_df, x='label', color='label',
                                         title='Distribution of Normal vs Attack Traffic')
                        st.plotly_chart(fig, use_container_width=True)

                with tabs[1]:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Records", f"{len(test_df):,}")
                    with col2:
                        st.metric("Features", f"{len(test_df.columns)}")
                    with col3:
                        attack_ratio = (test_df['label'].sum() / len(test_df)) * 100
                        st.metric("Attack Ratio", f"{attack_ratio:.2f}%")
                    
                    st.dataframe(test_df.head(10), use_container_width=True)

                with tabs[2]:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Records", f"{len(combined_df):,}")
                    with col2:
                        st.metric("Features", f"{len(combined_df.columns)}")
                    with col3:
                        attack_ratio = (combined_df['label'].sum() / len(combined_df)) * 100
                        st.metric("Attack Ratio", f"{attack_ratio:.2f}%")
                    
                    st.dataframe(combined_df.head(10), use_container_width=True)
                
                # Add dataset statistics in an expander
                with st.expander("📈 View Detailed Statistics"):
                    st.write("### Training Dataset Statistics")
                    st.write(train_df.describe())
                    
                    # Add correlation heatmap for numerical columns
                    if st.checkbox("Show Correlation Heatmap"):
                        numeric_cols = train_df.select_dtypes(include=['float64', 'int64']).columns
                        fig = px.imshow(train_df[numeric_cols].corr(),
                                      title="Feature Correlation Heatmap")
                        st.plotly_chart(fig, use_container_width=True)
            else:
                st.error("❌ Failed to load the datasets. Please check the file paths.")

    if store_button:
        with st.spinner("Storing datasets..."):
            store_raw_dataset()
            st.success("✅ Datasets stored successfully in the database!")
            st.balloons()

    # Add footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #666;'>
            <p>Created with ❤️ for Network Security Analysis</p>
            <p>UNSW-NB15 Dataset Explorer v1.0</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    load_and_store_dataset()
