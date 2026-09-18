import os
import joblib
import pandas as pd
import streamlit as st

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(page_title="Delivery Time Predictor", layout="centered")

@st.cache_resource
def load_artifacts():
    model_path = os.path.join(BASE_DIR, "model.pkl")
    prep_path = os.path.join(BASE_DIR, "preprocessor.pkl")
    
    if not os.path.exists(model_path) or not os.path.exists(prep_path):
        st.error("Model or Preprocessor files are missing.")
        st.stop()
        
    model = joblib.load(model_path)
    preprocessor = joblib.load(prep_path)
    return model, preprocessor

st.title("🚚 Delivery Time Predictor")
st.write("Enter the order details below to estimate delivery time.")

with st.form("prediction_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        order_hour = st.number_input("Order Hour (0-23)", min_value=0, max_value=23, value=18)
        is_weekend = st.selectbox("Is Weekend?", options=[0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
        weather = st.selectbox("Weather", ["Clear", "Rainy", "Foggy", "Stormy"])
        vehicle_type = st.selectbox("Vehicle Type", ["Motorcycle", "Scooter", "Bicycle"])
        rider_experience = st.number_input("Rider Experience (Years)", min_value=0.0, value=3.5, step=0.5)

    with col2:
        restaurant_load = st.selectbox("Restaurant Load", ["Low", "Medium", "High"])
        prep_time = st.number_input("Preparation Time (Min)", min_value=0.0, value=15.0, step=1.0)
        distance = st.number_input("Road Distance (km)", min_value=0.0, value=5.2, step=0.1)
        traffic_level = st.selectbox("Traffic Level", ["Low", "Medium", "High", "Jam"])
        avg_speed = st.number_input("Average Speed (km/h)", min_value=1.0, value=25.0, step=1.0)
        
    submit_btn = st.form_submit_button("Predict Delivery Time", use_container_width=True)

if submit_btn:
    try:
        model, preprocessor = load_artifacts()
        
        input_data = pd.DataFrame([{
            "Order_Hour": order_hour,
            "Is_Weekend": is_weekend,
            "Weather": weather,
            "Vehicle_Type": vehicle_type,
            "Rider_Experience_Years": rider_experience,
            "Restaurant_Load": restaurant_load,
            "Preparation_Time_Min": prep_time,
            "Road_Distance_km": distance,
            "Traffic_Level": traffic_level,
            "Average_Speed_kmph": avg_speed
        }])

        processed_data = preprocessor.transform(input_data)
        prediction = model.predict(processed_data)[0]
        
        st.success(f"⏱️ **Estimated Delivery Time:** {round(float(prediction), 2)} mins")
    except Exception as e:
        st.error(f"Error making prediction: {e}")
