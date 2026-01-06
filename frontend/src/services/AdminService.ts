import axios from 'axios';
import type { DashboardData, Recommendation } from '../types/admin';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Define API Reponse Types locally to ensure type safety
interface ApiStudentStats {
    total_requests: number;
    top_5_roles: Array<{ role: string; count: number }>;
    top_10_missing_skills: Array<{ skill: string; count: number }>;
}

interface ApiCoverageItem {
    aligned_subjects: Array<{ code: string; alignment_score: number }>;
    subject_count: number;
    bscs_count: number;
    bsit_count: number;
    bscs_stats: { readiness: number; gap: string; missing_count: number };
    bsit_stats: { readiness: number; gap: string; missing_count: number };
}

interface ApiRecommendation {
    type: string;
    role?: string;
    skill?: string;
    message: string;
    action: string;
}

interface ApiResponse {
    student_stats: ApiStudentStats;
    curriculum_coverage: Record<string, ApiCoverageItem>;
    ai_recommendations: ApiRecommendation[];
    summary: {
        total_student_requests: number;
        [key: string]: any;
    };
}

export const AdminService = {
    async getRecommendations(): Promise<DashboardData> {
        const response = await axios.get<ApiResponse>(`${API_URL}/admin/recommendations`);
        console.log("Admin API Response:", response.data); // DEBUG
        const { student_stats, curriculum_coverage, ai_recommendations, summary } = response.data;
        console.log("Curriculum Coverage Keys:", Object.keys(curriculum_coverage)); // DEBUG

        // Transform KPI Data
        const kpi = {
            totalStudents: summary.total_student_requests,
            topRole: student_stats.top_5_roles.length > 0 ? student_stats.top_5_roles[0].role : "N/A",
            criticalGap: student_stats.top_10_missing_skills.length > 0 ? student_stats.top_10_missing_skills[0].skill : "None"
        };

        // Transform Department Stats
        const getDeptStats = (deptKey: 'bscs_stats' | 'bsit_stats') => {
            let maxReadiness_ = -1;
            let topRole = "N/A";
            let topGap = "None";

            Object.entries(curriculum_coverage).forEach(([role, data]) => {
                const stats = data[deptKey];
                // Check if this role has higher readiness than current max
                if (stats && stats.readiness > maxReadiness_) {
                    maxReadiness_ = stats.readiness;
                    topRole = role;
                    topGap = stats.gap;
                }
            });

            return {
                top_role: topRole,
                // If topGap is "None", it means fully ready. Otherwise show missing skill.
                gap: topGap === "None" ? "All Skills Covered" : `Missing: ${topGap}`,
                readiness: maxReadiness_ === -1 ? 0 : maxReadiness_
            };
        };

        const department_stats = {
            BSCS: getDeptStats('bscs_stats'),
            BSIT: getDeptStats('bsit_stats')
        };

        // Transform Chart Data
        const chartData = student_stats.top_5_roles.map((item) => {
            const role = item.role;
            const coverage = curriculum_coverage[role] || { bscs_count: 0, bsit_count: 0 };
            return {
                role: role,
                industryDemand: item.count,
                bscsSupply: coverage.bscs_count,
                bsitSupply: coverage.bsit_count
            };
        });

        // Transform Recommendations
        const recommendations: Recommendation[] = ai_recommendations.map((rec, index) => {
            let severity: "critical" | "warning" | "info" = "info";
            if (rec.type === "CRITICAL") severity = "critical";
            if (rec.type === "WARNING") severity = "warning";
            if (rec.type === "SKILL_GAP") severity = "warning";

            return {
                id: `rec-${index}`,
                title: rec.type.replace('_', ' '),
                department: "All",
                description: rec.message,
                severity: severity,
                timestamp: "Just now"
            };
        });

        return {
            kpi,
            department_stats,
            chartData,
            recommendations
        };
    }
};
