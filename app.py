import streamlit as st
import numpy as np
import joblib

# 1. Load the saved model and scaler
# We use @st.cache_resource so it only loads these files once, making the app much faster
@st.cache_resource
def load_artifacts():
    model = joblib.load('concrete_rf_model.pkl')
    scaler = joblib.load('concrete_scaler.pkl')
    return model, scaler

model, scaler = load_artifacts()

# 2. Build the User Interface
st.title("Concrete Compressive Strength Predictor")
st.write("Enter the concrete mix details below to predict its compressive strength.")

# 3. Create a form for user inputs
# Using a form prevents the app from recalculating every time a single number is typed
with st.form("prediction_form"):
    st.subheader("Mixture Ingredients")
    
    # We use columns to make the UI look cleaner
    col1, col2 = st.columns(2)
    
    with col1:
        cement = st.number_input("Cement (kg/m³)", min_value=0.0, value=250.0)
        slag = st.number_input("Blast Furnace Slag (kg/m³)", min_value=0.0, value=0.0)
        flyash = st.number_input("Fly Ash (kg/m³)", min_value=0.0, value=0.0)
        water = st.number_input("Water (kg/m³)", min_value=0.0, value=150.0)
        
    with col2:
        superplasticizer = st.number_input("Superplasticizer (kg/m³)", min_value=0.0, value=0.0)
        coarse = st.number_input("Coarse Aggregate (kg/m³)", min_value=0.0, value=1000.0)
        fine = st.number_input("Fine Aggregate (kg/m³)", min_value=0.0, value=750.0)
        age = st.number_input("Age (days)", min_value=1, value=28) # 28 days is standard testing age
        
    # The submit button
    submit_button = st.form_submit_button("Predict Strength")

# 4. Make the prediction when the button is clicked
if submit_button:
    # Gather the inputs into the same format the model was trained on
    features = np.array([[cement, slag, flyash, water, superplasticizer, coarse, fine, age]])
    
    # Scale the inputs using the saved scaler
    features_scaled = scaler.transform(features)
    
    # Generate the prediction
    prediction = model.predict(features_scaled)[0]
    
    # Display the result prominently

    st.success(f"### Predicted Compressive Strength: {prediction:.2f} MPa")
