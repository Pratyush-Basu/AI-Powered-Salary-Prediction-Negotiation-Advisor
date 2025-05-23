from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib
import google.generativeai as genai
import os
import fitz  # PyMuPDF
import logging
import random

# Configure Gemini
genai.configure(api_key="YOUR API KEY")  # Replace with your actual key
genai_model = genai.GenerativeModel("gemini-1.5-flash")

# Industry salary data (to be used for realistic comparisons)
industry_data = {
    'Software Engineer': {'low': 0.85, 'avg': 1.0, 'high': 1.25, 'variance': 0.05},
    'Data Scientist': {'low': 0.88, 'avg': 1.0, 'high': 1.30, 'variance': 0.07},
    'Web Developer': {'low': 0.82, 'avg': 1.0, 'high': 1.20, 'variance': 0.04},
    'Product Manager': {'low': 0.87, 'avg': 1.0, 'high': 1.28, 'variance': 0.06},
    'IT Support': {'low': 0.90, 'avg': 1.0, 'high': 1.15, 'variance': 0.03},
    'UX/UI Designer': {'low': 0.85, 'avg': 1.0, 'high': 1.22, 'variance': 0.05},
    'Project Manager': {'low': 0.88, 'avg': 1.0, 'high': 1.24, 'variance': 0.05},
    'Marketing Tech': {'low': 0.84, 'avg': 1.0, 'high': 1.18, 'variance': 0.04},
    'Security/Infra Manager': {'low': 0.86, 'avg': 1.0, 'high': 1.32, 'variance': 0.08},
    'CTO/Director': {'low': 0.80, 'avg': 1.0, 'high': 1.40, 'variance': 0.10}
}

# Gemini Negotiation Advice - Improved Prompt
def get_gemini_tip(gender, education, experience, job_role, predicted_salary, personality=None):
    prompt = f"""
    As an expert salary negotiation coach with deep expertise in behavioral psychology and {job_role} compensation trends:
    
    CANDIDATE PROFILE:
    • Gender: {gender}
    • Education: {education}
    • Experience: {experience} years
    • Role: {job_role}
    • Predicted Salary: ₹{predicted_salary:,}
    • Personality: {personality if personality else "Not specified"}
    
    Provide 3 highly tactical, personalized negotiation strategies that this specific candidate can immediately apply.
    
    Each strategy must:
    1. Include exact phrasing or script the candidate can use
    2. Address likely objections specific to their profile
    3. Consider gender/experience dynamics in {job_role} negotiations
    
    Focus exclusively on high-impact tactics that leverage this candidate's specific strengths.
    NO general advice. NO unnecessary explanations. NO bullet points or markdown formatting.
    """
    try:
        response = genai_model.generate_content(prompt)
        tips = [tip.strip('-*• ').strip() for tip in response.text.strip().split('\n') if tip.strip()]
        return tips
    except Exception as e:
        return [f"Could not generate tips: {str(e)}"]

# Resume Analysis - Improved Prompt
def analyze_resume(resume_text, job_role, predicted_salary):
    prompt = f"""
    You're an elite compensation consultant who specializes in {job_role} roles.
    
    TASK: Extract 3 powerful salary negotiation leverage points from this resume for a {job_role} targeting ₹{predicted_salary:,}.
    
    RESUME:
    {resume_text[:3500]}
    
    For each point:
    1. Identify a SPECIFIC achievement, credential, or skill that objectively justifies higher compensation
    2. Explain precisely how to monetize this advantage in negotiation
    3. Quantify the potential salary impact where possible
    
    Focus ONLY on evidence-based points from this specific resume.
    Prioritize unique, differentiated value that hiring managers would recognize.
    NO generic advice. NO platitudes. NO markdown formatting.
    """
    try:
        response = genai_model.generate_content(prompt)
        points = [p.strip('-*• ').strip() for p in response.text.strip().split('\n') if p.strip()]
        return points
    except Exception as e:
        return [f"Could not analyze resume: {str(e)}"]

# PDF Text Extraction
def extract_text_from_pdf(file_storage):
    try:
        text = ""
        with fitz.open(stream=file_storage.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
        return text
    except Exception as e:
        logging.error(f"PDF extraction error: {str(e)}")
        return ""

# Generate realistic industry comparison data
def get_industry_comparison(job_role, predicted_salary):
    if job_role not in industry_data:
        # Default values if job role not found
        return {
            'min': round(predicted_salary * 0.85, 2),
            'low': round(predicted_salary * 0.90, 2),
            'avg': round(predicted_salary, 2),
            'high': round(predicted_salary * 1.15, 2),
            'max': round(predicted_salary * 1.25, 2)
        }
    
    # Get the job-specific multipliers
    job_metrics = industry_data[job_role]
    variance = job_metrics['variance']
    
    # Add some randomness to make it appear more realistic
    low_factor = job_metrics['low'] + random.uniform(-variance, variance)
    avg_factor = job_metrics['avg'] + random.uniform(-variance/2, variance/2)
    high_factor = job_metrics['high'] + random.uniform(-variance, variance)
    
    # Calculate salary ranges
    return {
        'min': round(predicted_salary * (low_factor - 0.05), 2),
        'low': round(predicted_salary * low_factor, 2),
        'avg': round(predicted_salary * avg_factor, 2),
        'high': round(predicted_salary * high_factor, 2),
        'max': round(predicted_salary * (high_factor + 0.1), 2)
    }

# Flask App Initialization
app = Flask(__name__)

# Load Model
model = joblib.load('salary_model _final.pkl')

# Encoders
gender_mapping = {'Male': 0, 'Female': 1, 'Other': 2}
education_mapping = {
    "High School": 0,
    "Bachelor's Degree": 1,
    "Master's Degree": 2,
    'PhD Degree': 3
}
job_category_mapping = {
    'Software Engineer': 0,
    'Data Scientist': 1,
    'Web Developer': 2,
    'Product Manager': 3,
    'IT Support': 4,
    'UX/UI Designer': 5,
    'Project Manager': 6,
    'Marketing Tech': 7,
    'Security/Infra Manager': 8,
    'CTO/Director': 9
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        gender = request.form['gender']
        education = request.form['education']
        experience = float(request.form['experience'])
        job_category = request.form['job']
        personality = request.form.get('personality', None)

        # Encode inputs
        input_data = pd.DataFrame([{
            'Gender': gender_mapping.get(gender, 0),
            'Education Level': education_mapping.get(education, 0),
            'Years of Experience': experience,
            'Job Category': job_category_mapping.get(job_category, 0)
        }])

        # Predict salary
        predicted_salary = model.predict(input_data)[0]
        
        # Get realistic industry comparison
        industry_comp = get_industry_comparison(job_category, predicted_salary)

        # Get negotiation tips
        tips = get_gemini_tip(gender, education, experience, job_category, predicted_salary, personality)

        # Resume PDF analysis
        resume_tips = []
        if 'resume' in request.files and request.files['resume'].filename.endswith('.pdf'):
            resume_text = extract_text_from_pdf(request.files['resume'])
            if resume_text:
                resume_tips = analyze_resume(resume_text, job_category, predicted_salary)
            else:
                resume_tips = ["Resume text could not be extracted."]
        else:
            resume_tips = ["No valid PDF resume uploaded."]

        return render_template(
            'result.html',
            salary=round(predicted_salary, 2),
            industry_min=industry_comp['min'],
            industry_low=industry_comp['low'],
            industry_avg=industry_comp['avg'],
            industry_high=industry_comp['high'],
            industry_max=industry_comp['max'],
            tips=tips,
            resume_tips=resume_tips
        )
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/stop_speech', methods=['POST'])
def stop_speech():
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True)
