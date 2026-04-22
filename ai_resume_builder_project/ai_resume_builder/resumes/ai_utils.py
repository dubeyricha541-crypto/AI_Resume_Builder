import os

import google.generativeai as genai

_api_key = os.getenv("GEMINI_API_KEY") or ""
if _api_key:
    genai.configure(api_key=_api_key)

# Prefer current Gemini models; fall back for older projects.
_MODEL_CANDIDATES = (
    "gemini-2.0-flash",
    "gemini-1.5-flash",
    "gemini-1.5-flash-latest",
    "gemini-pro",
)


def generate_resume(prompt):
    """
    Generate AI-powered resume suggestions given a prompt string.
    Returns the generated text or an error message.
    """
    if not _api_key:
        return "Error: GEMINI_API_KEY is not set."
    last_err = None
    for model_name in _MODEL_CANDIDATES:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            text = getattr(response, "text", None) or ""
            if text.strip():
                return text
        except Exception as e:
            last_err = e
            continue
    return f"Error generating resume suggestions: {last_err or 'no response'}"


def build_improvement_prompt(career_objective, skills, experience):
    """Helper to build a structured improvement prompt."""
    return f"""
    Improve this resume professionally:

    Career Objective: {career_objective}
    Skills: {skills}
    Experience: {experience}

    Provide specific, actionable suggestions for each section.
    """


def build_ats_prompt(resume_text: str, job_description: str) -> str:
    """
    Ask the model to return strict JSON for ATS scoring + suggestions.
    """
    return f"""
You are an ATS (Applicant Tracking System) evaluator.

Return ONLY valid JSON (no markdown, no code fences) with this schema:
{{
  "score": 0-100 integer,
  "missing_keywords": ["..."],
  "suggestions": ["..."]
}}

Scoring rubric:
- Prioritize keyword alignment with job description (if provided).
- Reward clear structure, measurable impact, relevant skills, and concise bullets.
- Penalize missing contact info, vague claims, and irrelevant content.

Job Description (optional):
{job_description}

Resume Text:
{resume_text}
"""
