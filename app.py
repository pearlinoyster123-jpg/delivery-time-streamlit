import os
import joblib
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Delivery Time Predictor",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Load artifacts with caching
@st.cache_resource
def load_models():
  base_dir = os.path.dirname(os.path.abspath(__file__))
  model_path = os.path.join(base_dir, "model.pkl")
  prep_path = os.path.join(base_dir, "preprocessor.pkl")

  if not os.path.exists(model_path) or not os.path.exists(prep_path):
    return None, None

  model = joblib.load(model_path)
  preprocessor = joblib.load(prep_path)
  return model, preprocessor


model, preprocessor = load_models()

# Fancy Neon Dark Theme CSS
st.markdown(
    """
    <style>
    /* Dark Background */
    .stApp {
        background-color: #0d1117 !important;
        color: #f0f6fc !important;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #161b22 !important;
        border-right: 2px solid #8a2be2 !important;
    }
    
    /* Main Large Title (h1) Styling */
    h1 {
        color: #00f2fe !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 72px !important;  /* Enlarged title size */
        font-weight: 800 !important;
        text-shadow: 0 0 15px rgba(0, 242, 254, 0.5);
        margin-bottom: 5px !important;
    }

    /* Subheaders (h2, h3) Styling */
    h2, h3 {
        color: #00f2fe !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 700 !important;
        text-shadow: 0 0 10px rgba(0, 242, 254, 0.3);
    }
    
    /* Ensure ALL text labels are bright and readable */
    p, span, label, div, li {
        color: #f0f6fc !important;
        font-size: 15px !important;
    }
    
    /* Card Container */
    div[data-testid="stForm"] {
        background: #161b22 !important;
        border: 1px solid #30363d !important;
        border-radius: 16px !important;
        padding: 24px !important;
        box-shadow: 0 8px 24px rgba(0,0,0,0.5);
    }

    /* Input Field Styling */
    input, select, div[role="combobox"] {
        background-color: #21262d !important;
        color: #ffffff !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
    }
    
    /* Fancy Gradient Button */
    div.stButton > button {
        background: linear-gradient(135deg, #8a2be2 0%, #4a00e0 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 14px 28px !important;
        font-size: 18px !important;
        font-weight: bold !important;
        width: 100% !important;
        box-shadow: 0 4px 15px rgba(138, 43, 226, 0.4);
        transition: all 0.3s ease;
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(138, 43, 226, 0.7) !important;
    }

    /* Prediction Result Box */
    .result-card {
        background: linear-gradient(135deg, #1f293d 0%, #111827 100%);
        border: 2px solid #00f2fe;
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        margin-top: 20px;
        box-shadow: 0 0 20px rgba(0, 242, 254, 0.2);
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- SIDEBAR ---
with st.sidebar:
  st.title("⚡ Navigation")
  st.markdown("---")
  st.subheader("📌 About App")
  st.write(
      "Real-time machine learning engine predicting food & package delivery"
      " timelines."
  )

  st.markdown("---")
  st.subheader("👨‍💻 Developer")
  st.markdown("**Umme Ahmad**")
  st.caption("Data Scientist & ML Engineer")

  st.markdown("---")
  st.subheader("🛠 Tech Stack")
  st.markdown("- **Framework:** Streamlit")
  st.markdown("- **Model:** Scikit-Learn")
  st.markdown("- **Engine:** Python 3.11")

# --- MAIN CONTENT ---
st.title("🚚 Delivery Time Predictor")
st.markdown("Fill in the order details below to estimate delivery time.")

# Form Layout
with st.form("prediction_form"):
  col1, col2 = st.columns(2)

  with col1:
    order_hour = st.number_input(
        "Order Hour (0-23)", min_value=0, max_value=23, value=18
    )
    is_weekend_str = st.selectbox("Is Weekend?", ["No", "Yes"])
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

  submit_btn = st.form_submit_button("✨ Calculate Delivery Time")

# --- PREDICTION RESULT SECTION ---
if submit_btn:
  if model is None or preprocessor is None:
    st.error("⚠️ Model or Preprocessor files (`.pkl`) are missing from repository.")
  else:
    is_weekend = 1 if is_weekend_str == "Yes" else 0

    input_df = pd.DataFrame([{
        "Order_Hour": order_hour,
        "Is_Weekend": is_weekend,
        "Weather": weather,
        "Vehicle_Type": vehicle_type,
        "Rider_Experience_Years": rider_exp,
        "Restaurant_Load": restaurant_load,
        "Preparation_Time_Min": prep_time,
        "Road_Distance_km": road_distance,
        "Traffic_Level": traffic_level,
        "Average_Speed_kmph": avg_speed,
    }])

    try:
      processed_data = preprocessor.transform(input_df)
      prediction = model.predict(processed_data)[0]

      st.markdown(
          f"""
            <div class="result-card">
                <h3 style="color: #00f2fe !important; margin: 0;">🎯 Estimated Delivery Time</h3>
                <h1 style="color: #ffffff !important; font-size: 48px; margin: 10px 0;">{round(prediction, 1)} <span style="font-size: 24px; color: #00f2fe;">Minutes</span></h1>
                <p style="color: #8b949e !important;">Based on traffic conditions, distance, and rider profile.</p>
            </div>
            """,
          unsafe_allow_html=True,
      )
    except Exception as e:
      st.error(f"Error during prediction: {str(e)}")
