import streamlit as st
import requests


# Specify the path to your GIF file
# Update this with the correct path

# Display the GIF
# st.image(gif_path, use_column_width=True)
# Configure the app's page
st.set_page_config(
    page_title="Net Guard Dashboard",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Enhanced CSS styling with animations and better aesthetics
st.markdown(
    """
    <style>
        /* Base styles and resets */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        /* Hide Streamlit elements */
        section[data-testid="stSidebar"],
        .css-1d391kg,
        .css-18e3th9,
        div[data-testid="stSidebarNav"],
        footer {
            display: none !important;
        }
        
        /* Modern dark theme */
        body {
            background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 100%);
            color: #ffffff;
            font-family: 'Inter', sans-serif;
        }
        
        /* Hero section styling */
        .hero-container {
            text-align: center;
            padding: 5rem 2rem;
            background: linear-gradient(145deg, rgba(30,30,46,0.9) 0%, rgba(45,45,65,0.9) 100%);
            border-radius: 30px;
            margin: 2rem auto;
            max-width: 1400px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
            animation: fadeIn 1s ease-out;
        }
        
        /* Animated headline */
        .hero-headline {
            font-size: 4em;
            background: linear-gradient(120deg, #bb86fc, #7b2cbf);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1.5rem;
            font-weight: 800;
            line-height: 1.2;
            letter-spacing: -0.5px;
            animation: slideDown 0.8s ease-out;
            text-align: center;
        }
        
        /* Subtext with better readability */
        .hero-subtext {
            font-size: 1.6em;
            text-align: center !important; /* Ensure centering */
            color: #e0e0e0;
            margin-bottom: 3rem;
            line-height: 1.6;
            animation: fadeIn 1s ease-out 0.3s both;
        }
        
        /* Network visualization */
        .network-animation {
            position: relative;
            height: 450px;
            background: radial-gradient(circle at center, rgba(187,134,252,0.1) 0%, rgba(0,0,0,0) 70%);
            margin: 3rem 0;
            border-radius: 20px;
            overflow: hidden;
            animation: pulse 2s infinite;
        }
        
        /* Feature cards */
        .feature-card {
            background: rgba(30,30,46,0.7);
            padding: 2rem;
            border-radius: 20px;
            margin: 1rem 0;
            border: 1px solid rgba(187,134,252,0.1);
            transition: all 0.3s ease;
            animation: slideUp 0.8s ease-out;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(187,134,252,0.2);
            border-color: rgba(187,134,252,0.3);
        }
        
        /* Feature icons and text */
        .feature-icon {
            font-size: 2em;
            margin-bottom: 1rem;
            color: #bb86fc;
        }
        
        .feature-title {
            color: #bb86fc;
            font-size: 1.3em;
            margin-bottom: 0.5rem;
            font-weight: 600;
        }
        
        /* Button styling */
        .stButton button {
            background: linear-gradient(45deg, #bb86fc 0%, #7b2cbf 100%) !important;
            color: white !important;
            padding: 1em 3em !important;
            border-radius: 50px !important;
            font-size: 1.2em !important;
            font-weight: 600 !important;
            border: none !important;
            box-shadow: 0 4px 15px rgba(187,134,252,0.3) !important;
            transition: all 0.3s ease !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
            margin: 2rem auto !important;
            display: block !important;
        }
        
        .stButton button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(187,134,252,0.5) !important;
        }
        
        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        @keyframes slideDown {
            from { transform: translateY(-30px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        
        @keyframes slideUp {
            from { transform: translateY(30px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        
        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(187,134,252,0.4); }
            70% { box-shadow: 0 0 0 20px rgba(187,134,252,0); }
            100% { box-shadow: 0 0 0 0 rgba(187,134,252,0); }
        }
        
        /* Responsive design */
        @media (max-width: 768px) {
            .hero-headline { font-size: 2.5em; }
            .hero-subtext { font-size: 1.2em; }
            .network-animation { height: 300px; }
        }
        
        .hero-subtext {
            text-align: center !important; /* Force centering */
        }
        
         /* Animations */
         @keyframes slideIn {
        from { transform: translateX(-30px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
        }

         @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
        }
    </style>
""",
    unsafe_allow_html=True,
)

# Hero Section
st.markdown(
    """
<div class="hero-container">
    <h1 class="hero-headline">Detect Anomalies Before They Become Threats</h1>
    <h5 class="hero-subtext">Net Guard leverages advanced AI to ensure network security by detecting unauthorized access, malware, and unusual traffic patterns.</p>
</div>
""",
    unsafe_allow_html=True,
)

# CTA Button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("View Demo", key="demo_button", type="primary"):
        st.switch_page("pages/data_loading_page.py")

# Features section
st.markdown(
    """
<div style='padding: 2rem 0;'>
    <h2 style='text-align: center; color: #bb86fc; margin-bottom: 2rem; font-size: 2.5em;'>Why Choose Net Guard?</h2>
</div>
""",
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
    <div class="feature-card">
        <div class="feature-icon">🔍</div>
        <div class="feature-title">Real-time Detection</div>
        <p>Advanced monitoring system that continuously analyzes network traffic patterns and behaviors.</p>
    </div>
    
    <div class="feature-card">
        <div class="feature-icon">🤖</div>
        <div class="feature-title">AI-Powered Analysis</div>
        <p>State-of-the-art machine learning algorithms that adapt and learn from your network's unique patterns.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
    <div class="feature-card">
        <div class="feature-icon">🛡️</div>
        <div class="feature-title">Proactive Defense</div>
        <p>Stop potential threats before they can impact your systems with predictive analysis.</p>
    </div>
    
    <div class="feature-card">
        <div class="feature-icon">📊</div>
        <div class="feature-title">Interactive Insights</div>
        <p>Beautiful, intuitive dashboards that give you complete visibility into your network's security status.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

# How It Works Section
st.markdown(
    """
    <div style="padding: 4rem 0; text-align: center;">
        <h2 style="color: #bb86fc;">How It Works</h2>
        <p>Experience the power of Net Guard in just a few simple steps:</p>
        <ol>
            <li>Load your network logs.</li>
            <li>AI detects patterns and anomalies.</li>
            <li>Review results in an interactive dashboard.</li>
        </ol>
    </div>
    """,
    unsafe_allow_html=True,
)

# Footer
st.markdown(
    """
<div style="text-align: center; padding: 4rem 0; color: #bb86fc; font-size: 1.2em;">
    <p>Net Guard | Securing Networks with AI</p>
</div>
""",
    unsafe_allow_html=True,
)
