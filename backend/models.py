from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional

class SkillsInput(BaseModel):
    """Input model for skills-based queries"""
    skills: List[str] = Field(..., min_length=1, description="List of student skills")
    department: Optional[str] = Field(
        None, 
        description="Optional university department code (e.g., 'BSCS', 'BSIT') to pre-load baseline curriculum skills"
    )
    student_name: Optional[str] = Field(None, description="Name of the student for reporting")
    
    class Config:
        json_schema_extra = {
            "example": {
                "skills": ["Python", "Machine Learning", "TensorFlow", "Data Analysis"],
                "department": "BSCS"
            }
        }

class ContactRequest(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str
    turnstile_token: Optional[str] = None

class PredictionResponse(BaseModel):
    """Response model for job role prediction"""
    predicted_role: str
    confidence: float
    confidence_percent: str

class GapAnalysisResponse(BaseModel):
    """Response model for full gap analysis"""
    # Prediction
    predicted_role: str
    confidence: float
    confidence_percent: str
    # Gap Analysis
    target_role: str
    match_score: float
    total_required: int
    present_skills: List[str]
    missing_skills: List[str]
    advice: str

class RoleInfo(BaseModel):
    """Information about a supported role"""
    role: str
    required_skills: List[str]

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    model_loaded: bool
    knowledge_engine_loaded: bool

class CurriculumResponse(BaseModel):
    """Response model for curriculum baseline skills"""
    department: str
    program_name: str
    baseline_skills: List[str]

class RoadmapInput(BaseModel):
    """Input for roadmap generation"""
    role: str
    skills: List[str]

class RoadmapStep(BaseModel):
    """A single step in the learning roadmap"""
    title: str
    description: str
    duration: str
    resources: List[str]
    status: str = "pending"  # pending, in-progress, completed

class RoadmapResponse(BaseModel):
    """Response model for roadmap"""
    role: str
    steps: List[RoadmapStep]
