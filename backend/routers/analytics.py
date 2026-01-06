from fastapi import APIRouter, HTTPException
from dependencies import get_knowledge_engine
from analytics_db import get_analytics

router = APIRouter(tags=["Admin"])

@router.get("/admin/recommendations")
async def get_admin_recommendations():
    """
    Macro-Gap Analysis: Compare Student Demand vs. Curriculum Supply.
    
    Provides AI-powered recommendations for curriculum improvement based on:
    - Student analysis trends (most requested roles, commonly missing skills)
    - Curriculum coverage (which subjects align with which roles)
    
    Returns: student_stats, curriculum_coverage, ai_recommendations
    """
    try:
        ke = get_knowledge_engine()
        
        # 1. Get Student Analytics (Demand)
        student_stats = get_analytics()
        
        # 2. Curriculum Audit (Supply) - Deep Comparison
        # First, aggregate ALL skills taught by each department
        dept_skills = {
            "BSCS": set(),
            "BSIT": set()
        }
        
        # Populate department skills
        for dept in ["BSCS", "BSIT"]:
            codes = ke.academic_baselines.get(dept, [])
            for code in codes:
                # Get skills for this subject (case insensitive normalization)
                skills = ke.course_map.get(code.upper(), [])
                for s in skills:
                    dept_skills[dept].add(s.lower())

        curriculum_coverage = {}
        
        # Helper: Check if subject is in a department
        def is_in_dept(code, dept):
            return any(c.strip().upper() == code.strip().upper() for c in ke.academic_baselines.get(dept, []))

        # Iterate through course_map for subject-level alignment (for Charts)
        # We still need this for the "Aligned Subjects" count, but we add readiness separately
        for role_name in ke.role_requirements.keys():
            # Calculate Department Specific Readiness & Gaps
            req_skills = set(s.lower() for s in ke.role_requirements[role_name])
            total_req = len(req_skills)
            
            bscs_overlap = req_skills.intersection(dept_skills["BSCS"])
            bsit_overlap = req_skills.intersection(dept_skills["BSIT"])
            
            bscs_missing = list(req_skills - bscs_overlap)
            bsit_missing = list(req_skills - bsit_overlap)
            
            curriculum_coverage[role_name] = {
                "aligned_subjects": [],
                "subject_count": 0,
                "bscs_count": 0,
                "bsit_count": 0,
                # NEW: Real Readiness & Gap Analysis
                "bscs_stats": {
                    "readiness": round((len(bscs_overlap) / total_req * 100), 1) if total_req > 0 else 0,
                    "gap": bscs_missing[0] if bscs_missing else "None",
                    "missing_count": len(bscs_missing)
                },
                "bsit_stats": {
                    "readiness": round((len(bsit_overlap) / total_req * 100), 1) if total_req > 0 else 0,
                    "gap": bsit_missing[0] if bsit_missing else "None",
                    "missing_count": len(bsit_missing)
                }
            }
        
        # Helper: Check if subject is in a department
        def is_in_dept(code, dept):
            return any(c.strip().upper() == code.strip().upper() for c in ke.academic_baselines.get(dept, []))

        # Iterate through course_map and find best matching role for each subject
        for subject_code, subject_skills in ke.course_map.items():
            if not subject_skills:
                continue
            
            # Find best matching role for this subject
            best_role = None
            best_score = 0.0
            
            for role_name, required_skills in ke.role_requirements.items():
                # Calculate match score
                if not required_skills:
                    continue
                subject_set = set(s.lower() for s in subject_skills)
                role_set = set(s.lower() for s in required_skills)
                overlap = subject_set.intersection(role_set)
                score = (len(overlap) / len(role_set)) * 100
                
                if score > best_score and score > 15:  # Minimum 15% alignment
                    best_score = score
                    best_role = role_name
            
            if best_role:
                curriculum_coverage[best_role]["aligned_subjects"].append({
                    "code": subject_code,
                    "alignment_score": round(best_score, 1)
                })
                curriculum_coverage[best_role]["subject_count"] += 1
                
                # Check Department Specific Counts
                if is_in_dept(subject_code, "BSCS"):
                    curriculum_coverage[best_role]["bscs_count"] += 1
                if is_in_dept(subject_code, "BSIT"):
                    curriculum_coverage[best_role]["bsit_count"] += 1
        
        # 3. Generate AI Recommendations
        ai_recommendations = []
        
        # Get popular roles from student stats
        popular_roles = {item["role"]: item["count"] for item in student_stats.get("top_5_roles", [])}
        
        for role_name, coverage in curriculum_coverage.items():
            subject_count = coverage["subject_count"]
            student_demand = popular_roles.get(role_name, 0)
            
            # CRITICAL: Popular role with 0 subjects
            if student_demand > 0 and subject_count == 0:
                ai_recommendations.append({
                    "type": "CRITICAL",
                    "role": role_name,
                    "message": f"'{role_name}' is in demand ({student_demand} students) but has NO aligned subjects in the curriculum!",
                    "action": f"Consider adding dedicated courses for {role_name}"
                })
            # WARNING: Popular role with < 2 subjects
            elif student_demand > 0 and subject_count < 2:
                ai_recommendations.append({
                    "type": "WARNING",
                    "role": role_name,
                    "message": f"'{role_name}' has high demand ({student_demand} students) but only {subject_count} aligned subject(s)",
                    "action": f"Consider expanding curriculum coverage for {role_name}"
                })
        
        # SKILL GAP: Skills missing for >5 students
        for skill_item in student_stats.get("top_10_missing_skills", []):
            skill = skill_item["skill"]
            count = skill_item["count"]
            if count >= 5:
                ai_recommendations.append({
                    "type": "SKILL_GAP",
                    "skill": skill,
                    "message": f"'{skill}' is missing for {count} students",
                    "action": f"Consider adding '{skill}' to relevant course syllabi"
                })
        
        return {
            "student_stats": student_stats,
            "curriculum_coverage": curriculum_coverage,
            "ai_recommendations": ai_recommendations,
            "summary": {
                "total_roles_tracked": len(ke.role_requirements),
                "total_subjects_in_curriculum": len(ke.course_map),
                "total_student_requests": student_stats.get("total_requests", 0),
                "critical_alerts": len([r for r in ai_recommendations if r["type"] == "CRITICAL"]),
                "warnings": len([r for r in ai_recommendations if r["type"] == "WARNING"]),
                "skill_gaps": len([r for r in ai_recommendations if r["type"] == "SKILL_GAP"])
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics error: {str(e)}")
