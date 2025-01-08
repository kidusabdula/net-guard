import streamlit as st
import pandas as pd
from src.database.db_operations import fetch_table_data
from src.preprocessing.check_missing_values import CheckMissingValuesFactory


def display_data_summary(data, title):
    st.subheader(title)
    st.write(data.describe())
    st.write(f"Shape: {data.shape[0]} rows, {data.shape[1]} columns")
    st.write("---")  # Separator for better visual distinction


def check_missing_values_page():
    st.title("🔍 Check Missing Values in Datasets")

    # Hero Section
    st.markdown(
        """
        <style>
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
        .hero {
            background-color: #f4f7f6;
            padding: 2rem;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        }
        .hero h1 {
            color: #2d3436;
            font-size: 2.5rem;
            font-weight: bold;
        }
        .hero p {
            color: #636e72;
            font-size: 1.2rem;
        }
        .description {
            font-size: 1.2em;
            color: #555;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="hero"><h1>Welcome to the Missing Values Analyzer</h1>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="description">Ensure the integrity of your data with our state-of-the-art tool. This product identifies missing values in your datasets and utilizes KNN imputation to handle them efficiently, ensuring your data is ready for analysis and modeling.</p>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # Explanation of KNN imputation
    st.markdown(
        """
        ## How It Works
        Our tool checks for missing values across your datasets and leverages the power of K-Nearest Neighbors (KNN) imputation to handle them. The KNN method works by finding the 'K' nearest neighbors of a given missing value and using their values to estimate and fill in the missing one. This ensures that your data remains consistent and ready for any analysis or modeling task.
        
        ### Key Features:
        - **Efficient Missing Value Detection:** Quickly identifies missing data across various columns.
        - **KNN Imputation:** Uses KNN to replace missing values with accurate estimates based on similar records.
        - **Comprehensive Data Visualization:** Visualize the distribution of missing values with easy-to-understand charts.
        - **Seamless Integration:** Works with datasets stored in your database for easy access and management.

        With this tool, you can ensure that your data is complete, consistent, and ready for the next steps in your data processing pipeline.
        """
    )

    # Fetch train and test datasets with a spinner
    with st.spinner("Fetching train and test datasets from the database..."):
        train_data = fetch_table_data("unsw_nb15_raw_train_dataset")
        test_data = fetch_table_data("unsw_nb15_raw_test_dataset")
        st.success("Datasets fetched successfully.")  # Indicate success

    # Convert fetched data to DataFrame
    train_df = pd.DataFrame(train_data)
    test_df = pd.DataFrame(test_data)

    if train_df is not None and test_df is not None:
        # Display summaries
        display_data_summary(train_df, "Train Dataset Summary")
        display_data_summary(test_df, "Test Dataset Summary")

        # Check for missing values
        check_missing_values_factory = CheckMissingValuesFactory()
        test_missing_summary, train_missing_summary = (
            check_missing_values_factory.check_missing_values_module(
                test_data, train_data
            )
        )

        # Display missing values summary
        if not test_missing_summary.empty:
            st.write("### Missing Values in Test Data:")
            st.write(test_missing_summary)
            st.bar_chart(
                test_missing_summary
            )  # Visual representation of missing values

        if not train_missing_summary.empty:
            st.write("### Missing Values in Train Data:")
            st.write(train_missing_summary)
            st.bar_chart(
                train_missing_summary
            )  # Visual representation of missing values
    else:
        st.error("Failed to fetch datasets. Please check the database connection.")

    # Add a dynamic and aesthetic button to redirect to Imputation_page.py
    if st.button(
                "Proceed to Imputation Process", key="proceed_button", type="primary"
            ):
                st.switch_page("pages/imputation_page.py")


if __name__ == "__main__":
    check_missing_values_page()
