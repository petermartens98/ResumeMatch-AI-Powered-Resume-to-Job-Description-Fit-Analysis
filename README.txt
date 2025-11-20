# ResumeMatch

## ⚙️ Tech Stack

* **Python** (Streamlit, Pydantic, CrewAI)
* **OpenAI API** (GPT-based analysis)
* **Multi-Agent Orchestration** via CrewAI


## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/petermartens98/ResumeMatch.git
cd ResumeMatch
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
