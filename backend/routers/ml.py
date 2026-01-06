from fastapi import APIRouter, HTTPException
from models import SkillsInput, PredictionResponse, GapAnalysisResponse, RoadmapInput, RoadmapResponse
from dependencies import get_predictor, get_knowledge_engine
from analytics_db import log_student_request

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict_role(input_data: SkillsInput):
    """
    Predict the most suitable job role based on student skills.
    
    - **skills**: List of skills the student has
    - Returns: Predicted role and confidence score
    """
    try:
        pred = get_predictor()
        role, confidence = pred.predict_role(input_data.skills)
        
        if role is None:
            raise HTTPException(status_code=400, detail="Could not predict role from provided skills")
        
        return PredictionResponse(
            predicted_role=role,
            confidence=round(confidence, 4),
            confidence_percent=f"{confidence * 100:.2f}%"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@router.post("/analyze", response_model=GapAnalysisResponse, tags=["Gap Analysis"])
async def analyze_gap(input_data: SkillsInput):
    """
    Full curriculum gap analysis pipeline.
    
    1. Predicts the most suitable job role
    2. Analyzes the skill gap for that role
    3. Provides actionable advice
    
    - **skills**: List of skills the student has
    - **department**: Optional department code to include baseline curriculum skills
    - Returns: Prediction + gap analysis with missing skills and advice
    """
    try:
        pred = get_predictor()
        ke = get_knowledge_engine()
        
        # Combine user skills with department baseline (if provided)
        combined_skills = list(input_data.skills)  # Start with user-provided skills
        
        if input_data.department:
            try:
                baseline = ke.get_baseline(input_data.department)
                # Merge without duplicates (case-insensitive)
                existing_lower = {s.lower() for s in combined_skills}
                for skill in baseline:
                    if skill.lower() not in existing_lower:
                        combined_skills.append(skill)
                        existing_lower.add(skill.lower())
            except KeyError:
                # Department not found, continue with user skills only
                pass
        
        # Step 1: Predict role using USER skills only (prioritize intent)
        role, confidence = pred.predict_role(input_data.skills)
        
        if role is None:
            raise HTTPException(status_code=400, detail="Could not predict role from provided skills")
        
        # Step 2: Analyze gap using combined skills
        gap_result = ke.analyze_gap(role, combined_skills)
        
        # Step 3: Log the request for Macro-Gap Analysis
        missing_skills = gap_result.get("missing_skills", [])
        log_student_request(role, missing_skills, input_data.student_name)
        
        return GapAnalysisResponse(
            predicted_role=role,
            confidence=round(confidence, 4),
            confidence_percent=f"{confidence * 100:.2f}%",
            target_role=gap_result.get("target_role", role),
            match_score=gap_result.get("match_score", 0),
            total_required=gap_result.get("total_required", 0),
            present_skills=gap_result.get("present_skills", []),
            missing_skills=missing_skills,
            advice=gap_result.get("advice", "No advice available.")
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")

@router.post("/roadmap", response_model=RoadmapResponse, tags=["Roadmap"])
async def generate_roadmap(input_data: RoadmapInput):
    """
    Generate a personalized learning roadmap.
    """
    try:
        ke = get_knowledge_engine()
        steps = ke.generate_roadmap(input_data.role, input_data.skills)
        
        return RoadmapResponse(
            role=input_data.role,
            steps=steps
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Roadmap generation error: {str(e)}")
