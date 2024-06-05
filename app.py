from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
from PIL import Image
from PIL import PngImagePlugin
import io
import base64
import pdf2image
import google.generativeai as genai
import fitz  # PyMuPDF

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

# Function to convert PDF to images using PyMuPDF 
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Read the uploaded PDF file
        pdf_document = fitz.open("pdf", uploaded_file.read())
        images = []
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            images.append(img)
        return images
    else:
        raise FileNotFoundError("No File Uploaded")


#Streamlit application

st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
input_text=st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your Resume(pdf)...", type =["pdf"])

submit1 = st.button("Tell me about my Resume")
#submit2 = st.button("How Can I Improvise my Skills")
submit3 = st.button("Percentage Match")

input_prompt1 = """
You are an experienced HR With Tech Experience in the filed of Data Science, Full stack Web development, Big Data Engineering, DEVOPS, Data Analyst, your task is to review the provided resume against the job description for these profiles.
Please share your professional evaluation on whether the candidate's profile aligns with Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of Data Science, Full stack Web development, Big Data Engineering, DEVOPS, Data Analyst and deep ATS functionality, your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)

    else:
        st.write("Please upload your Resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3, pdf_content, input_text)
        print(response)
        st.subheader("The Response is")
        st.write(response)

    else:
        st.write("Please upload your Resume")

        
















