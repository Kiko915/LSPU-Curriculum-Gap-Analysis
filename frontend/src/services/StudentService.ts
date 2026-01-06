import type { Curriculum, GapAnalysis, RoadmapStep } from "../types/student";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

// Interface for Backend API Response
interface GapAnalysisAPIResponse {
    predicted_role: string;
    confidence: number;
    confidence_percent: string;
    target_role: string;
    match_score: number;
    total_required: number;
    present_skills: string[];
    missing_skills: string[];
    advice: string;
}

// Mock data
const mockCurriculums: Record<string, Curriculum> = {
    BSCS: {
        dept: "BSCS",
        totalUnits: 148,
        description: "Bachelor of Science in Computer Science - Focus on Algorithms and AI"
    },
    BSIT: {
        dept: "BSIT",
        totalUnits: 151,
        description: "Bachelor of Science in Information Technology - Focus on Web and Networking"
    }
};

const mockRoadmaps: Record<string, RoadmapStep[]> = {
    "Data Scientist": [
        {
            title: "Phase 1: Advanced Python & Math",
            description: "Master libraries like NumPy, Pandas and refresh Linear Algebra.",
            duration: "2-3 Weeks",
            resources: ["Coursera: Math for ML", "Kaggle Python Course"]
        },
        {
            title: "Phase 2: Deep Learning Frameworks",
            description: "Build projects using TensorFlow and PyTorch.",
            duration: "4 Weeks",
            resources: ["DeepLearning.ai", "Fast.ai"]
        },
        {
            title: "Phase 3: Big Data Tools",
            description: "Learn Spark and SQL for large scale data processing.",
            duration: "3 Weeks",
            resources: ["Databricks Community Edition"]
        }
    ],
    "Full Stack Developer": [
        {
            title: "Phase 1: Containerization",
            description: "Learn Docker and how to containerize applications.",
            duration: "2 Weeks",
            resources: ["Docker documentation", "Nana's DevOps Bootcamp"]
        },
        {
            title: "Phase 2: Orchestration",
            description: "Understand Kubernetes basics and cluster management.",
            duration: "3 Weeks",
            resources: ["Kubernetes.io", "Minikube"]
        },
        {
            title: "Phase 3: CI/CD Pipelines",
            description: "Automate testing and deployment with GitHub Actions.",
            duration: "2 Weeks",
            resources: ["GitHub Actions Docs"]
        }
    ]
};

export const StudentService = {
    getCurriculum: async (dept: string): Promise<Curriculum> => {
        // Simulate network delay
        await new Promise(resolve => setTimeout(resolve, 800));

        if (mockCurriculums[dept]) {
            return mockCurriculums[dept];
        }
        throw new Error("Department not found");
    },

    analyzeProfile: async (skills: string[], dept: string, name: string): Promise<GapAnalysis> => {
        try {
            const response = await fetch(`${API_BASE_URL}/analyze`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    skills: skills,
                    department: dept,
                    student_name: name
                }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || "Analysis failed");
            }

            const data: GapAnalysisAPIResponse = await response.json();

            // Map backend response to frontend interface
            return {
                role: data.predicted_role,
                confidence: data.confidence,
                missingSkills: data.missing_skills,
                advice: data.advice
            };
        } catch (error) {
            console.error("Gap Analysis API Error:", error);
            throw error;
        }
    },

    generateRoadmap: async (role: string, skills: string[]): Promise<RoadmapStep[]> => {
        try {
            const response = await fetch(`${API_BASE_URL}/roadmap`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    role: role,
                    skills: skills
                }),
            });

            if (!response.ok) {
                console.warn("Roadmap generation failed, falling back to mock");
                return mockRoadmaps[role] || mockRoadmaps["Full Stack Developer"];
            }

            const data = await response.json();
            return data.steps;

        } catch (error) {
            console.error("Roadmap API Error:", error);
            // Fallback to mock if API fails
            return mockRoadmaps[role] || mockRoadmaps["Full Stack Developer"];
        }
    }
};
