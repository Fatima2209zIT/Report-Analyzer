import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import fitz

# Load API Key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)
st.set_page_config(page_title="💡 AI Medical Assistant 🏥")
# Custom CSS for Enhanced UI
st.markdown(
    """
      <style>
        .stApp {
            background-color: #0D1117;
            color: #E6EDF3;
            font-family: 'Poppins', sans-serif;
            padding: 20px;
        }
        .stButton>button {
            background: linear-gradient(45deg, #00c6ff, #0072ff);
            color: white;
            font-size: 18px;
            font-weight: bold;
            border-radius: 12px;
            padding: 12px 24px;
            transition: 0.3s;
            border: none;
            width: 100%;
            max-width: 320px;
            margin: 10px auto;
            display: block;
            box-shadow: 0 4px 15px rgba(0, 200, 255, 0.4);
        }
        .stButton>button:hover {
            background: linear-gradient(45deg, #0072ff, #00c6ff);
            transform: scale(1.08);
            box-shadow: 0 6px 20px rgba(0, 200, 255, 0.6);
        }
        .analysis-box {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 15px;
            margin-top: 20px;
            box-shadow: 0 4px 12px rgba(255, 255, 255, 0.1);
            overflow-wrap: break-word;
        }
        .footer {
            text-align: center;
            padding: 15px;
            font-size: 14px;
            color: #888;
            margin-top: 20px;
        }
        @media screen and (max-width: 600px) {
            .stButton>button {
                font-size: 16px;
                padding: 10px 20px;
                width: 100%;
                max-width: 280px;
            }
            .analysis-box {
                padding: 10px;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar - Medical Information
st.sidebar.title("📚 Medical Reference")
st.sidebar.markdown("**Normal Ranges for Common Tests:**")
st.sidebar.markdown("- **WBC Count:** 4,000-11,000 cells/μL")
st.sidebar.markdown("- **Hemoglobin (Hb):** 12-16 g/dL")
st.sidebar.markdown("- **Platelet Count:** 150,000-450,000/μL")
st.sidebar.markdown("- **Blood Sugar (Fasting):** 70-100 mg/dL")
st.sidebar.markdown("- **Cholesterol (Total):** < 200 mg/dL")
st.sidebar.markdown("- **LDL (Bad Cholesterol):** < 100 mg/dL")
st.sidebar.markdown("- **HDL (Good Cholesterol):** > 40 mg/dL")
st.sidebar.markdown("- **Triglycerides:** < 150 mg/dL")
st.sidebar.markdown("- **Blood Pressure:** 120/80 mmHg")
st.sidebar.markdown("- **Heart Rate:** 60-100 bpm")
st.sidebar.markdown("---")
st.sidebar.markdown("**For Experts:**")
st.sidebar.markdown("- **CRP Levels:** < 10 mg/L")
st.sidebar.markdown("- **D-Dimer Test:** < 0.5 μg/mL")
st.sidebar.markdown("- **Troponin Levels:** < 0.01 ng/mL")
st.sidebar.markdown("- **Bilirubin (Total):** 0.1-1.2 mg/dL")
st.sidebar.markdown("- **ALT (Liver Enzyme):** 7-56 U/L")
st.sidebar.markdown("- **AST (Liver Enzyme):** 10-40 U/L")
st.sidebar.markdown("- **TSH (Thyroid Stimulating Hormone):** 0.4-4.0 mIU/L")
st.sidebar.markdown("- **Vitamin D:** 20-50 ng/mL")
st.sidebar.markdown("- **Vitamin B12:** 200-900 pg/mL")
st.sidebar.markdown("- **Ferritin:** 30-400 ng/mL")
st.sidebar.markdown("- **Calcium:** 8.5-10.2 mg/dL")
st.sidebar.markdown("---")
st.sidebar.markdown("📌 **Tip:** Consult your doctor if values are outside the normal range.")


# Function to Analyze Medical File
def analyze_medical_file(uploaded_file):
    model = genai.GenerativeModel("gemini-2.0-flash")
    file_data = uploaded_file.getvalue()
    file_type = uploaded_file.type

    if file_type == "application/pdf":
        with fitz.open(stream=file_data, filetype="pdf") as pdf:
            text = "".join(page.get_text() for page in pdf)
        
        prompt =         f"""
   Analyze this blood test report and provide an extraordinary, highly professional, and engaging analysis FIRST IDENTIFY THAT IF THE FILE
   IS IS RELATED TO MEDICAL TEST REPORT OR MEDICAL IMAGE. IF IT IS RELATED TO MEDICAL TEST REPORT THEN FOLLOW THE BELOW GUIDELINES AND 
   IF IT IS NOT RELATED TO MEDICAL IMAGE GIVE THE USER A MESSAGE THAT THE FILE IS NOT RELATED TO MEDICAL TEST REPORT OR MEDICAL SO I CAN'T 
   ANALYZE. :

1. 📊 Create a **beautiful, well-structured table** listing:
    - Test Name
    - Patient's Value
    - Normal Range
    - Status (⬇️ LOW / ✅ NORMAL / ⬆️ HIGH)
    - Emoji indicator

2. 🚨 Boldly **highlight all abnormal values** in red with warning emojis to grab attention.

3. 🧠 Write **detailed health risks** of each abnormal parameter with medical explanations, but make it easy to understand for a common person.

4. 👨‍⚕️ Suggest the **best doctor specialists** for each issue with reasons (e.g., "Consult a Cardiologist 🫀 because...").

5. 🥗 Recommend a **customized diet plan** with specific foods (like Spinach 🥬, Salmon 🐟) and a simple weekly routine.

6. 🚀 End the analysis with an **inspirational health quote** to motivate the patient!

Make the whole analysis super friendly, fun, colorful with emojis, and eye-catching like a professional health report designed by a top-level AI.
Report:
{text}


        """
        response = model.generate_content(prompt)
        return response.text

    elif file_type in ["image/png", "image/jpeg", "image/jpg"]:
        prompt = """

""You are an advanced medical AI assistant with specialized expertise in analyzing medical images and delivering precise, insightful medical evaluations. Your role is to:

1️⃣ Conduct a thorough and accurate analysis of the medical image with exceptional attention to detail.
2️⃣ Provide clear, structured, and professional medical observations.
3️⃣ Identify and highlight any abnormalities or areas of concern that may require further evaluation.
4️⃣ Utilize appropriate medical terminology, ensuring explanations are both scientifically accurate and easily understandable.
5️⃣ Uphold patient confidentiality and adhere to the highest standards of medical ethics.
6️⃣ Emphasize that your analysis serves as an informative guide but does not replace a professional medical diagnosis.. 
GIVE A DISCLAIMER IN THE END THAT THIS IS AI GENERATED ADVICE AND NOT A SUBSTITUTE FOR PROFESSIONAL MEDICAL CONSULTATION. 

        """
        response = model.generate_content(
            [{"text": prompt}, {"inline_data": {"mime_type": file_type, "data": file_data}}]
        )
        return response.text

    else:
        return "❌ Unsupported file type. Please upload a PDF or medical image (JPG, PNG)."

# AI-Powered Symptom Checker
def diagnose_symptoms(symptoms):
    model = genai.GenerativeModel("gemini-2.0-flash")
    prompt =  f"""
    You are a medical assistant. Based on the following symptoms, provide a detailed and structured response:
    
    **Symptoms**: {symptoms}

    **Instructions**:
    1. **Probable Diagnosis**: List the most likely conditions matching these symptoms. For each condition, provide:
       - A brief description.
       - Common causes.
       - Risk level (low, medium, high).
    2. **Severe Conditions**: Highlight any conditions that require urgent medical attention. Explain why they are urgent.
    3. **Specialists to Consult**: Recommend the appropriate medical specialists for further evaluation.
    4. **Home Remedies & Lifestyle Changes**: Suggest general home remedies and lifestyle changes to alleviate symptoms.
    5. **Disclaimer**: Always include a disclaimer that this is AI-generated advice and not a substitute for professional medical consultation.

    Format the response using clear headings, bullet points, and emojis for better readability.
    """
    response = model.generate_content(prompt)
    return response.text


# Main UI
st.title("💡 AI Medical Report & Image Analyzer 🏥")

# File Upload Section
uploaded_file = st.file_uploader("📤 Upload File", type=["pdf", "jpg", "jpeg", "png"])

if uploaded_file:
    file_type = uploaded_file.type

    # Display uploaded image
    if file_type in ["image/png", "image/jpeg", "image/jpg"]:
        st.image(uploaded_file, caption="🖼️ Uploaded Medical Image", use_container_width=True)


    if st.button("🚀 Analyze File"):
        with st.spinner("🔍 Analyzing..."):
            analysis = analyze_medical_file(uploaded_file)
        st.subheader("📝 Analysis Result")
        st.markdown(f"<div class='analysis-box'>{analysis}</div>", unsafe_allow_html=True)

# Symptom Checker UI
st.title("🩺 AI-Powered Symptom Checker")
symptoms = st.text_area("Enter your symptoms (e.g., 'fever, cough, fatigue'):")

if st.button("🔍 Get Diagnosis"):
    if symptoms:
        with st.spinner("Analyzing symptoms..."):
            diagnosis = analyze_medical_file(uploaded_file)
        st.subheader("🔍 Diagnosis")
        st.markdown(
            f"<div style='background-color: #222; padding: 15px; border-radius: 8px;'>{diagnosis}</div>",
            unsafe_allow_html=True
        )
    else:
        st.warning("⚠️ Please enter your symptoms first.")

# Footer
st.markdown("<div class='footer'>⚕️ Designed for Medical Professionals | Empowered by Cutting-Edge AI Technology<br>Created with ❤️ by Mehmil Zeeshan</div>", unsafe_allow_html=True)
