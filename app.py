import streamlit as st
from PIL import Image
import openai
import base64
import io
from openai import OpenAI
from dotenv import load_dotenv
import os
import textwrap
from io import BytesIO

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_KEY")
client = OpenAI(api_key=OPENAI_KEY)

#openai.api_key = OPENAI_KEY

import base64

def encode_image(image):
    if image.mode != "RGB":
        image = image.convert("RGB")
    
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()

# Prompt Template
PROMPT_TEMPLATE = """
You are an expert civil engineer and structural consultant. A user will upload an image of a concrete or steel structure. Based on the visual characteristics of the image, analyze the structure and provide an expert assessment of its condition.

Your response must follow this specific format:

Defect: Yes / No along with Probability of Defect in percentage.

Explain the Type of Defect: (E.g., Honeycombing, Dampness, Spalling, Exposed Reinforcement, Efflorescence, Cracking, etc.)
Observed Defects: Describe what is seen in the image that supports your diagnosis.
Possible Causes: Based on the defect type, list the likely causes.
Recommendations: What should be done immediately to address or further investigate the issue.
Repair Strategy: Detailed step-by-step repair methodology suitable for this defect.

Only give answers based on what is visible in the image. Do not speculate beyond visual evidence. Be concise but thorough. Use civil engineering terminology and best practices.
Try to write the answer covering the following points:
sections = {
        "Defect": "",
        "Type of Defect": "",
        "Observed Defects": "",
        "Possible Causes": "",
        "Recommendations": "",
        "Repair Strategy": ""
    }

Image (base64 encoded): {image_data}
"""

def analyze_image(image):
    image_data = encode_image(image)
    
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are an expert civil engineer and structural consultant."},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": PROMPT_TEMPLATE},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
                ]
            }
        ],
        max_tokens=1000
    )
    return response.choices[0].message.content

# Streamlit App
st.header("🏗️:blue[Construction Defect] Detection System")
st.subheader(":orange[Prototype for Automated Defect Analysis]", divider = True)
#st.title("🏗️Construction Defect Detection App", )
#st.markdown("Upload an image of a concrete or steel structure to detect possible defects.")

# Sidebar
st.sidebar.title("Upload Construction Image")
uploaded_file = st.sidebar.file_uploader(label = "Upload the Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.sidebar.image(img, caption="Uploaded Image")
    
    with st.spinner("Analyzing image..."):
        result = analyze_image(img)

    st.markdown("### Analysis Result")
    st.markdown(result)
    
# Footer
st.markdown("""
            <div style="text-align: center; margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #eee;">
            <p>Construction Defect Detection System - Prototype Version 1.0</p>
            </div>""", unsafe_allow_html=True)
