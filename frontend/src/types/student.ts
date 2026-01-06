export interface Curriculum {
    dept: string;
    totalUnits: number;
    description: string;
}

export interface GapAnalysis {
    role: string;
    confidence: number;
    missingSkills: string[];
    advice: string;
}

export interface RoadmapStep {
    title: string;
    description: string;
    duration: string;
    resources: string[];
}
