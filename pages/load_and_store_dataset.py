import streamlit as st
import pandas as pd
import time
from pathlib import Path
import os
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from src.preprocessing.store_raw_dataset import store_raw_dataset
from src.preprocessing.raw_dataset_loader import raw_dataset_loader


def load_and_store_dataset():
    # Initialize session states
    if 'show_heatmap' not in st.session_state:
        st.session_state['show_heatmap'] = False
    if 'loaded_data' not in st.session_state:
        st.session_state['loaded_data'] = {
            'train_df': None,
            'test_df': None,
            'combined_df': None
        }

    # Set page config
    st.set_page_config(layout="wide", page_title="Network Security Dataset Explorer")

    # Custom CSS for better styling
    st.markdown(
        """
        <style>
            /* Hide all sidebar elements */
        section[data-testid="stSidebar"] {display: none;}
        
        /* Hide other sidebar related elements */
        .css-1d391kg {display: none;}
        .css-18e3th9 {display: none;}
        div[data-testid="stSidebarNav"] {display: none;}
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
        
        /* New styles for centering */
        .correlation-section {
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            margin: 2rem auto;
            max-width: 1200px;
        }
        
        .correlation-controls {
            margin-bottom: 2rem;
            width: 100%;
            display: flex;
            justify-content: center;
            gap: 2rem;
        }
        
        /* Style for the plotly chart container */
        .stPlotlyChart {
            margin: 0 auto;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )

    # Title with custom styling
    st.markdown(
        """
        <h1 style='text-align: center; color: #2e4057;'>
            Network Security Dataset Explorer 🔒
        </h1>
    """,
        unsafe_allow_html=True,
    )

    # Introduction in a collapsible section
    with st.expander("ℹ️ About Network Security Datasets", expanded=False):
        st.markdown(
            """
            **Network Logs and Anomaly Detection**

            Network logs are crucial for analyzing traffic patterns and identifying unusual activity, such as unauthorized access or malware, within a network. These logs contain data such as IP addresses, timestamps, event types, and other network activity.
        """
        )

        # Create two columns for dataset info
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                """
                ### 📊 UNSW-NB15 Dataset Features
                - Over 2.5 million records
                - 49 features per record
                - Mix of categorical and numerical data
                - Real network traffic patterns
                - Labeled attack types
            """
            )

        with col2:
            st.markdown(
                """
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
            """
            )

    # Add new sample dataset section after the introduction
    st.markdown("---")
    st.header("📋 Sample Dataset")

    st.markdown(
        """
        ### Sample Dataset Available: UNSW-NB15
        
        We provide the UNSW-NB15 dataset as a sample to help you get started. This dataset is:
        
        - **Pre-loaded**: Ready to use with this application
        - **Well-documented**: Contains detailed feature descriptions
        - **Balanced**: Includes both normal and attack traffic
        - **Comprehensive**: Contains various types of network attacks
        
        ### How to Use the Sample Dataset:
        
        1. Click the "🔄 Load Dataset" button to load the UNSW-NB15 dataset
        2. Explore the data through the interactive visualizations
        3. When ready, click "💾 Store Dataset" to save it to the database
        
        > **Note**: The sample dataset is already preprocessed and ready for analysis. You can use this as a reference for working with your own network security datasets later.
    """
    )

    # Dataset schema in a separate expander
    with st.expander("📑 View Dataset Schema"):
        st.markdown(
            """
            ### Key Features in UNSW-NB15:
            
            #### Flow Features:
            - `srcip`, `sport`, `dstip`, `dsport`: Source/Destination IPs and ports
            - `proto`: Transaction protocol
            - `state`: Connection state
            
            #### Basic Features:
            - `dur`: Record total duration
            - `sbytes`, `dbytes`: Source/Destination bytes
            - `sttl`, `dttl`: Source/Destination time to live
            - `sloss`, `dloss`: Source/Destination packets retransmitted
            
            #### Content Features:
            - `service`: HTTP, FTP, IRC, etc.
            - `sload`, `dload`: Source/Destination bits per second
            
            #### Time Features:
            - `Stime`, `Ltime`: Record start/last time
            
            #### Generated Features:
            - `is_sm_ips_ports`: 1 if source/destination IP/port are equal
            - `ct_state_ttl`: No. of connections with same state and TTL
            
            #### Labels:
            - `attack_cat`: Attack category if applicable
            - `label`: Binary (0 for normal, 1 for attack)
        """
        )

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
            train_df, test_df, combined_df = raw_dataset_loader()
            
            # Store the loaded data in session state
            st.session_state['loaded_data']['train_df'] = train_df
            st.session_state['loaded_data']['test_df'] = test_df
            st.session_state['loaded_data']['combined_df'] = combined_df

    if store_button:
        with st.spinner("Storing datasets..."):
            store_raw_dataset()
            st.success("✅ Datasets stored successfully in the database!")
            st.balloons()

    # Move the data visualization outside the load_button handler
    if st.session_state['loaded_data']['train_df'] is not None:
        train_df = st.session_state['loaded_data']['train_df']
        test_df = st.session_state['loaded_data']['test_df']
        combined_df = st.session_state['loaded_data']['combined_df']

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
                attack_ratio = (train_df["label"].sum() / len(train_df)) * 100
                st.metric("Attack Ratio", f"{attack_ratio:.2f}%")

            # Show interactive dataframe
            st.dataframe(train_df.head(10), use_container_width=True)

            # Add basic visualizations
            if st.checkbox("Show Training Data Distribution"):
                fig = px.histogram(
                    train_df,
                    x="label",
                    color="label",
                    title="Distribution of Normal vs Attack Traffic",
                )
                st.plotly_chart(fig, use_container_width=True)

        with tabs[1]:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Records", f"{len(test_df):,}")
            with col2:
                st.metric("Features", f"{len(test_df.columns)}")
            with col3:
                attack_ratio = (test_df["label"].sum() / len(test_df)) * 100
                st.metric("Attack Ratio", f"{attack_ratio:.2f}%")

            st.dataframe(test_df.head(30), use_container_width=True)

        with tabs[2]:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Records", f"{len(combined_df):,}")
            with col2:
                st.metric("Features", f"{len(combined_df.columns)}")
            with col3:
                attack_ratio = (
                    combined_df["label"].sum() / len(combined_df)
                ) * 100
                st.metric("Attack Ratio", f"{attack_ratio:.2f}%")

            st.dataframe(combined_df.head(10), use_container_width=True)

        # Add dataset statistics in an expander
        with st.expander("📈 View Detailed Statistics"):
            st.write("### Training Dataset Statistics")
            st.write(train_df.describe())

        # Move the heatmap section outside the expander
        st.markdown('<div class="correlation-section">', unsafe_allow_html=True)
        st.markdown("### Correlation Analysis")

        # Create a container for the controls
        st.markdown('<div class="correlation-controls">', unsafe_allow_html=True)
        col1, col2 = st.columns([1, 1])
        with col1:
            show_heatmap = st.checkbox(
                "Show Correlation Heatmap",
                key="heatmap_checkbox",
                value=st.session_state["show_heatmap"]
            )
        with col2:
            show_table = st.checkbox(
                "Show correlation values as table",
                key="correlation_table"
            )
        st.markdown('</div>', unsafe_allow_html=True)

        if show_heatmap:
            st.session_state["show_heatmap"] = True
            
            try:
                numeric_cols = train_df.select_dtypes(
                    include=["float64", "int64"]
                ).columns
                correlation_matrix = train_df[numeric_cols].corr()

                # Create and display the heatmap
                fig, ax = plt.subplots(figsize=(12, 8))
                sns.heatmap(
                    correlation_matrix,
                    annot=True,
                    fmt=".2f",
                    cmap="coolwarm",
                    ax=ax
                )
                plt.title("Feature Correlation Heatmap", pad=20)
                st.pyplot(fig)

                # Show correlation table if selected
                if show_table:
                    st.dataframe(correlation_matrix, use_container_width=True)

            except Exception as e:
                st.error(f"Error creating heatmap: {str(e)}")
        else:
            st.session_state["show_heatmap"] = False

        st.markdown('</div>', unsafe_allow_html=True)

    # Add footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <p>Created with ❤️ for Network Security Analysis</p>
            <p>UNSW-NB15 Dataset Explorer v1.0</p>
        </div>
    """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    load_and_store_dataset()
