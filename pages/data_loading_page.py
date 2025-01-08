import streamlit as st
from src.preprocessing.load_raw_data import DataLoaderFactory
from src.preprocessing.store_dataset import StoreDataSetFactory

# Hide the sidebar and other default Streamlit elements
st.markdown(
    """
    <style>
        /* Hide all sidebar elements */
        section[data-testid="stSidebar"] {display: none;}
        
        /* Hide other sidebar related elements */
        .css-1d391kg {display: none;}
        .css-18e3th9 {display: none;}
        div[data-testid="stSidebarNav"] {display: none;}
        
        /* Hide hamburger menu */
        button[kind="header"] {display: none;}
        
        /* Hide footer */
        footer {display: none;}
        
        /* Hide main menu */
        #MainMenu {display: none;}
    </style>
""",
    unsafe_allow_html=True,
)


def show_dataset_info():
    st.info(
        """
    ### About UNSW-NB15 Dataset
    The UNSW-NB15 dataset is a network security dataset that contains real modern normal and attack behaviors of network traffic.
    
    - Created by the IXIA PerfectStorm tool in the Cyber Range Lab of UNSW Canberra
    - Contains 49 features with labeled flows marking various types of attacks
    - Includes both training (175,341 records) and testing (82,332 records) sets
    - Features various attack categories including Fuzzers, Analysis, Backdoors, DoS, and more
    
    ### Future Updates
    This application will be enhanced to support:
    - Custom dataset uploads
    - Multiple data formats (CSV, Excel, JSON)
    - Direct database connections
    - Real-time data streaming
    """
    )


def data_loading_page():
    st.title("🔍 Data Loading and Exploration")

    # Center the hero subtext using custom CSS
    st.markdown(
        """
        <style>
            .hero-text {
                text-align: center;
            }
        </style>
        <div class="hero-text">
            <h2>Explore and Analyze Your Network Traffic Data</h2>
        </div>
    """,
        unsafe_allow_html=True,
    )

    # Show dataset information
    show_dataset_info()

    # Initialize session state for datasets if not exists
    if "datasets_loaded" not in st.session_state:
        st.session_state.datasets_loaded = False

    # Create a centered layout for the Load Dataset button
    col1, col2, col3 = st.columns([1, 2, 1])  # Adjust the proportions as needed
    with col2:
        if st.button("Load UNSW-NB15 Dataset"):
            with st.spinner("Loading datasets..."):
                data_loader = DataLoaderFactory()
                train_df, test_df, combined_df = data_loader.load_raw_data()

                if (
                    train_df is not None
                    and test_df is not None
                    and combined_df is not None
                ):
                    st.session_state.train_df = train_df
                    st.session_state.test_df = test_df
                    st.session_state.combined_df = combined_df
                    st.session_state.datasets_loaded = True
                    st.success("Datasets loaded successfully.")
                else:
                    st.error(
                        "Failed to load datasets. Please check the file paths and try again."
                    )

    # Display dataset information only if data is loaded
    if st.session_state.datasets_loaded:
        # Dataset selection
        dataset_option = st.radio(
            "Select Dataset to View:",
            ["Training Dataset", "Testing Dataset", "Combined Dataset"],
        )

        selected_df = None
        if dataset_option == "Training Dataset":
            selected_df = st.session_state.train_df
        elif dataset_option == "Testing Dataset":
            selected_df = st.session_state.test_df
        else:
            selected_df = st.session_state.combined_df

        st.write(f"Shape: {selected_df.shape} (rows, columns)")

        try:
            # Display summary statistics
            st.subheader("Dataset Summary")
            st.write(selected_df.describe())

            # Preview data with pagination
            st.subheader("Data Preview")
            page_size = st.slider("Rows per page", min_value=5, max_value=50, value=10)
            page_number = st.number_input("Page number", min_value=1, value=1)
            start_idx = (page_number - 1) * page_size
            end_idx = start_idx + page_size
            # Add a button to store the dataset
            if st.button("Store Dataset To Database"):
                with st.spinner("Storing dataset to database..."):
                    try:
                        store_dataset = StoreDataSetFactory()
                        store_dataset.store_raw_dataset()
                        st.success("Dataset stored successfully.")
                        st.write(selected_df.iloc[start_idx:end_idx])
                        col1, col2, col3 = st.columns([1, 2, 1])

                    except Exception as e:
                        st.error(f"Failed to store dataset: {str(e)}")

        except Exception as e:
            st.error(f"Error processing data: {str(e)}")

        with col2:
            if st.button(
                "Proceed to Preprocessing", key="proceed_button", type="primary"
            ):
                st.switch_page("pages/missing_values_handling.py")


# This line is crucial for Streamlit to run the page
data_loading_page()
