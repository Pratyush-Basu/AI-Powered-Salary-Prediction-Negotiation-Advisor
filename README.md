
# 💼 AI-Powered Salary Prediction & Negotiation Advisor

An intelligent web-based platform that predicts your salary based on your profile and provides **personalized salary negotiation strategies** using Google Gemini AI. Upload your resume in PDF format and get powerful, resume-based tips to boost your offer.

---

## 🚀 Features

- 🧠 **AI Salary Prediction** based on Gender, Education, Experience, and Job Role
- 🤖 **Smart Negotiation Advice** from Google Gemini AI
- 📄 **PDF Resume Analysis** to extract negotiation points
- 🌐 **Frontend** built using HTML, CSS, Bootstrap & JS
- 📊 **Salary Model** trained and saved using `scikit-learn` and `joblib`

---

## 🖼️ Demo Screenshots

| Home Page | Result Page |
|-----------|-------------|
| ![Home](screenshots/home.png) | ![Result](screenshots/result.png) |

---

## 🛠️ Tech Stack

**Frontend:**
- HTML5, CSS3
- Bootstrap 5
- JavaScript

**Backend:**
- Flask (Python)
- scikit-learn (salary prediction model)
- PyMuPDF (`fitz`) for PDF resume text extraction
- Google Gemini (Generative AI for negotiation tips)

---

## 📂 Project Structure

├── templates/
│ ├── index.html
│ └── result.html
├── salary_model _final.pkl
├── app.py
├── requirements.txt
└── README.md



---

## 📦 Installation

### 1. Clone the repository


git clone https://github.com/Pratyush-Basu/AI-Powered-Salary-Prediction-Negotiation-Advisor.git
cd ai-salary-negotiation
2. Install dependencies

pip install -r requirements.txt
3. Add your Gemini API Key
Replace the placeholder in app.py:

python
Copy
Edit
genai.configure(api_key="YOUR_GEMINI_API_KEY")
4. Run the app
bash
Copy
Edit
python app.py
Visit: http://localhost:5000

📥 Upload Format for Resume
Only PDF files supported

Resume must be under 3,000 characters for optimal AI analysis

🧪 Model Details
salary_model _final.pkl is a pre-trained regression model

Encodes:

Gender (Male, Female, Other)

Education (High School, Bachelor's, Master's, PhD)

Experience (years)

Job Category (mapped numerically)

🔐 Security Note
Do not expose your Gemini API key in public repositories. Use environment variables or secret managers for production deployments.

✨ Future Enhancements
Save results to user profile

Add support for DOCX resumes

Use Gemini Pro for deeper resume insights

Real-time salary comparison graphs

🤝 Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss.

📃 License
MIT

📫 Contact
Developer: Pratyush Basu
📧 Email: basupratyush76@gmail.com
🌐 GitHub: @Pratyush-Basu





Let me know if you'd like a `requirements.txt` file, example resume, or `index.html` + `result.html` templates
