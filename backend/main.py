"""
FastAPI Backend for Curriculum Gap Analysis System
===================================================

This is the main API server that exposes the ML model and knowledge engine
for curriculum gap analysis.

Endpoints:
- POST /predict - Predict job role from skills
- POST /analyze - Full gap analysis (predict + gap)
- GET /roles - List all supported job roles
- GET /curriculum/{dept} - Get baseline skills for a department
- GET /admin/recommendations - Macro-Gap Analysis for curriculum improvement
- GET /health - Health check
- POST /contact - Send contact email via Unosend
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import sys

# Load environment variables
load_dotenv()

# Add ml_engine to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'ml_engine'))

from dependencies import get_predictor, get_knowledge_engine
from models import HealthResponse
from routers import ml, contact, analytics, curriculum

# Initialize FastAPI app
app = FastAPI(
    title="Curriculum Gap Analysis API",
    description="AI-powered job role prediction and curriculum gap analysis for students",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware (allow frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(ml.router)
app.include_router(contact.router)
app.include_router(analytics.router)
app.include_router(curriculum.router)


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Curriculum Gap Analysis API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "predict": "POST /predict",
            "analyze": "POST /analyze",
            "roles": "GET /roles",
            "curriculum": "GET /curriculum/{dept}",
            "health": "GET /health",
            "contact": "POST /contact"
        }
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Check if the API and its components are healthy"""
    try:
        pred = get_predictor()
        ke = get_knowledge_engine()
        return HealthResponse(
            status="healthy",
            model_loaded=pred is not None,
            knowledge_engine_loaded=ke is not None
        )
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service unhealthy: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
