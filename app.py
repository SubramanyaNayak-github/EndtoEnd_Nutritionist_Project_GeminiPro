import os 
import streamlit as st
import google.generativeai as genai 
from dotenv import load_dotenv
from PIL import Image


load_dotenv()

genai.configure(api_key= os.getenv('GOOGLE_API_KEY'))


def gemini_response(input_prompt,image):
    model= genai.GenerativeModel('gemini-pro-vision')

    response = model.generate_content([input_prompt,image[0]])
    return response.text

def preprocess_input_image(uploaded_image):
    if uploaded_image is not None:
        bytes_data = uploaded_image.getvalue()

        image_parts = [ {
            'mime_type': uploaded_image.type,
            'data' : bytes_data
        }]

        return image_parts
    
    else:
        raise FileNotFoundError('No Image file Umploaded')
    


st.set_page_config(page_title = 'Nutrition Advisor Application')

st.header('Gemini Nutrition Application')

uploaded_image = st.file_uploader('Upload image here',type =['jpg','jpeg','png'])
image = ''
if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.image(image,caption = 'Uploaded Image', use_column_width= True)


submit = st.button('Tell me about the total calories')


input_prompt = """As a nutritionist, your task is to analyze images of food items and calculate the total calories. Provide detailed information on each food item along with its calorie intake in the following format:

1. Item 1 - Calories
2. Item 2 - Calories
...

Ensure accuracy in identifying food items and calculating portion sizes. Consider incorporating serving sizes and common portion measurements to 
provide more accurate nutritional information. Additionally, you may want to include recommendations for portion control and balanced meal planning 
to promote healthier dietary habits.

Output the total calories consumed for better understanding and tracking of dietary intake. This information can help individuals make informed decisions
about their food choices and maintain a balanced diet.

"""


if submit:
    image_data=preprocess_input_image(uploaded_image)
    response=gemini_response(input_prompt,image_data,input)
    st.subheader("The Response is")
    st.write(response)
