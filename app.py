import streamlit as st
import google.generativeai as genai
import os
from PIL import Image
import numpy as np

# Configure Gemini API
genai.configure(api_key="AIzaSyDrcSJY77xcaertsGJENaYZtB-shvrTrXI")

# Define function to get Gemini response
def get_gemini_response(input_prompt, image):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_prompt, image[0]])
    return response.text

# Set up Streamlit app
st.title("Doctor's Prescription Text Extractor")
st.write("Upload an image of a prescription to extract the text using AI.")

# Upload image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Process uploaded image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Prescription', use_column_width=True)

    # Convert image to bytes for API
    image_data = [{
        "mime_type": uploaded_file.type,
        "data": uploaded_file.getvalue()
    }]

    # Define prompt for prescription analysis
    input_prompt = """
    You are an advanced medical assistant AI. Extract the text from the given doctor's prescription image.
    Correct any spelling errors, identify medical terms, and format the output cleanly and readably.
    If any medicines, dosages, or instructions are present, present them in a structured format.
    """

    # Get response from Gemini model
    st.subheader("Extracting text... 🔍")
    response_text = get_gemini_response(input_prompt, image_data)

    # Display extracted text
    st.subheader("Extracted Text")
    st.text_area("Text Output", response_text, height=300)

    # Option to download the output
    st.download_button(
        label="Download Extracted Text",
        data=response_text,
        file_name="extracted_prescription.txt",
        mime="text/plain"
    )

# Footer
st.write("Built with Streamlit, Google Gemini AI")
