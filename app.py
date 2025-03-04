import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import fitz

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini AI
genai.configure(api_key=API_KEY)

# Custom CSS (same as your current one)
st.markdown(
    """
    <style>
     .stApp {
        background-color: #121212;
        color: #ffffff;
        font-family: 'Arial', sans-serif;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 12px;
        padding: 12px 24px;
        font-size: 16px;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #45a049;
        transform: scale(1.05);
    }
    .stFileUploader>div>div>button {
        background-color: #008CBA;
        color: white;
        border-radius: 12px;
        padding: 12px 24px;
        font-size: 16px;
        border: none;
        transition: 0.3s;
    }
    .stFileUploader>div>div>button:hover {
        background-color: #007B9E;
        transform: scale(1.05);
    }
    .stTextInput>div>div>input {
        border-radius: 8px;
        padding: 10px;
        font-size: 16px;
        background-color: #1e1e1e;
        color: #ffffff;
        border: 1px solid #444;
    }
    .stMarkdown div {
        background-color: #1e1e1e;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        font-size: 16px;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #4CAF50;
    }
 
    </style>
    """,
    unsafe_allow_html=True,
)

def extract_text(file):
    """Extract text from a PDF file."""
    text = ""
    if file.name.endswith(".pdf"):
        pdf_document = fitz.open(stream=file.read(), filetype="pdf")
        for page in pdf_document:
            text += page.get_text("text")
    return text

def is_medical_report(text):
    """Check if the text is from a medical report."""
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(
        f"""
        Identify if the following text belongs to a blood test medical report.
        Reply only with 'YES' or 'NO'.

        Text:
        {text}
        """
    )
    return response.text.strip().upper() == "YES"

def analyze_report(text):
    """Analyze blood test report using Gemini AI."""
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(
        f"""
        Analyze this blood test report and provide a summary.
        Identify any abnormal values and compare them with normal ranges.
        Report:
        {text}
        """
    )
    return response.text

def ask_question(question):
    """Answer user questions about health or symptoms."""
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(
        f"""
        The patient is asking:
        "{question}"
        
        Provide a helpful response. If it's about symptoms, suggest possible illnesses.
        Disclaimer: THESE RESULTS MAY VARY, PLEASE CONSULT A DOCTOR!
        """
    )
    return response.text

# Streamlit UI
st.title("🩺 Blood Test Report Analyzer")
st.markdown("Upload your blood test report (PDF) and get an AI-powered analysis.")

uploaded_file = st.file_uploader("Upload File", type=["pdf"])

if uploaded_file is not None:
    with st.spinner("Extracting text..."):
        extracted_text = extract_text(uploaded_file)

    with st.spinner("Checking if it's a blood test report..."):
        if not is_medical_report(extracted_text):
            st.error("❌ This is not a blood test report. Please upload a valid blood test medical report.")
        else:
            with st.spinner("Analyzing report..."):
                analysis = analyze_report(extracted_text)

            st.subheader("📊 Analysis Result")
            st.markdown(
                f"<div style='background-color: #222; padding: 15px; border-radius: 8px;'>{analysis}</div>",
                unsafe_allow_html=True
            )

            # AI Health Question Section
            st.subheader("🤖 Ask AI a Health Question")
            user_question = st.text_input("Enter your question (e.g., 'What does high WBC mean?')")

            if st.button("Get AI Response 🚀"):
                if user_question:
                    with st.spinner("Processing..."):
                        ai_response = ask_question(user_question)
                    st.subheader("💡 AI's Answer:")
                    st.markdown(
                        f"<div style='background-color: #222; padding: 15px; border-radius: 8px;'>{ai_response}</div>",
                        unsafe_allow_html=True
                    )
                else:
                    st.warning("⚠️ Please enter a question before clicking the button.")

st.markdown(
    "<hr><p style='text-align: center; color: white;'>Made with ❤️ by Mehmil Zeeshan</p>",
    unsafe_allow_html=True
)

