import streamlit as st
import requests
import os

# Backend URL
BACKEND_URL = "http://127.0.0.1:8000/predict/"

st.title("AurumAI - Jewellery Image Retrieval")

# Input prompt
prompt = st.text_input("Enter your jewellery description:")

if st.button("Search"):
    if prompt:
        try:
            response = requests.get(BACKEND_URL, params={"prompt": prompt})
            response.raise_for_status()  # Raise error for failed request (e.g., backend down)

            result = response.json()
            selected_image = result.get("selected_image", "")

            if selected_image and selected_image != "No match found":
                image_path = os.path.join("images", selected_image)  # Ensure correct path
                
                if os.path.exists(image_path):  # Check if image exists
                    st.image(image_path, caption="Best Matching Jewelry", use_container_width=True)
                else:
                    st.error(f"Image file '{selected_image}' not found in 'images/' folder.")
            else:
                st.error("No matching image found.")

        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to backend: {e}")

