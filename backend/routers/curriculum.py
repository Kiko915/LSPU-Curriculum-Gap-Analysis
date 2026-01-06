from fastapi import APIRouter, HTTPException
from typing import List
from models import RoleInfo, CurriculumResponse
from dependencies import get_knowledge_engine

router = APIRouter()

@router.get("/roles", response_model=List[RoleInfo], tags=["Roles"])
async def list_roles():
    """
    List all supported job roles and their required skills.
    
    Useful for understanding what roles the system can predict.
    """
    try:
        ke = get_knowledge_engine()
        roles = []
        for role_name, skills in ke.role_requirements.items():
            roles.append(RoleInfo(
                role=role_name,
                required_skills=sorted(list(skills))
            ))
        return sorted(roles, key=lambda x: x.role)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching roles: {str(e)}")


@router.get("/roles/{role_name}", response_model=RoleInfo, tags=["Roles"])
async def get_role(role_name: str):
    """
    Get details about a specific role.
    
    - **role_name**: Name of the job role (case-insensitive)
    """
    try:
        ke = get_knowledge_engine()
        role_input = role_name.lower().strip()
        
        # Case-insensitive lookup: find the key that matches
        matched_role = None
        for key in ke.role_requirements.keys():
            if key.lower() == role_input:
                matched_role = key
                break
        
        if matched_role is None:
            available_roles = list(ke.role_requirements.keys())
            raise HTTPException(
                status_code=404, 
                detail=f"Role '{role_name}' not found. Available: {available_roles}"
            )
        
        return RoleInfo(
            role=matched_role,
            required_skills=sorted(list(ke.role_requirements[matched_role]))
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get("/curriculum/{dept}", response_model=CurriculumResponse, tags=["Curriculum"])
async def get_curriculum(dept: str):
    """
    Get the baseline curriculum skills for a university department.
    
    - **dept**: Department code (e.g., 'BSCS', 'BSIT')
    - Returns: List of baseline skills for that program
    """
    try:
        ke = get_knowledge_engine()
        dept_upper = dept.upper().strip()
        
        try:
            baseline_skills = ke.get_baseline(dept_upper)
        except KeyError:
            raise HTTPException(
                status_code=404, 
                detail=f"Department '{dept}' not found. Available: {list(ke.academic_baselines.keys())}"
            )
        
        # Get program name if available
        program_names = {
            "BSCS": "Bachelor of Science in Computer Science",
            "BSIT": "Bachelor of Science in Information Technology",
            "BSIS": "Bachelor of Science in Information Systems",
            "BSCE": "Bachelor of Science in Computer Engineering",
            "BSECE": "Bachelor of Science in Electronics and Communications Engineering"
        }
        
        return CurriculumResponse(
            department=dept_upper,
            program_name=program_names.get(dept_upper, f"{dept_upper} Program"),
            baseline_skills=baseline_skills
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching curriculum: {str(e)}")
