import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image
import io

# Load the environment variables
load_dotenv()

# Configure Google API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# Function to get response from Gemini model (using gemini-1.5-flash)
def get_gemini_response(input_prompt, image_data):
    model = genai.GenerativeModel("gemini-1.5-flash")  # Updated model
    # Generate content using the input prompt and image data
    response = model.generate_content([input_prompt, image_data])
    return response.text


# Function to prepare the image data
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        # Convert the uploaded image file to binary data
        bytes_data = uploaded_file.getvalue()

        # Create an Image object using PIL
        image = Image.open(io.BytesIO(bytes_data))

        # Ensure the image is in the correct format (JPEG or PNG)
        if uploaded_file.type in ["image/jpeg", "image/png"]:
            return image
        else:
            st.error("Unsupported image format. Please upload a JPEG or PNG file.")
            return None
    else:
        st.error("No file uploaded.")
        return None


# Streamlit app
st.set_page_config(page_title="Calories Advisor App")

st.header("Calories Advisor App")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

# Button to submit the image and get the calorie information
submit = st.button("Tell me about the total calories")

# Input prompt for the Gemini model
input_prompt = """
You are an expert nutritionist. Please analyze the food items from the image,
calculate the total calories, and provide the details of each food item with calorie intake
in the following format:

1. Item 1 - no of calories
2. Item 2 - no of calories
---
Also mention whether the food is healthy or not, and provide a percentage breakdown of the 
ratio of carbohydrates, fats, fibers, sugar, and other important nutritional components in the diet.
"""

if submit and uploaded_file is not None:
    # Prepare image data for the API
    image_data = input_image_setup(uploaded_file)
    if image_data:
        # Get the Gemini model's response
        response = get_gemini_response(input_prompt, image_data)
        st.subheader("The Response is:")
        st.write(response)
else:
    st.warning("Please upload an image before submitting.")
