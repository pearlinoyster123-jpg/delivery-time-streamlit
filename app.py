import joblib
import pandas as pd
import streamlit as st

# Page setup
st.set_page_config(
    page_title="Delivery Time Predictor", page_icon="🚚", layout="wide"
)

# Custom Red & Black Theme CSS
st.markdown(
    """
    <style>
    /* Dark theme background */
    .stApp {
        background-color: #0e0e10;
        color: #ffffff;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #16161a;
        border-right: 2px solid #e50914;
    }
    
    /* Red Accent Headers */
    h1, h2, h3 {
        color: #e50914 !important;
        font-weight: 700;
    }
    
    /* Custom Card Containers */
    div[data-testid="stForm"] {
        background-color: #1a1a1e;
        border: 1px solid #333333;
        border-radius: 12px;
        padding: 20px;
    }
    
    /* Red Styled Buttons */
    .stButton>button {
        background-color: #e50914 !important;
        color: white !important;
        border-radius: 8px;
        border: none;
        font-weight: bold;
        width: 100%;
        padding: 10px;
    }
    .stButton>button:hover {
        background-color: #b20710 !important;
    }
    
    /* Input Box Styles */
    .stNumberInput, .stSelectbox {
        color: white;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- SIDEBAR: Developer Info & App Overview ---
with st.sidebar:
  st.title("📌 About App")
  st.write(
      "This **Delivery Time Predictor** uses machine learning to estimate"
      " order fulfillment times in real-time based on distance, traffic,"
      " weather, and rider experience."
  )

  st.markdown("---")
  st.subheader("👨‍💻 Developer")
  st.markdown("**Umme Ahmad**")
  st.caption("Data Scientist & ML Engineer")

  st.markdown("---")
  st.subheader("🛠 Tech Stack")
  st.markdown("- **Framework:** Streamlit")
  st.markdown("- **Model:** Scikit-Learn Pipeline")
  st.markdown("- **Language:** Python 3.11")

# --- MAIN CONTENT ---
st.title("🚚 Delivery Time Predictor")
st.markdown(
    "Enter order parameters below to generate an estimated delivery window."
)

# Form Layout
with st.form("prediction_form"):
  col1, col2 = st.columns(2)

  with col1:
    order_hour = st.number_input(
        "Order Hour (0-23)", min_value=0, max_value=23, value=18
    )
    is_weekend = st.selectbox("Is Weekend?", ["No", "Yes"])
    weather = st.selectbox(
        "Weather", ["Clear", "Rainy", "Foggy", "Windy", "Stormy"]
    )
    vehicle_type = st.selectbox(
        "Vehicle Type", ["Motorcycle", "Bicycle", "Scooter", "Car"]
    )
    rider_exp = st.number_input(
        "Rider Experience (Years)", min_value=0.0, value=3.5, step=0.5
    )

  with col2:
    restaurant_load = st.selectbox("Restaurant Load", ["Low", "Medium", "High"])
    prep_time = st.number_input(
        "Preparation Time (Min)", min_value=1.0, value=15.0, step=1.0
    )
    road_distance = st.number_input(
        "Road Distance (km)", min_value=0.1, value=5.2, step=0.1
    )
    traffic_level = st.selectbox("Traffic Level", ["Low", "Medium", "High"])
    avg_speed = st.number_input(
        "Average Speed (km/h)", min_value=1.0, value=25.0, step=1.0
    )

  submit_btn = st.form_submit_button("Predict Delivery Time")

# --- PREDICTION HANDLING ---
if submit_btn:
  # Insert your model loading & inference code here
  st.success("Calculating estimated delivery time...")
