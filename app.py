import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

# Load API key from environment variables
load_dotenv()
genai.configure(api_key=os.getenv("API_KEY"))

def get_gemini_response(input_text, image, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([prompt, image])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        # Convert uploaded file into PIL Image
        image = Image.open(uploaded_file)
        return image
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit app
input_prompt = """
You are an expert nutritionist. Look at the food items in the image and calculate the total calories.  
And one strict rule: no need to give response like the the data is missing or cant identify if we dont have the proper data like the data is missing. you are free to asume the average .
Also, provide details for each food item with calories in the following format:
 in table format as below 
1| Item 1 | number of calories  | how we calculate that food  
2  Item 2 | number of calories  | how we calculate that food 


and in the end give suggestion if required or likely to 
------
"""

st.set_page_config(page_title="AI Nutritionist App")
st.header("AI Nutritionist App")

innput = st.text_input("Input Prompt", key="input")
uploaded_file = st.file_uploader("Choose an image ...", type=["jpg", "jpeg", "png"])

image = None

if uploaded_file is not None:
    # Show the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded image", use_column_width=True)

submit = st.button("Tell me the Total Calories")

if submit and uploaded_file is not None:
    image = input_image_setup(uploaded_file)  # Ensure image is in the correct format
    response = get_gemini_response(innput, image, input_prompt)
    st.subheader("The response is ...")
    st.write(response)
