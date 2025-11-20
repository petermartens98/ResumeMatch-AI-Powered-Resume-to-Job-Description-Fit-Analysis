from openai import OpenAI
from models import MatchAnalysis
from prompts import MATCH_ANALYSIS_PROMPT

client = OpenAI()

def perform_match_analysis(resume: str, job_description: str) -> MatchAnalysis | None:
    prompt = f"""
    UPLOADED RESUME:
    {resume}

    UPLOADED JOB DESCRIPTION:
    {job_description}
    """
    completion = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": MATCH_ANALYSIS_PROMPT},
            {"role": "user", "content": prompt},
        ],
        response_format=MatchAnalysis
    )
    
    message = completion.choices[0].message
    if message.parsed:
        return message.parsed
    return None