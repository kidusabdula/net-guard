import streamlit as st
import pandas as pd
from src.preprocessing.dataset_encoder import DatasetEncoderFactory
from src.preprocessing.knn_imputation import KNNImputerFactory
from src.preprocessing.dataset_decoder import DatasetDecoderFactory
from src.database.db_operations import fetch_table_data
from src.database.db_operations import bulk_store_dataset
from time import sleep
import time


def initialize_session_state():
    if "encoded_df_var" not in st.session_state:
        st.session_state.encoded_df_var = None
    if "imputed_df_var" not in st.session_state:
        st.session_state.imputed_df_var = None
    if "decoded_df_var" not in st.session_state:
        st.session_state.decoded_df_var = None


def imputation_page():
    initialize_session_state()

    st.title("📊 KNN Imputation of Missing Values")

    # UI Styling
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
        
        .hero {
            background-color: #2d3436;
            padding: 3rem;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            margin-bottom: 2rem;
        }
        .hero h1 {
            color: #ffffff;
            font-size: 3rem;
        }
        .description {
            font-size: 1.2rem;
            color: #b2bec3;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # Fetch Data
    st.markdown(
        '<div class="hero"><h1>Dynamic KNN Imputation Tool</h1></div>',
        unsafe_allow_html=True,
    )
    with st.spinner("Fetching train and test datasets from the database..."):
        train_data = fetch_table_data("unsw_nb15_raw_train_dataset")
    st.success("Datasets fetched successfully.")

    # Encoding
    st.subheader("Step 1: Encoding the Dataset")
    if st.button("Start Encoding"):
        with st.spinner("Encoding the dataset..."):
            encoder = DatasetEncoderFactory(train_data)
            columns_to_encode = encoder.dataset.select_dtypes(
                include=["object"]
            ).columns
            total_columns = len(columns_to_encode)

            # Visualization elements
            progress_bar = st.progress(0)
            status_text = st.empty()
            encoded_preview_placeholder = st.empty()

            for idx, column in enumerate(columns_to_encode, start=1):
                status_text.text(f"Encoding column {idx}/{total_columns}: {column}")
                unique_values = encoder.dataset[column].nunique()
                with st.spinner(f"Applying encoding to column: {column}"):
                    time.sleep(4)  # Simulate processing time for visualization
                    if unique_values <= 10:
                        encoder.encode_label(column)
                    else:
                        encoder.encode_one_hot(column)

                # Update progress
                progress_bar.progress(idx / total_columns)

                # Preview of encoded dataset (updates incrementally)
                encoded_preview_placeholder.write(
                    f"### Encoding Progress: {column}\nPreview of Encoded Dataset:"
                )
                encoded_preview_placeholder.write(encoder.dataset.head())

            # Finalize encoding
            encoded_df = encoder.apply_encoding()
            st.session_state.encoded_df_var = encoded_df

            # Final preview of the dataset
            st.write("### Encoded Dataset Preview")
            st.write(encoded_df.head())

        st.success("Dataset encoded successfully!")

    # Imputation
    st.subheader("Step 2: Apply KNN Imputation")

    if st.session_state.encoded_df_var is not None:
        if st.button("Start KNN Imputation"):
            with st.spinner("Applying KNN Imputation..."):
                encoded_df = st.session_state.encoded_df_var.copy()

                # Initialize imputer
                imputer = KNNImputerFactory(
                    n_neighbors=5, metric="euclidean", aggregation="mean"
                )

                # Visualization elements
                total_rows = len(encoded_df)
                progress_bar = st.progress(0)
                status_text = st.empty()
                imputed_preview_placeholder = st.empty()

                # Adjust update frequency based on dataset size
                update_frequency = max(
                    1, total_rows // 50
                )  # Update every 2% of the dataset

                # Simulate progress visualization
                for idx in range(1, total_rows + 1):
                    if (
                        idx % update_frequency == 0 or idx == total_rows
                    ):  # Update at intervals
                        status_text.text(f"Processing row {idx}/{total_rows}")
                        progress_bar.progress(idx / total_rows)

                        # Update preview periodically
                        if idx % (5 * update_frequency) == 0 or idx == total_rows:
                            imputed_preview_placeholder.write(
                                f"### Progress: Row {idx}/{total_rows}\nPreview of Dataset (Before Imputation):"
                            )
                            imputed_preview_placeholder.write(encoded_df.head())

                # Apply KNN Imputation to the entire dataset
                imputed_data = imputer.fit_transform(encoded_df.values)
                imputed_df = pd.DataFrame(imputed_data, columns=encoded_df.columns)
                st.session_state.imputed_df_var = imputed_df

                # Final preview of imputed dataset
                st.write("### Imputed Dataset Preview")
                st.write(imputed_df.head())

            st.success("KNN Imputation completed successfully!")
    else:
        st.info("Please encode the dataset before applying KNN imputation.")

    # Decoding
    st.subheader("Step 3: Decoding the Imputed Dataset")
    if st.session_state.imputed_df_var is not None:
        if st.button("Start Decoding Process"):
            with st.spinner("Decoding the dataset..."):
                imputed_df = st.session_state.imputed_df_var.copy()

                # Initialize decoder
                decoder = DatasetDecoderFactory(imputed_df)

                # Visualization elements
                total_rows = len(imputed_df)
                progress_bar = st.progress(0)
                status_text = st.empty()
                decoded_preview_placeholder = st.empty()

                # Adjust update frequency based on dataset size
                update_frequency = max(
                    1, total_rows // 50
                )  # Update every 2% of the dataset

                # Simulate progress visualization
                for idx in range(1, total_rows + 1):
                    if (
                        idx % update_frequency == 0 or idx == total_rows
                    ):  # Update at intervals
                        status_text.text(f"Processing row {idx}/{total_rows}")
                        progress_bar.progress(idx / total_rows)

                        # Update preview periodically
                        if idx % (5 * update_frequency) == 0 or idx == total_rows:
                            decoded_preview_placeholder.write(
                                f"### Progress: Row {idx}/{total_rows}\nPreview of Dataset (During Decoding):"
                            )
                            decoded_preview_placeholder.write(imputed_df.head())

                # Apply decoding to the entire dataset
                decoded_df = decoder.decode(imputed_df)
                st.session_state.decoded_df_var = decoded_df

                # Final preview of decoded dataset
                st.write("### Decoded Dataset Preview")
                st.write(decoded_df.head())

            st.success("Decoding completed successfully!")
    else:
        st.info("Please complete the imputation process before starting decoding.")

    st.subheader("Step 4: Store Preprocessed Dataset to Database")

    if st.session_state.get("decoded_df_var") is not None:
        if st.button("Store Dataset in Database"):
            try:
                # Retrieve the preprocessed DataFrame from session state
                preprocessed_df = st.session_state.decoded_df_var

                # Specify the target table name in the database
                table_name = "unsw_nb15_preprocessed_dataset"

                # Store the dataset in the database
                bulk_store_dataset(table_name, preprocessed_df)

                st.success(
                    f"Preprocessed dataset successfully stored in table: {table_name}"
                )
            except Exception as e:
                st.error(f"Failed to store the dataset in the database: {e}")
    else:
        st.info("Please complete the decoding process before storing the dataset.")


if __name__ == "__main__":
    imputation_page()
