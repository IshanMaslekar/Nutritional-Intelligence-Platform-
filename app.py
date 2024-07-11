### Health Management APP
from dotenv import load_dotenv

load_dotenv() ## load all the environment variables

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("Your_API_KEY"))

## Function to load Google Gemini Pro Vision API And get response

def get_gemini_repsonse(input,image,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,image[0],prompt])
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
##initialize our streamlit app

st.set_page_config(page_title="Gemini Health App")

st.header("Gemini Health App")
input=st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit=st.button("Tell me the total calories")

input_prompt = """
You are a nutrition expert tasked with analyzing the food items in the provided image. Please perform the following:

1. Identify and list each food item present in the image.
2. For each food item, provide:
   - The estimated calorie content.
   - The estimated sodium content.
   - Any other relevant nutritional information (e.g., protein, fat, carbohydrates, sugar).
3. List the items and their nutritional content in the following format:
   - Item 1:
     - Calories: X calories
     - Sodium: Y mg
     - Protein: Z g
     - Fat: A g
     - Carbohydrates: B g
     - Sugar: C g
   - Item 2:
     - Calories: X calories
     - Sodium: Y mg
     - Protein: Z g
     - Fat: A g
     - Carbohydrates: B g
     - Sugar: C g
   - ...

4. Provide an overall summary of the meal, including:
   - Total calorie count.
   - Total sodium intake.
   - Any other notable nutritional aspects (e.g., high protein, high sugar).
   
5. Offer suggestions for healthier alternatives or modifications to reduce calorie and sodium intake if applicable.

6. If any food items cannot be identified, mention them separately and provide potential suggestions or ask for additional clarification.

Ensure the analysis is accurate, detailed, and easy to understand. Provide clear and concise information that can help users make informed dietary choices.
"""


## If submit button is clicked

if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_repsonse(input_prompt,image_data,input)
    st.subheader("The Response is")
    st.write(response)

