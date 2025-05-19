import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates

# Load color dataset
@st.cache_data
def load_colors():
    return pd.read_csv("colors.csv")

color_data = load_colors()
st.write("🎨 Loaded Color Data Sample:")
st.dataframe(color_data.head())

# Find closest color name
def get_color_name(R, G, B, color_data):
    try:
        distances = ((color_data['R'] - R)**2 + 
                     (color_data['G'] - G)**2 + 
                     (color_data['B'] - B)**2).pow(0.5)
        closest_index = distances.idxmin()
        return color_data.loc[closest_index]
    except Exception as e:
        st.error(f"Error finding closest color: {e}")
        return {'color_name': 'Unknown', 'hex': '#000000'}

# Streamlit UI
st.title("🎨 Color Detection from Image (No OpenCV)")

uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.write("🖱️ **Click on the image below to detect a color**")

    coords = streamlit_image_coordinates(image, key="click_image")

    if coords:
        x, y = int(coords['x']), int(coords['y'])
        st.write(f"📍 Clicked Coordinates: ({x}, {y})")

        image_np = np.array(image)
        if 0 <= y < image_np.shape[0] and 0 <= x < image_np.shape[1]:
            r, g, b = image_np[y, x]
            st.write(f"🎨 Clicked Pixel RGB: ({r}, {g}, {b})")

            color_info = get_color_name(r, g, b, color_data)
            hex_color = color_info['hex']

            st.markdown(f"""
            ### 🎯 Detected Color: `{color_info['color_name']}`
            - **RGB**: ({r}, {g}, {b})
            - **HEX**: `{hex_color}`
            """)
            st.markdown(f"""
            <div style="width:120px; height:50px; background-color:{hex_color}; border:1px solid #000;"></div>
            """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ Clicked outside image bounds.")
