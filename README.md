# ResumeMatch: AI-Powered Resume-to-Job-Description Fit Analysis
ResumeMatch is an AI-powered resume analysis tool designed to drastically improve a candidate's chances of landing a job interview by calculating the fit between a resume and a specific job description.

## 🛠️ Key Functionality
The application uses an advanced multi-agent orchestration framework (CrewAI) combined with the analytical power of OpenAI's GPT models to provide a comprehensive, data-driven match analysis.
- Holistic Score Calculation: Generates a single, easy-to-understand overall match score for the candidate.
- Skills Gap Analysis: Identifies matching skills and crucial missing skills that should be addressed in the resume.
- Education and Experience Evaluation: Provides a detailed breakdown of how the candidate's educational and professional history meets, partially meets, or exceeds the job requirements.
- Actionable Suggestions: Offers concrete, step-by-step suggestions on how to revise the resume to maximize relevance and score higher against the target job description.

## ⚙️ Tech Stack

* **Python** (Streamlit, Pydantic, CrewAI)
* **OpenAI API** (GPT-based analysis)
* **Multi-Agent Orchestration** via CrewAI

## 📸 Screenshots
<img width="1586" height="1188" alt="image" src="https://github.com/user-attachments/assets/57f8867e-eea4-41b2-a488-b62326219c4d" />
<img width="1569" height="1035" alt="image" src="https://github.com/user-attachments/assets/480abf8a-e6f4-4b31-b779-dbd3bef20217" />
<img width="1582" height="496" alt="image" src="https://github.com/user-attachments/assets/c58d2f3d-21a6-436d-a607-b20a239c22ae" />
<img width="1566" height="1182" alt="image" src="https://github.com/user-attachments/assets/8f561e7d-dbfc-4147-a067-154d09dc785d" />
<img width="1595" height="1235" alt="image" src="https://github.com/user-attachments/assets/4a449d44-75ae-4ff0-9373-c9525fab526a" />


## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/petermartens98/ResumeMatch-AI-Powered-Resume-to-Job-Description-Fit-Analysis
cd ResumeMatch-AI-Powered-Resume-to-Job-Description-Fit-Analysis
```

### 2. Create and activate a virtual environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install CrewAI (agent orchestration framework)

```bash
uv tool install crewai
```

### 5. Set your OpenAI API key

Create a file at `.streamlit/secrets.toml` and add:

```toml
OPENAI_API_KEY = "your-openai-api-key"
```

### 6. Configure the model and API key

In `resume_match_crew/.env`, open the configuration file and set your preferred **MODEL** (e.g. `gpt-4.5`) and **OPENAI_API_KEY**.

### 7. Launch the app

```bash
streamlit run streamlit_app.py
```

---

## 🧑‍💻 Author

**Peter Martens**
🔗 [GitHub](https://github.com/petermartens98) • [LinkedIn](https://www.linkedin.com/in/petermartens5498)
