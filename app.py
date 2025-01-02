import streamlit as st

# Configure the app's page to have no sidebar
st.set_page_config(
    page_title="Net Guard Dashboard",
    page_icon="🔒",
    layout="wide",
)

# Enhanced CSS styling
st.markdown("""
    <style>
        /* Hide sidebar */
        .css-1d391kg {display: none;}
        .css-18e3th9 {display: none;}
        
        /* Dark mode styling */
        body {
            background-color: #121212; /* Dark background */
            color: #ffffff; /* Light text */
        }
        .main-header {
            color: #bb86fc; /* Light purple */
            text-align: center;
            padding: 2rem 0;
        }
        .subheader {
            color: #e0e0e0; /* Light gray */
            text-align: center;
            margin-bottom: 2rem;
        }
        .feature-card {
            background-color: #1e1e1e; /* Dark card background */
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.3);
            margin-bottom: 1rem;
        }
        .step-card {
            background-color: #1e1e1e; /* Dark step card background */
            padding: 1.5rem;
            border-left: 4px solid #bb86fc; /* Light purple border */
            margin-bottom: 1.5rem;
            border-radius: 0 10px 10px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }
        .footer {
            text-align: center;
            padding: 2rem 0;
            color: #aaaaaa; /* Light gray for footer */
            border-top: 1px solid #333; /* Darker border */
        }
        /* Sidebar styling */
        .css-1d391kg {
            background-color: #1e1e1e;  /* Dark sidebar background */
        }
        .css-1d391kg .stButton button {
            width: 100%;
            background-color: #bb86fc;  /* Purple buttons */
            color: #ffffff;
            border: none;
            border-radius: 5px;
            padding: 10px;
            margin: 5px 0;
        }
        .css-1d391kg h1 {
            color: #bb86fc;  /* Purple headers */
            font-size: 1.5em;
            padding: 1rem 0;
        }
        /* Sidebar links */
        .css-1d391kg a {
            color: #e0e0e0;
        }
        /* Sidebar divider */
        .css-1d391kg hr {
            border-color: #333333;
        }
    </style>
""", unsafe_allow_html=True)

# Enhanced header section
st.markdown('<h1 class="main-header">Net Guard Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<h3 class="subheader">A Comprehensive Solution for Anomaly Detection in Network Logs</h3>', unsafe_allow_html=True)

# Welcome message in a container
with st.container():
    st.markdown("""
    <div class="feature-card">
        Welcome to the <b>Net Guard Dashboard</b>! This platform guides you through the entire process of network anomaly detection, 
        from raw dataset loading to advanced clustering and anomaly detection using autoencoders. Explore each step in detail by 
        navigating through the options below.
    </div>
    """, unsafe_allow_html=True)

# Features section with columns
st.markdown("### 🎯 Features of the Dashboard")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="feature-card">
        • 📊 <b>Load Raw Datasets</b>: Import and inspect your network log data<br>
        • 🔍 <b>Handle Missing Values</b>: Check and impute missing entries<br>
        • 🔄 <b>Encode Categorical Data</b>: Transform categorical features<br>
        • 📈 <b>Visualize Data</b>: Generate visualizations to understand data distributions<br>
        • 📊 <b>Data Normalization</b>: Normalize data for better model performance<br>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        • 🤖 <b>Apply KNN Imputation</b>: Ensure data integrity<br>
        • 📈 <b>Cluster Analysis</b>: Understand network patterns<br>
        • 🚨 <b>Anomaly Detection</b>: Detect irregularities<br>
        • 📊 <b>Generate Reports</b>: Create detailed reports of findings and insights<br>
        • 📚 <b>Documentation</b>: Access detailed documentation for each feature<br>
    </div>
    """, unsafe_allow_html=True)

# Workflow section
st.markdown("### 🔄 Detailed Workflow of Net Guard")

# Add each step in a card-like container
steps = [
    ("Step 1: Load and Inspect Raw Data", "Loading raw dataset containing network log data..."),
    ("Step 2: Handle Missing Values", "Using KNN Imputer to fill in missing entries..."),
    ("Step 3: Encode Categorical Data", "Converting categorical features into numeric values..."),
    ("Step 4: Data Normalization", "Normalizing data for better model performance..."),
    ("Step 5: Apply KNN Imputation", "Applying K-Nearest Neighbors imputation..."),
    ("Step 6: Decode Data", "Reversing encoding for readable format..."),
    ("Step 7: Load and Scale Data", "Scaling features for consistent analysis..."),
    ("Step 8: Perform K-Means Clustering", "Grouping data points based on similarity..."),
    ("Step 9: Apply Anomaly Detection", "Using autoencoders to detect network anomalies..."),
    ("Step 10: Visualize Results", "Creating visualizations to interpret clustering and anomalies..."),
    ("Step 11: Generate Reports", "Compiling findings into a comprehensive report..."),
    ("Step 12: Review and Feedback", "Gathering user feedback for continuous improvement...")
]

for title, description in steps:
    st.markdown(f"""
    <div class="step-card">
        <h4>{title}</h4>
        {description}
    </div>
    """, unsafe_allow_html=True)

# User Feedback Section
st.markdown("### 📝 User Feedback")
st.markdown("""
We value your feedback! Please let us know your thoughts about the Net Guard Dashboard:
""")
feedback = st.text_area("Your Feedback:", height=150)
if st.button("Submit Feedback"):
    st.success("Thank you for your feedback!")

# Rest of your existing logic for page navigation
page = st.query_params.get("page", ["Home"])[0]

if page == "Load_Dataset":
    st.header("📥 Load Raw Dataset")
    st.write("Here you can import and inspect your network log data.")

elif page == "Autoencoder":
    st.header("🔍 Anomaly Detection")
    st.write("Here you can apply autoencoder models to detect anomalies in the data.")

elif page == "Load_and_Store_Dataset":
    st.header("💾 Load and Store Dataset")
    st.write("This is where you load and store your dataset for further processing.")

else:
    st.markdown("""
    <div style="text-align: left; margin-top: 50px;">
        <h1 style="font-size: 3em; color: #bb86fc;">🚀 Start Exploring</h1>
        <p style="font-size: 1.5em; color: #e0e0e0;">Click the button below to try the Anomaly Detector!</p>
        <div style="margin-top: 20px;">
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Try the Anomaly Detector", key="start_button"):
        st.switch_page("pages/load_and_store_dataset.py")

# Enhanced footer
st.markdown("""
<div class="footer">
    <b>Net Guard Dashboard</b> | Developed by [Your Name] | Powered by Streamlit
</div>
""", unsafe_allow_html=True)

# Create the sidebar
with st.sidebar:
    st.title("Navigation")
    st.markdown("---")
    if st.button("Home"):
        st.experimental_set_query_params(page="Home")
    if st.button("Load Dataset"):
        st.experimental_set_query_params(page="Load_Dataset")
    if st.button("Anomaly Detection"):
        st.experimental_set_query_params(page="Autoencoder")
    st.markdown("---")
    st.markdown("### Settings")
    # Add any settings controls here
