"""
ATS score computation: AI (Gemini) when configured, plus deterministic fallbacks.
"""
import json
import re

from django.conf import settings

from .ai_utils import generate_resume, build_ats_prompt


def resume_to_plain_text(resume) -> str:
    """Flatten resume model fields into plain text for ATS analysis."""
    job_title = getattr(resume, "job_title", "") or ""
    parts = [
        resume.full_name,
        job_title,
        resume.email,
        resume.phone,
        resume.address,
        resume.career_objective,
        resume.skills,
        resume.experience,
        resume.education,
        resume.projects,
        resume.certifications,
        resume.achievements,
        resume.languages,
    ]
    return "\n".join(str(p).strip() for p in parts if p and str(p).strip())


def heuristic_ats_score(resume_text: str, job_description: str = "") -> int:
    """Rule-based score when AI is unavailable; aligns loosely with ATS heuristics."""
    rt = (resume_text or "").lower().strip()
    score = 0
    if len(rt) >= 200:
        score += 28
    elif len(rt) >= 80:
        score += 18
    elif len(rt) >= 40:
        score += 10

    if re.search(r"[\w.+-]+@[\w.-]+\.[a-z]{2,}", rt):
        score += 12
    if re.search(r"\+?\d[\d\s\-().]{7,}", rt):
        score += 8

    section_hits = sum(
        1
        for kw in (
            "experience",
            "education",
            "skill",
            "project",
            "summary",
            "objective",
            "certification",
        )
        if kw in rt
    )
    score += min(section_hits * 5, 25)

    jd = (job_description or "").lower()
    jd_words = set(re.findall(r"[a-z][a-z0-9+.#]{2,}", jd))
    jd_words = {w for w in jd_words if w not in {"the", "and", "for", "with", "you", "our", "are", "will", "this", "that"}}
    if jd_words:
        matched = sum(1 for w in jd_words if w in rt)
        ratio = matched / max(len(jd_words), 1)
        score += int(min(35, ratio * 35))

    return max(0, min(100, score))


def _parse_ai_score(raw: str) -> int | None:
    if not raw or raw.strip().startswith("Error"):
        return None
    t = raw.strip()
    if t.startswith("```"):
        t = re.sub(r"^```(?:json)?\s*", "", t, flags=re.IGNORECASE)
        t = re.sub(r"\s*```$", "", t)
    try:
        data = json.loads(t)
        return max(0, min(100, int(data.get("score", 0))))
    except (json.JSONDecodeError, TypeError, ValueError):
        return None


def compute_ats_score(resume_text: str, job_description: str = "") -> int:
    """Return 0–100 ATS compatibility score."""
    text = (resume_text or "").strip()
    jd = (job_description or "").strip()
    if len(text) < 15:
        return 0

    key = getattr(settings, "GEMINI_API_KEY", None) or ""
    if not key:
        return heuristic_ats_score(text, jd)

    prompt = build_ats_prompt(resume_text=text, job_description=jd)
    raw = generate_resume(prompt)
    parsed = _parse_ai_score(raw)
    if parsed is not None:
        return parsed
    return heuristic_ats_score(text, jd)


def refresh_resume_ats_score(resume) -> int:
    """Persist ats_score on the resume from current fields and optional job description."""
    from .models import Resume

    text = resume_to_plain_text(resume)
    jd = (resume.job_description or "").strip()
    score = compute_ats_score(text, jd)
    Resume.objects.filter(pk=resume.pk).update(ats_score=score)
    resume.ats_score = score
    return score
