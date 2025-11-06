import streamlit as st
import pickle
import json
import numpy as np
import os

# Page config
st.set_page_config(
    page_title="Delhi House Price Predictor",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load model and data
@st.cache_resource
def load_saved_artifacts():
    """Load the trained model and location data"""
    try:
        # Load from artifacts directory
        base_dir = os.path.dirname(__file__)
        
        # Load columns
        columns_path = os.path.join(base_dir, "artifacts", "columns.json")
        with open(columns_path, "r") as f:
            data_columns = json.load(f)['data_columns']
            locations = data_columns[3:]  # first 3 columns are sqft, bath, bhk
        
        # Load model
        model_path = os.path.join(base_dir, "artifacts", "delhi_home_prices_model.pickle")
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
            
        return data_columns, locations, model
        
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None, None, None

def get_estimated_price(location, sqft, bhk, bath, data_columns, model):
    """Predict house price based on input parameters"""
    try:
        loc_index = data_columns.index(location.lower())
    except:
        loc_index = -1

    x = np.zeros(len(data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1

    return round(model.predict([x])[0], 2)

# Main app
def main():
    # Load artifacts
    data_columns, locations, model = load_saved_artifacts()
    
    if not data_columns or not locations or not model:
        st.stop()
    
    # Header
    st.title("🏠 Delhi House Price Predictor")
    st.markdown("### Get accurate price estimates for properties across Delhi & NCR")
    
    # Create two columns for layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### Property Details")
        
        # Area input
        sqft = st.number_input(
            "Area (Square Feet)",
            min_value=100,
            max_value=10000,
            value=1000,
            step=100,
            help="Enter the total area of the property in square feet"
        )
        
        # BHK selection
        bhk = st.selectbox(
            "BHK (Bedrooms)",
            options=[1, 2, 3, 4, 5],
            index=1,  # Default to 2 BHK
            help="Select the number of bedrooms"
        )
        
        # Bathrooms selection
        bath = st.selectbox(
            "Bathrooms",
            options=[1, 2, 3, 4, 5],
            index=1,  # Default to 2 bathrooms
            help="Select the number of bathrooms"
        )
        
        # Location selection
        location = st.selectbox(
            "Location",
            options=sorted(locations),
            help="Select the location of the property"
        )
    
    with col2:
        st.markdown("#### Price Prediction")
        
        # Prediction button
        if st.button("🔮 Predict Price", type="primary", use_container_width=True):
            with st.spinner("Calculating price estimate..."):
                try:
                    estimated_price = get_estimated_price(
                        location, sqft, bhk, bath, data_columns, model
                    )
                    
                    # Display result
                    st.success("Price Estimated Successfully!")
                    
                    # Price display
                    st.metric(
                        label="Estimated Price",
                        value=f"₹ {estimated_price} Lakhs",
                        help="This is an estimated price based on the provided parameters"
                    )
                    
                    # Property summary
                    st.markdown("#### Property Summary")
                    st.write(f"**Location:** {location}")
                    st.write(f"**Area:** {sqft} sq ft")
                    st.write(f"**Configuration:** {bhk} BHK, {bath} Bath")
                    st.write(f"**Price per sq ft:** ₹ {round((estimated_price * 100000) / sqft, 2)}")
                    
                except Exception as e:
                    st.error(f"Error predicting price: {str(e)}")
        
        # Info section
        st.markdown("#### ℹ️ About")
        st.info("""
        This AI-powered tool predicts house prices in Delhi & NCR region based on:
        - Property location
        - Total area in square feet
        - Number of bedrooms (BHK)
        - Number of bathrooms
        
        The model is trained on real estate data from Delhi, Noida, Gurgaon, and Ghaziabad.
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("**Note:** Prices are estimates and may vary based on market conditions, property condition, and other factors.")

if __name__ == "__main__":
    main()