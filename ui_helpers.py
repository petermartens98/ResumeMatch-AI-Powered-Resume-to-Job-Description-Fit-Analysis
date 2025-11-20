from models import EducationMatch, ExperienceMatch
from config import AppConfig

def get_education_color(match_status: EducationMatch) -> tuple:
    colors = {
        EducationMatch.exceeds: (AppConfig.COLOR_SUCCESS, "✨"),
        EducationMatch.meets: (AppConfig.COLOR_SUCCESS, "✅"),
        EducationMatch.partial: ("#fbbf24", "⚠️"),
        EducationMatch.insufficient: ("#dc3545", "❌")
    }
    return colors.get(match_status, ("#6b7280", "ℹ️"))

def get_experience_color(match_status: ExperienceMatch) -> tuple:
    colors = {
        ExperienceMatch.exceeds: (AppConfig.COLOR_SUCCESS, "✨"),
        ExperienceMatch.meets: (AppConfig.COLOR_SUCCESS, "✅"),
        ExperienceMatch.partial: ("#fbbf24", "⚠️"),
        ExperienceMatch.insufficient: ("#dc3545", "❌")
    }
    return colors.get(match_status, ("#6b7280", "ℹ️"))

def get_score_color(score: int) -> str:
    if score >= 80:
        return "#10b981"
    elif score >= 60:
        return "#fbbf24"
    elif score >= 40:
        return "#f97316"
    else:
        return "#dc3545"
    

def get_score_message(score: int) -> str:
    """Get appropriate message for match score"""
    if score >= AppConfig.SCORE_EXCELLENT:
        return 'Excellent Match! 🎉'
    elif score >= AppConfig.SCORE_GOOD:
        return 'Good Match 👍'
    elif score >= AppConfig.SCORE_MODERATE:
        return 'Moderate Match 🤔'
    else:
        return 'Needs Improvement 📚'
