# 🚀 AI-Powered Resume & Job Matchmaker

## 📌 Overview
This project automates resume screening using **GPT-4** and **SBERT embeddings**, comparing resumes with job descriptions to generate three scores:
1. **GPT-4 Score** → Measures structured relevance based on skills, experience, and education.
2. **SBERT Similarity Score** → Measures textual similarity between resume & job description.
3. **Final Combined Score** → The average of both scores.

✅ **Built With:** FastAPI | OpenAI GPT-4 | SBERT | Azure AI Studio | PDF/Text Processing

> ⚠️ **Project Status:** This project is currently in progress. Due to limitations on the number of requests that can be sent to Azure OpenAI in the student plan, development will continue once access to Azure premium services is available. The core functionality is implemented, but further testing and optimization are pending.

---

## 📁 Project Structure

```bash
📂 AI_Resume_Screening
│── 📂 src
│   ├── preprocess.py  # Text extraction from resumes & JDs
│   ├── match_score.py  # Computes matching scores using GPT-4 & SBERT
│   ├── app.py  # FastAPI server & endpoint for resume matching
│   └── __init__.py
│── 📂 deployment
│   └── azure_config.yaml  # Azure deployment configuration
│── 📂 models  # Model artifacts and embeddings
│── 📂 tests
│   ├── sample_resume.pdf  # Example resume for testing
│   └── job_description.txt  # Example job description
│── .env  # API keys (ignored in Git)
│── requirements.txt  # Dependencies
│── README.md  # Documentation
```

---

## 🔧 Setup & Installation
### 1️⃣ Clone Repository
```bash
git clone https://github.com/your-repo/AI_Resume_Screening.git
cd AI_Resume_Screening
```

### 2️⃣ Set Up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Set Up API Keys
Create a `.env` file in the root directory and add:
```env
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_KEY=your-azure-api-key
AZURE_OPENAI_DEPLOYMENT=gpt-4-deployment  # Use the deployment name you set
```

### 5️⃣ Run FastAPI Server
```bash
uvicorn src.app:app --reload
```
✅ **API will be available at:** `http://127.0.0.1:8000`

---

## ⚙️ API Usage
### **📌 Endpoint:** `/match`
#### **Request Format (POST)**
```json
{
  "resume_path": "tests/sample_resume.pdf",
  "job_description_path": "tests/job_description.txt"
}
```
#### **Response Format**
```json
{
  "gpt_score": 85,
  "sbert_score": 78.5,
  "final_score": 81.75
}
```

---

## 📊 Scoring Methodology
| Score Type        | Description |
|------------------|-------------|
| **GPT-4 Score** | Evaluates skills, education, & experience match (0-100) |
| **SBERT Similarity** | Textual similarity score (0-100) |
| **Final Score** | Average of both scores |

---

## 🚀 Deployment on Azure AI Studio
1️⃣ **Create an Azure AI Studio Project**
2️⃣ **Configure deployment settings in `deployment/azure_config.yaml`**
3️⃣ **Deploy FastAPI using Azure App Service**
4️⃣ **Expose the API endpoint for resume screening**

🔗 **Final API Endpoint Example:** `https://your-azure-app-url/match`

> ⚠️ **Note:** Due to limitations in the Azure OpenAI student plan, the deployment is currently restricted. The project will be fully deployed once access to Azure premium services is available.

---

## 🎯 Future Enhancements
✅ Support for multiple job descriptions 📄
✅ Improved experience handling for fresher jobs 🆕
✅ UI for job seekers & HR to upload resumes 🎨
✅ Integration with job boards and ATS systems
✅ Real-time resume analysis and feedback
✅ Custom scoring weights for different job roles

---

## 💡 Authors & Credits
Project developed by **[Your Name]** as part of an internship assessment.

📩 **Contact:** [your.email@example.com]

---

## 📜 License
This project is licensed under **MIT License**.
