import { useEffect, useState } from "react";
import { AdminService } from "../services/AdminService";
import type { DashboardData, Recommendation } from "../types/admin";
import {
    Users,
    TrendingUp,
    AlertOctagon,
    BrainCircuit,
    AlertTriangle,
    Info,
    Loader2
} from "lucide-react";
import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
    ResponsiveContainer
} from "recharts";

// UI Components
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";

export default function AdminDashboard() {
    const [data, setData] = useState<DashboardData | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const dashboardData = await AdminService.getRecommendations();
                setData(dashboardData);
            } catch (error) {
                console.error("Failed to fetch admin data", error);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, []);

    if (loading) {
        return (
            <div className="min-h-screen bg-zinc-950 flex flex-col items-center justify-center">
                <div className="flex flex-col items-center gap-4">
                    <Loader2 className="w-10 h-10 animate-spin text-blue-500" />
                    <p className="text-zinc-400 font-medium animate-pulse">Aggregating University Data...</p>
                </div>
            </div>
        );
    }

    if (!data) return null;

    return (
        <div className="min-h-screen bg-zinc-950 text-zinc-100 p-6 md:p-8 font-sans relative overflow-hidden">
            {/* Background Gradients */}
            <div className="absolute top-[-10%] left-[-5%] w-[500px] h-[500px] bg-blue-500/10 rounded-full blur-[100px] pointer-events-none" />
            <div className="absolute bottom-[-10%] right-[-5%] w-[500px] h-[500px] bg-purple-500/10 rounded-full blur-[100px] pointer-events-none" />

            <div className="max-w-7xl mx-auto space-y-8 relative z-10">

                {/* Header */}
                <header className="space-y-2">
                    <h1 className="text-3xl font-bold tracking-tight flex items-center gap-3">
                        <BrainCircuit className="w-8 h-8 text-blue-500" />
                        <span className="bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
                            Curriculum Strategic Board
                        </span>
                    </h1>
                    <p className="text-zinc-400 text-lg">
                        Powered by <span className="font-semibold text-blue-400">A.S.P.I.R.E. Engine</span> • Real-time Gap Analysis
                    </p>
                </header>

                <Separator className="bg-zinc-800" />

                {/* KPI Row */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <Card className="bg-zinc-900/50 backdrop-blur-sm border-zinc-800 hover:border-blue-500/50 transition-all shadow-lg hover:shadow-blue-500/10">
                        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                            <CardTitle className="text-sm font-medium text-zinc-400">Total Students Analyzed</CardTitle>
                            <Users className="h-4 w-4 text-blue-500" />
                        </CardHeader>
                        <CardContent>
                            <div className="text-3xl font-bold text-white">{data.kpi.totalStudents.toLocaleString()}</div>
                            <p className="text-xs text-zinc-500 mt-1 flex items-center gap-1">
                                <span className="text-emerald-400 font-medium">+12%</span> from last semester
                            </p>
                        </CardContent>
                    </Card>

                    <Card className="bg-zinc-900/50 backdrop-blur-sm border-zinc-800 hover:border-purple-500/50 transition-all shadow-lg hover:shadow-purple-500/10">
                        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                            <CardTitle className="text-sm font-medium text-zinc-400">Top Predicted Role</CardTitle>
                            <TrendingUp className="h-4 w-4 text-purple-500" />
                        </CardHeader>
                        <CardContent>
                            <div className="text-3xl font-bold text-white">{data.kpi.topRole}</div>
                            <p className="text-xs text-zinc-500 mt-1">High alignment with curriculum</p>
                        </CardContent>
                    </Card>

                    <Card className="bg-zinc-900/50 backdrop-blur-sm border-zinc-800 hover:border-red-500/50 transition-all shadow-lg hover:shadow-red-500/10">
                        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                            <CardTitle className="text-sm font-medium text-zinc-400">Critical Skill Gap</CardTitle>
                            <AlertOctagon className="h-4 w-4 text-red-500" />
                        </CardHeader>
                        <CardContent>
                            <div className="text-3xl font-bold text-red-400">{data.kpi.criticalGap}</div>
                            <p className="text-xs text-zinc-500 mt-1">Immediate intervention recommended</p>
                        </CardContent>
                    </Card>
                </div>

                {/* Program Comparison Section */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {/* BSCS Health Card */}
                    <Card className="bg-zinc-900/50 backdrop-blur-sm border-l-4 border-l-blue-500 border-zinc-800 shadow-md">
                        <CardHeader className="pb-2">
                            <CardTitle className="text-lg font-bold text-blue-400 flex items-center justify-between">
                                BS Computer Science
                                <Badge variant="secondary" className="bg-blue-500/10 text-blue-400 border-blue-500/20">{data.department_stats.BSCS.readiness}% Readiness</Badge>
                            </CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div className="flex justify-between items-center bg-zinc-800/50 p-3 rounded-lg">
                                <span className="text-zinc-400 text-sm">Top Role</span>
                                <span className="font-semibold text-zinc-200">{data.department_stats.BSCS.top_role}</span>
                            </div>
                            <div className="flex justify-between items-center bg-zinc-800/50 p-3 rounded-lg border border-red-500/20">
                                <span className="text-zinc-400 text-sm">Gap</span>
                                <span className="font-semibold text-red-400">{data.department_stats.BSCS.gap}</span>
                            </div>
                        </CardContent>
                    </Card>

                    {/* BSIT Health Card */}
                    <Card className="bg-zinc-900/50 backdrop-blur-sm border-l-4 border-l-emerald-500 border-zinc-800 shadow-md">
                        <CardHeader className="pb-2">
                            <CardTitle className="text-lg font-bold text-emerald-400 flex items-center justify-between">
                                BS Info Tech
                                <Badge variant="secondary" className="bg-emerald-500/10 text-emerald-400 border-emerald-500/20">{data.department_stats.BSIT.readiness}% Readiness</Badge>
                            </CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div className="flex justify-between items-center bg-zinc-800/50 p-3 rounded-lg">
                                <span className="text-zinc-400 text-sm">Top Role</span>
                                <span className="font-semibold text-zinc-200">{data.department_stats.BSIT.top_role}</span>
                            </div>
                            <div className="flex justify-between items-center bg-zinc-800/50 p-3 rounded-lg border border-red-500/20">
                                <span className="text-zinc-400 text-sm">Gap</span>
                                <span className="font-semibold text-red-400">{data.department_stats.BSIT.gap}</span>
                            </div>
                        </CardContent>
                    </Card>
                </div>

                {/* Main Content Grid */}
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">

                    {/* Main Chart: Grouped Bar Chart */}
                    <Card className="col-span-1 lg:col-span-2 bg-zinc-900/50 backdrop-blur-sm border-zinc-800 shadow-xl">
                        <CardHeader>
                            <CardTitle className="text-xl font-bold text-white">Program vs. Industry Alignment</CardTitle>
                            <CardDescription className="text-zinc-400">
                                Comparing Industry Demand against BSCS and BSIT Curriculum Coverage.
                            </CardDescription>
                        </CardHeader>
                        <CardContent className="h-[400px]">
                            <ResponsiveContainer width="100%" height="100%">
                                <BarChart data={data.chartData} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
                                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#3f3f46" />
                                    <XAxis
                                        dataKey="role"
                                        stroke="#a1a1aa"
                                        fontSize={12}
                                        tickLine={false}
                                        axisLine={false}
                                    />
                                    <YAxis
                                        stroke="#a1a1aa"
                                        fontSize={12}
                                        tickLine={false}
                                        axisLine={false}
                                    />
                                    <Tooltip
                                        cursor={{ fill: '#27272a' }}
                                        contentStyle={{ backgroundColor: '#18181b', borderRadius: '8px', border: '1px solid #3f3f46', color: '#fff' }}
                                    />
                                    <Legend wrapperStyle={{ paddingTop: '20px' }} />
                                    <Bar
                                        dataKey="industryDemand"
                                        name="Industry Demand"
                                        fill="#71717a"
                                        radius={[4, 4, 0, 0]}
                                        barSize={20}
                                    />
                                    <Bar
                                        dataKey="bscsSupply"
                                        name="BSCS Coverage"
                                        fill="#3b82f6"
                                        radius={[4, 4, 0, 0]}
                                        barSize={20}
                                    />
                                    <Bar
                                        dataKey="bsitSupply"
                                        name="BSIT Coverage"
                                        fill="#10b981"
                                        radius={[4, 4, 0, 0]}
                                        barSize={20}
                                    />
                                </BarChart>
                            </ResponsiveContainer>
                        </CardContent>
                    </Card>

                    {/* Recommendation Feed */}
                    <Card className="bg-zinc-900/50 backdrop-blur-sm border-zinc-800 shadow-xl flex flex-col max-h-[500px]">
                        <CardHeader>
                            <CardTitle className="text-xl font-bold text-white flex items-center gap-2">
                                <SparklesIcon className="w-5 h-5 text-amber-500" />
                                AI Insights
                            </CardTitle>
                            <CardDescription className="text-zinc-400">Real-time strategic recommendations</CardDescription>
                        </CardHeader>
                        <CardContent className="flex-1 overflow-y-auto pr-2 space-y-4 custom-scrollbar">
                            {data.recommendations.map((rec) => (
                                <RecommendationCard key={rec.id} recommendation={rec} />
                            ))}
                        </CardContent>
                    </Card>
                </div>
            </div>
        </div>
    );
}

// Sub-component for Recommendation Cards
function RecommendationCard({ recommendation }: { recommendation: Recommendation }) {
    const severityStyles = {
        critical: "border-l-red-500 bg-red-950/20 hover:bg-red-950/30",
        warning: "border-l-amber-500 bg-amber-950/20 hover:bg-amber-950/30",
        info: "border-l-blue-500 bg-blue-950/20 hover:bg-blue-950/30"
    };

    const icons = {
        critical: <AlertTriangle className="w-5 h-5 text-red-500 shrink-0" />,
        warning: <AlertOctagon className="w-5 h-5 text-amber-500 shrink-0" />,
        info: <Info className="w-5 h-5 text-blue-500 shrink-0" />
    };

    return (
        <div className={`p-4 rounded-r-lg border-l-4 border-y border-r border-y-zinc-800 border-r-zinc-800 transition-colors ${severityStyles[recommendation.severity]}`}>
            <div className="flex items-start gap-3">
                {icons[recommendation.severity]}
                <div className="space-y-1 w-full">
                    <div className="flex items-center justify-between w-full mb-1">
                        <h4 className="font-semibold text-white text-sm">{recommendation.title}</h4>
                        <span className="text-[10px] text-zinc-500 font-mono">{recommendation.timestamp}</span>
                    </div>
                    {recommendation.department && (
                        <Badge variant="outline" className={`mb-2 px-1.5 py-0 text-[10px] h-5 ${recommendation.department === 'BSCS' ? 'text-blue-400 border-blue-500/30 bg-blue-500/10' :
                            recommendation.department === 'BSIT' ? 'text-emerald-400 border-emerald-500/30 bg-emerald-500/10' :
                                'text-zinc-400 border-zinc-700 bg-zinc-800'
                            }`}>
                            {recommendation.department}
                        </Badge>
                    )}
                    <p className="text-xs text-slate-400 leading-relaxed">
                        {recommendation.description}
                    </p>
                </div>
            </div>
        </div>
    );
}

function SparklesIcon({ className }: { className?: string }) {
    return (
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
            <path d="M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962L8.5 9.936A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .963 0L14.063 8.5A2 2 0 0 0 15.5 9.937l6.135 1.581a.5.5 0 0 1 0 .962L15.5 14.063a2 2 0 0 0-1.437 1.437l-1.582 6.135a.5.5 0 0 1-.963 0z" />
        </svg>
    )
}
