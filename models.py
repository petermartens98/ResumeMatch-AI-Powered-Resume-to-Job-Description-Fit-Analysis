from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class EducationMatch(str, Enum):
    exceeds = "Exceeds"
    meets = "Meets"
    partial = "Partial"
    insufficient = "Insufficient"

class ExperienceMatch(str, Enum):
    exceeds = "Exceeds"
    meets = "Meets"
    partial = "Partial"
    insufficient = "Insufficient"

class MatchAnalysis(BaseModel):
    matching_skills: List[str]
    missing_skills: List[str]
    minimum_education_required: str
    candidate_education: str
    education_match: EducationMatch
    minimum_experience_required: str
    candidate_experience: str
    experience_match: ExperienceMatch
    experience_gap_explanation: Optional[str] = None
    overall_match_score: int
    recommendations: List[str]