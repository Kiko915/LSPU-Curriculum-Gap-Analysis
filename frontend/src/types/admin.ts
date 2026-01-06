export interface KPIStats {
    totalStudents: number;
    topRole: string;
    criticalGap: string;
}

export interface DepartmentStat {
    top_role: string;
    gap: string;
    readiness: number;
}

export interface DepartmentStats {
    BSCS: DepartmentStat;
    BSIT: DepartmentStat;
}

export interface SkillGapData {
    role: string;
    industryDemand: number;
    bscsSupply: number;
    bsitSupply: number;
}

export type AlertSeverity = "critical" | "warning" | "info";

export interface Recommendation {
    id: string;
    title: string;
    department?: "BSCS" | "BSIT" | "All";
    description: string;
    severity: AlertSeverity;
    timestamp: string;
}

export interface DashboardData {
    kpi: KPIStats;
    department_stats: DepartmentStats;
    chartData: SkillGapData[];
    recommendations: Recommendation[];
}
