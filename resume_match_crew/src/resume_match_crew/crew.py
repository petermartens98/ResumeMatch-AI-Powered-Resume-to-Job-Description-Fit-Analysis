from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from pydantic import BaseModel
from typing import List


class SkillsOutput(BaseModel):
    skills_overlap_summary: str
    skills_lacking_summary: str


class EducationOutput(BaseModel):
    educational_relevance_summary: str


class ExperienceOutput(BaseModel):
    relevant_experience: List[str]
    missing_experience: List[str]
    experience_relevance_summary: str


class ResumeChangeOutput(BaseModel):
    suggestions: List[str]


@CrewBase
class ResumeMatchCrew():

    agents: List[BaseAgent]
    tasks: List[Task]

    # ----------------------------
    # Agents
    # ----------------------------

    @agent
    def skills_specialist(self) -> Agent:
        return Agent(
            role="Skills Specialist",
            goal="Provide a deep qualitative analysis of the candidate’s skill profile in relation to the job requirements.",
            backstory="""
                - An expert in talent evaluation and skill mapping, this agent goes beyond identifying matched and missing skills.
            """,
            allow_delegations=True
        )

    @agent
    def educational_specialist(self) -> Agent:
        return Agent(
            role="Educational Specialist",
            goal="Analyze candidate education and assess its relevance to job requirements",
            backstory="This agent focuses on degrees, certifications, and training to match job needs",
            allow_delegations=True
        )
    

    @agent
    def experience_specialist(self) -> Agent:
        return Agent(
            role="Experience Specialist",
            goal="Evaluate the candidate’s professional experience and determine its relevance, depth, and alignment with the job description.",
            backstory="This agent specializes in analyzing work experience, focusing on years in relevant roles, responsibilities, industries, and overall fit with the target position.",
            allow_delegations=True
        )


    @agent
    def resume_change_recommender(self) -> Agent:
        return Agent(
            role="Resume Change Recommender",
            goal="Recommend improvements to candidate resumes to better align with job requirements",
            backstory="This agent provides actionable resume suggestions based on skills, education, and experience gaps",
            allow_delegations=True
        )

    # ----------------------------
    # Tasks
    # ----------------------------

    @task
    def analyze_skills_task(self) -> Task:
        return Task(
            name="Analyze Skills",
            agent=self.skills_specialist(),
            description="Analyze candidate skills and extract a structured skills profile",
            expected_output="""
                CANDIDATE RESUME: {resume}
                JOB DESCRIPTION: {job_description}
                A Structured JSON Output with:
                    - skills_overlap_summary:
                        - Overlapping Skills: {overlapping_skills}
                        - Consider provided matching skills and expand on how the candidate overlaps with the job description. Max: 3 sentences
                    - skills_lacking_summary
                        - Lacking Skills: {lacking_skills}
                        - Consider provided lacking skills and expand on how the candidate lacks those skills with the job description. Max: 3 sentences
            """,
            output_json=SkillsOutput,
            context=[]
        )

    @task
    def analyze_education_task(self) -> Task:
        return Task(
            name="Analyze Education",
            agent=self.educational_specialist(),
            description="Analyze candidate education and assess alignment with job requirements",
            expected_output="""
            CANDIDATE RESUME: {resume}
            JOB DESCRIPTION: {job_description}
            Candidate Education: {candidate_education}
            Job Description Desired Education: {minimum_education_required}
            Return A structured report on candidate education, including:
                - educational_relevance_summary
                    - Max: 3 sentences.
            .""",
            output_json=EducationOutput,
            context=[]
        )

    @task
    def analyze_experience_task(self) -> Task:
        return Task(
            name="Analyze Experience",
            agent=self.experience_specialist(),
            description="Analyze candidate work experience and assess how well it aligns with the job requirements.",
            expected_output="""
            CANDIDATE RESUME: {resume}
            JOB DESCRIPTION: {job_description}

            Return a structured JSON report with:
                - relevant_experience: List of specific experiences directly related to the job requirements.
                - missing_experience: List of key experiences or responsibilities mentioned in the job description but not evident in the resume.
                - experience_relevance_summary: A concise summary (max 3 sentences) describing how well the candidate’s experience aligns with the role.
            """,
            output_json=ExperienceOutput,
            context=[]
        )

    @task
    def recommend_resume_changes_task(self) -> Task:
        return Task(
            name="Recommend Resume Changes",
            agent=self.resume_change_recommender(),
            description="Recommend resume changes to improve match with job description",
            expected_output="""
            CANDIDATE RESUME: {resume}
            JOB DESCRIPTION: {job_description}
            OUTPUT: A list of actionable resume improvement suggestions.
            Each suggestion should clearly indicate which skill, education, or experience gap it addresses.""",
            output_json=ResumeChangeOutput,
            context=[
                self.analyze_skills_task(),
                self.analyze_education_task(),
                self.analyze_experience_task(),
            ]
        )

    # ----------------------------
    # Crew Definition
    # ----------------------------

    @crew
    def crew(self) -> Crew:
        self.agents = [
            self.skills_specialist(),
            self.educational_specialist(),
            self.experience_specialist(),
            self.resume_change_recommender()
        ]

        self.tasks = [
            self.analyze_skills_task(),
            self.analyze_education_task(),
            self.analyze_experience_task(),
            self.recommend_resume_changes_task()
        ]

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
