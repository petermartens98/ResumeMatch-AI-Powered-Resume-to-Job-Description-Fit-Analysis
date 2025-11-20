"""
Resume Match Pro - Improved Version
Refactored for better architecture, performance, and maintainability
"""

import streamlit as st
from config import AppConfig
from typing import Optional, List
from dataclasses import dataclass
import json
import logging
from contextlib import contextmanager
from resume_match_crew.src.resume_match_crew.crew import ResumeMatchCrew
from models import MatchAnalysis
from ui_helpers import get_education_color, get_experience_color, get_score_color, get_score_message
from analysis import perform_match_analysis

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ========================================
# Configuration & Constants
# ========================================

@dataclass
class CrewAnalysisResult:
    """Structured result from crew analysis"""
    skills_overlap_summary: Optional[str] = None
    skills_lacking_summary: Optional[str] = None
    education_relevance_summary: Optional[str] = None
    relevant_experience: Optional[List[str]] = None
    missing_experience: Optional[List[str]] = None
    experience_relevance_summary: Optional[str] = None
    domain_relevance_summary: Optional[str] = None
    resume_suggestions: Optional[List[str]] = None


# ========================================
# Utility Functions
# ========================================

@contextmanager
def error_handler(error_message: str = "An error occurred"):
    """Context manager for consistent error handling"""
    try:
        yield
    except Exception as e:
        logger.error(f"{error_message}: {str(e)}", exc_info=True)
        st.error(f"❌ {error_message}: {str(e)}")
        raise


def validate_inputs(resume_text: str, job_text: str) -> bool:
    """Validate user inputs"""
    if not resume_text.strip():
        st.warning("⚠️ Please paste your resume before starting analysis.")
        return False
    
    if not job_text.strip():
        st.warning("⚠️ Please paste the job description before starting analysis.")
        return False
    
    # Additional validation
    if len(resume_text.strip()) < 50:
        st.warning("⚠️ Resume text seems too short. Please provide a complete resume.")
        return False
    
    if len(job_text.strip()) < 30:
        st.warning("⚠️ Job description seems too short. Please provide a complete job description.")
        return False
    
    return True


# ========================================
# Crew Analysis
# ========================================

class CrewAnalyzer:
    """Handles crew analysis operations"""

    ATTRIBUTE_MAP = {
        'skills_overlap_summary': 'skills_overlap_summary',
        'skills_lacking_summary': 'skills_lacking_summary',
        'educational_relevance_summary': 'education_relevance_summary',
        'missing_experience': 'missing_experience',
        'relevant_experience': 'relevant_experience',
        'experience_relevance_summary': 'experience_relevance_summary',
        'suggestions': 'resume_suggestions'
    }
    
    @staticmethod
    def extract_crew_outputs(crew_result) -> CrewAnalysisResult:
        """Extract and parse crew analysis outputs"""
        result = CrewAnalysisResult()
        
        if not hasattr(crew_result, 'tasks_output') or not crew_result.tasks_output:
            logger.warning("No tasks output found in crew result")
            return result
        
        for task_output in crew_result.tasks_output:
            # Try pydantic object first
            if task_output.pydantic is not None:
                CrewAnalyzer._extract_from_pydantic(task_output.pydantic, result)
            # Fallback to raw JSON
            elif task_output.raw:
                CrewAnalyzer._extract_from_raw(task_output.raw, result)
        
        return result
    
    @staticmethod
    def _extract_from_pydantic(pydantic_obj, result: CrewAnalysisResult) -> None:
        """Extract data from pydantic object"""

        for attr, result_attr in CrewAnalyzer.ATTRIBUTE_MAP.items():
            if hasattr(pydantic_obj, attr):
                setattr(result, result_attr, getattr(pydantic_obj, attr))
    
    @staticmethod
    def _extract_from_raw(raw_output: str, result: CrewAnalysisResult) -> None:
        """Extract data from raw JSON output"""
        try:
            data = json.loads(raw_output)

            for key, result_attr in CrewAnalyzer.ATTRIBUTE_MAP.items():
                if key in data:
                    setattr(result, result_attr, data[key])
                    
        except json.JSONDecodeError as e:
            logger.warning(f"Could not parse task output as JSON: {str(e)}")
    
    @staticmethod
    def run_crew_analysis(resume_text: str, job_text: str, match_analysis: MatchAnalysis) -> CrewAnalysisResult:
        """Run the crew analysis with proper error handling"""
        try:
            crew = ResumeMatchCrew().crew()
            crew_result = crew.kickoff(
                inputs={
                    "resume": resume_text, 
                    "job_description": job_text,
                    "current match analysis": str(match_analysis),
                    "overlapping_skills": match_analysis.matching_skills,
                    "lacking_skills": match_analysis.missing_skills,
                    "candidate_education": match_analysis.candidate_education,
                    "minimum_education_required": match_analysis.minimum_education_required,
                    "candidate_experience": match_analysis.candidate_experience,
                    "desired_experience": match_analysis.minimum_experience_required
                }
            )
            
            return CrewAnalyzer.extract_crew_outputs(crew_result)
            
        except Exception as e:
            logger.error(f"Crew analysis failed: {str(e)}", exc_info=True)
            st.warning("⚠️ Advanced analysis partially unavailable. Showing basic results.")
            return CrewAnalysisResult()


# ========================================
# UI Components
# ========================================

class UIComponents:
    """Reusable UI component builders"""
    
    @staticmethod
    def render_hero_score(score: int) -> None:
        """Render the hero section with overall match score"""
        score_color = get_score_color(score)
        score_message = get_score_message(score)
        
        st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, {score_color}15 0%, {score_color}05 100%);
                border: 2px solid {score_color};
                border-radius: 20px;
                padding: 2rem;
                text-align: center;
                margin-bottom: 2rem;
            ">
                <h2 style="margin: 0; color: #1f2937;">Overall Match Score</h2>
                <div style="
                    font-size: 4rem;
                    font-weight: bold;
                    color: {score_color};
                    margin: 1rem 0;
                ">{score}%</div>
                <p style="margin: 0; color: #6b7280; font-size: 1.1rem;">
                    {score_message}
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_metric_card(title: str, value: str, subtitle: str, gradient: str) -> str:
        """Generate HTML for a metric card"""
        return f"""
            <div style="
                background: linear-gradient(135deg, {gradient});
                border-radius: 15px;
                padding: 1.5rem;
                text-align: center;
                color: white;
            ">
                <div style="font-size: 0.9rem; opacity: 0.9;">{title}</div>
                <div style="font-size: 2.5rem; font-weight: bold; margin: 0.5rem 0;">
                    {value}
                </div>
                <div style="font-size: 0.85rem; opacity: 0.8;">
                    {subtitle}
                </div>
            </div>
        """
    
    @staticmethod
    def render_skill_box(title: str, skills: List[str], summary: Optional[str], 
                        color: str, icon: str, border_color: str) -> None:
        """Render a skill box with skills and summary"""
        if skills:
            bubbles = ''.join([
                f'<span style="background-color: {color}; color: white; '
                f'padding: 10px 18px; border-radius: 25px; font-size: 0.95rem; '
                f'white-space: nowrap; font-weight: 500; '
                f'box-shadow: 0 2px 4px rgba(0,0,0,0.1);">{icon} {skill}</span>'
                for skill in skills
            ])
        else:
            bubbles = '<i style="color: #6b7280;">No skills in this category</i>'
        
        summary_text = summary if summary else "No additional analysis available."
        
        html = f"""
        <div style="
            background: linear-gradient(135deg, {color}20 0%, {color}10 100%);
            padding: 1.5rem;
            border-radius: 15px;
            border: 2px solid {border_color};
            margin-bottom: 1rem;
        ">
            <h3 style="margin-top: 0; color: {border_color};">{title}</h3>
            <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 10px;">
                {bubbles}
            </div>
            <p style="margin-top: 10px; color: {border_color}; line-height: 1.6;">
                {summary_text}
            </p>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)
    
    @staticmethod
    def render_suggestions(suggestions: List[str]) -> None:
        """Render resume improvement suggestions"""
        if not suggestions:
            return
        
        st.markdown("## 📝 Recommended Resume Changes")
        
        for i, suggestion in enumerate(suggestions, 1):
            st.markdown(f"""
                <div style="
                    background: white;
                    border-left: 4px solid {AppConfig.COLOR_PRIMARY};
                    border-radius: 8px;
                    padding: 1rem;
                    margin-bottom: 1rem;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                ">
                    <div style="color: #374151; line-height: 1.6;">
                        <strong style="color: {AppConfig.COLOR_PRIMARY};">#{i}</strong> {suggestion}
                    </div>
                </div>
            """, unsafe_allow_html=True)


class AnalysisDisplay:
    """Handles the display of analysis results"""
    
    @staticmethod
    def display_skills_analysis(analysis: MatchAnalysis, crew_result: CrewAnalysisResult) -> None:
        """Display comprehensive skills analysis"""
        st.markdown("## 📊 Skills Analysis")
        
        # Calculate metrics
        total_skills = len(analysis.matching_skills) + len(analysis.missing_skills)
        skill_match_percentage = (
            (len(analysis.matching_skills) / total_skills) * 100
            if total_skills > 0 else 0
        )
        
        # Metric cards
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(UIComponents.render_metric_card(
                "Skill Match Rate",
                f"{skill_match_percentage:.0f}%",
                f"{len(analysis.matching_skills)}/{total_skills} skills",
                f"{AppConfig.COLOR_PRIMARY} 0%, {AppConfig.COLOR_SECONDARY} 100%"
            ), unsafe_allow_html=True)
        
        with col2:
            st.markdown(UIComponents.render_metric_card(
                "Matching Skills",
                str(len(analysis.matching_skills)),
                "✓ Found in resume",
                f"{AppConfig.COLOR_SUCCESS} 0%, #059669 100%"
            ), unsafe_allow_html=True)
        
        with col3:
            st.markdown(UIComponents.render_metric_card(
                "Skills to Develop",
                str(len(analysis.missing_skills)),
                "⚡ Growth areas",
                f"{AppConfig.COLOR_WARNING} 0%, #dc2626 100%"
            ), unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Skill details
        col_left, col_right = st.columns(2)
        
        with col_left:
            UIComponents.render_skill_box(
                "✅ Matching Skills",
                analysis.matching_skills,
                crew_result.skills_overlap_summary,
                AppConfig.COLOR_SUCCESS,
                "✓",
                AppConfig.COLOR_SUCCESS
            )
        
        with col_right:
            UIComponents.render_skill_box(
                "📚 Skills to Develop",
                analysis.missing_skills,
                crew_result.skills_lacking_summary,
                AppConfig.COLOR_WARNING,
                "!",
                AppConfig.COLOR_WARNING
            )
    
    @staticmethod
    def display_education_analysis(analysis: MatchAnalysis, crew_result: CrewAnalysisResult) -> None:
        """Display education analysis section"""
        st.markdown("## 🎓 Education Analysis")
        
        edu_color, edu_icon = get_education_color(analysis.education_match)
        summary = crew_result.education_relevance_summary or "No detailed analysis available."
        
        edu_html = f"""
        <div style="background: linear-gradient(135deg, rgba(16,185,129,0.1) 0%, rgba(16,185,129,0.05) 100%);
                    border-left: 5px solid {edu_color};
                    border-radius: 10px;
                    padding: 1.5rem;
                    margin-bottom: 1.5rem;">
            <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                <span style="font-size: 2rem; margin-right: 1rem;">{edu_icon}</span>
                <h3 style="margin: 0; color: {edu_color};">Education Match: {analysis.education_match.value}</h3>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;">
                <div style="background: white; padding: 1rem; border-radius: 8px; border: 1px solid #e5e7eb;">
                    <div style="font-size: 0.85rem; color: #6b7280; margin-bottom: 0.5rem;">📋 Required Education</div>
                    <div style="font-weight: 600; color: #1f2937;">{analysis.minimum_education_required}</div>
                </div>
                <div style="background: white; padding: 1rem; border-radius: 8px; border: 1px solid #e5e7eb;">
                    <div style="font-size: 0.85rem; color: #6b7280; margin-bottom: 0.5rem;">🎓 Your Education</div>
                    <div style="font-weight: 600; color: #1f2937;">{analysis.candidate_education}</div>
                </div>
            </div>
            <div style="margin-top: 1rem;">
                <div style="background: white; border-radius: 8px; padding: 1rem; border: 1px solid #e5e7eb;">
                    <div style="font-size: 0.85rem; color: #6b7280; margin-bottom: 0.5rem; font-weight: 500;">
                        🎓 Education Relevance
                    </div>
                    <p style="margin: 0; color: {edu_color}; line-height: 1.6;">{summary}</p>
                </div>
            </div>
        </div>
        """
        st.markdown(edu_html, unsafe_allow_html=True)
    

    @staticmethod
    def display_experience_analysis(analysis: MatchAnalysis, crew_result: CrewAnalysisResult) -> None:
        """Display experience analysis section with relevant and missing experience lists side by side"""
        st.markdown("## 💼 Experience Analysis")
        
        exp_color, exp_icon = get_experience_color(analysis.experience_match)
        
        # Get experience data
        missing_experience = crew_result.missing_experience
        relevant_experience = crew_result.relevant_experience
        exp_summary = crew_result.experience_relevance_summary or "No detailed analysis available."
        
        # Convert to lists if needed
        missing_experience = missing_experience or []
        missing_experience = missing_experience if isinstance(missing_experience, list) else [missing_experience]

        relevant_experience = relevant_experience or []
        relevant_experience = relevant_experience if isinstance(relevant_experience, list) else [relevant_experience]

        
        # Display header with match status
        exp_match_html =  f'''
            <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                <span style="font-size: 2rem; margin-right: 1rem;">{exp_icon}</span>
                <h3 style="margin: 0; color: {exp_color};">Education Match: {analysis.experience_match.value}</h3>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;">
                <div style="background: white; padding: 1rem; border-radius: 8px; border: 1px solid #e5e7eb;">
                    <div style="font-size: 0.85rem; color: #6b7280; margin-bottom: 0.5rem;">💼 Your Experience</div>
                    <div style="font-weight: 600; color: #1f2937;">{analysis.candidate_experience}</div>
                </div>
                <div style="background: white; padding: 1rem; border-radius: 8px; border: 1px solid #e5e7eb;">
                    <div style="font-size: 0.85rem; color: #6b7280; margin-bottom: 0.5rem;">📋 Required Experience</div>
                    <div style="font-weight: 600; color: #1f2937;">{analysis.minimum_experience_required}</div>
                </div>
            </div>
        '''
        st.markdown(exp_match_html, unsafe_allow_html=True)
        

        # Display summary
        st.markdown("### ⏱️ Overlap Summary")
        st.info(exp_summary)
        
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown("#### ✅ Relevant Experience")
            if relevant_experience and len(relevant_experience) > 0:
                for item in relevant_experience:
                    st.success(f"✓ {item}")
            else:
                st.caption("_No relevant experience identified_")
        
        with col_right:
            st.markdown("#### ❌ Missing Experience")
            if missing_experience and len(missing_experience) > 0:
                for item in missing_experience:
                    st.error(f"✗ {item}")
            else:
                st.caption("_No missing experience identified_")

    @staticmethod
    def display_complete_analysis(analysis: MatchAnalysis, crew_result: CrewAnalysisResult) -> None:
        """Display the complete analysis with all sections"""
        UIComponents.render_hero_score(analysis.overall_match_score)
        AnalysisDisplay.display_skills_analysis(analysis, crew_result)
        AnalysisDisplay.display_education_analysis(analysis, crew_result)
        AnalysisDisplay.display_experience_analysis(analysis, crew_result)
        UIComponents.render_suggestions(crew_result.resume_suggestions or [])


# ========================================
# Page Setup
# ========================================

def setup_page_config() -> None:
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title=AppConfig.PAGE_TITLE,
        layout=AppConfig.LAYOUT,
        initial_sidebar_state="collapsed",
        page_icon=AppConfig.PAGE_ICON
    )


def inject_custom_css() -> None:
    """Inject custom CSS styles"""
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        * {
            font-family: 'Inter', sans-serif;
        }
        
        .main-header {
            text-align: center;
            padding: 2rem 1rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 20px;
            margin-bottom: 2.5rem;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        }
        
        .main-header h1 {
            margin: 0;
            font-size: 2.5rem;
            font-weight: 700;
        }
        
        .main-header p {
            margin: 0.5rem 0 0 0;
            font-size: 1.1rem;
            opacity: 0.95;
        }
        
        .stButton>button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-weight: 600;
            border: none;
            padding: 0.9rem 3rem;
            border-radius: 30px;
            font-size: 1.1rem;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
            transform: translateY(-2px);
        }
        
        .stTextArea textarea {
            border-radius: 15px;
            border: 2px solid #e5e7eb;
            padding: 1rem;
            font-size: 0.95rem;
            transition: border-color 0.3s ease;
        }
        
        .stTextArea textarea:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        h1, h2, h3 {
            color: #1f2937;
        }
        
        .input-section-header {
            background: linear-gradient(135deg, #f3f4f6 0%, #ffffff 100%);
            padding: 1rem 1.5rem;
            border-radius: 12px;
            margin-bottom: 1rem;
            border-left: 4px solid #667eea;
            font-weight: 600;
            color: #374151;
            font-size: 1.1rem;
        }
        </style>
    """, unsafe_allow_html=True)


def render_header() -> None:
    """Render the application header"""
    st.markdown('''
        <div class="main-header">
            <h1>📊 Resume Match Pro</h1>
            <p>AI-powered resume analysis with comprehensive education matching</p>
        </div>
    ''', unsafe_allow_html=True)


def render_input_section() -> tuple[str, str]:
    """Render input section and return resume and job text"""
    left_col, right_col = st.columns(2, gap="large")
    
    with left_col:
        st.markdown('<div class="input-section-header">📄 Your Resume</div>', 
                   unsafe_allow_html=True)
        resume_text = st.text_area(
            "Paste your resume here:",
            height=AppConfig.TEXTAREA_HEIGHT,
            placeholder="Copy and paste your complete resume here...\n\n"
                       "• Include your education background\n"
                       "• List your skills and experience\n"
                       "• Add relevant certifications",
            label_visibility="collapsed",
            key="resume_input"
        )

    with right_col:
        st.markdown('<div class="input-section-header">💼 Job Description</div>', 
                   unsafe_allow_html=True)
        job_text = st.text_area(
            "Paste the job description here:",
            height=AppConfig.TEXTAREA_HEIGHT,
            placeholder="Copy and paste the job description here...\n\n"
                       "• Include required skills\n"
                       "• Mention education requirements\n"
                       "• Add preferred qualifications",
            label_visibility="collapsed",
            key="job_input"
        )
    
    return resume_text, job_text


# ========================================
# Main Application
# ========================================

def run_analysis_pipeline(resume_text: str, job_text: str) -> None:
    """Execute the complete analysis pipeline"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    # Step 1: Initial analysis
    with col2:
        with st.spinner("🔍 Analyzing Resume and Job Description..."):
            match_analysis = perform_match_analysis(resume_text, job_text)
    
    if not match_analysis:
        st.error("❌ Analysis failed. Please try again or check your inputs.")
        return
    
    # Step 2: Crew analysis
    with col2:
        with st.spinner("🤖 Running Advanced AI Analysis..."):
            crew_result = CrewAnalyzer.run_crew_analysis(
                resume_text, 
                job_text, 
                match_analysis
            )
    
    # Step 3: Display results
    AnalysisDisplay.display_complete_analysis(match_analysis, crew_result)


def main():
    """Main application entry point"""
    # Setup
    setup_page_config()
    inject_custom_css()
    
    # Render UI
    render_header()
    resume_text, job_text = render_input_section()
    
    # Analysis button
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        analyze_btn = st.button("🚀 Analyze Match", use_container_width=True)
    
    # Execute analysis
    if analyze_btn:
        if validate_inputs(resume_text, job_text):
            with error_handler("Analysis failed"):
                run_analysis_pipeline(resume_text, job_text)


if __name__ == "__main__":
    main()