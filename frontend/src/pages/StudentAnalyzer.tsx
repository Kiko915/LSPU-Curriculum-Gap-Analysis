import { useState, useMemo, useEffect, useRef } from "react";
import { StudentService } from "../services/StudentService";
import type { RoadmapStep } from "../types/student";
import { motion, AnimatePresence } from "framer-motion";
import { BrainCircuit, AlertTriangle, CheckCircle, X, Loader2, Sparkles, ChevronRight, Search, Map, BookOpen, Clock } from "lucide-react";
import { toast } from "sonner";
import skillsData from "../data/skills.json";

// UI Components
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Separator } from "@/components/ui/separator";
import { ShimmerButton } from "@/components/ui/shimmer-button";
import { MagicCard } from "@/components/ui/magic-card";
import { Label } from "@/components/ui/label";

interface GapAnalysisResult {
    role: string;
    confidence: number;
    missingSkills: string[];
    advice: string;
}

export default function StudentAnalyzer() {
    // Input States
    const [name, setName] = useState("");
    const [dept, setDept] = useState("BSCS");

    // Skill Autocomplete States
    const [currentSkill, setCurrentSkill] = useState("");
    const [skills, setSkills] = useState<string[]>([]);
    const [filteredSuggestions, setFilteredSuggestions] = useState<string[]>([]);
    const [showSuggestions, setShowSuggestions] = useState(false);
    const [activeIndex, setActiveIndex] = useState(0);
    const suggestionsRef = useRef<HTMLDivElement>(null);

    // Analysis States
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<GapAnalysisResult | null>(null);

    // Roadmap States
    const [roadmapLoading, setRoadmapLoading] = useState(false);
    const [roadmap, setRoadmap] = useState<RoadmapStep[] | null>(null);

    // Filter Skills Logic
    useEffect(() => {
        if (currentSkill.length > 1) {
            const matches = skillsData
                .filter(s => s.toLowerCase().includes(currentSkill.toLowerCase()) && !skills.includes(s))
                .slice(0, 8); // Limit to top 8 matches
            setFilteredSuggestions(matches);
            setShowSuggestions(true);
            setActiveIndex(0);
        } else {
            setFilteredSuggestions([]);
            setShowSuggestions(false);
        }
    }, [currentSkill, skills]);

    // Handlers
    const handleDeptChange = async (e: React.ChangeEvent<HTMLSelectElement>) => {
        const newDept = e.target.value;
        setDept(newDept);
        try {
            await StudentService.getCurriculum(newDept);
            toast.success(`Baseline Curriculum for ${newDept} Loaded`);
        } catch (error) {
            toast.error("Failed to load curriculum");
        }
    };

    const addSkill = (skillToAdd: string) => {
        if (skillToAdd && !skills.includes(skillToAdd)) {
            setSkills([...skills, skillToAdd]);
            setCurrentSkill("");
            setShowSuggestions(false);
        }
    };

    const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === "Enter") {
            e.preventDefault();
            if (showSuggestions && filteredSuggestions.length > 0) {
                addSkill(filteredSuggestions[activeIndex]);
            } else if (currentSkill.trim()) {
                // Allow adding custom skills not in list
                addSkill(currentSkill.trim());
            }
        } else if (e.key === "ArrowDown") {
            e.preventDefault();
            setActiveIndex(prev => (prev < filteredSuggestions.length - 1 ? prev + 1 : prev));
        } else if (e.key === "ArrowUp") {
            e.preventDefault();
            setActiveIndex(prev => (prev > 0 ? prev - 1 : prev));
        } else if (e.key === "Escape") {
            setShowSuggestions(false);
        }
    };

    // Click outside to close suggestions
    useEffect(() => {
        const handleClickOutside = (event: MouseEvent) => {
            if (suggestionsRef.current && !suggestionsRef.current.contains(event.target as Node)) {
                setShowSuggestions(false);
            }
        };
        document.addEventListener("mousedown", handleClickOutside);
        return () => document.removeEventListener("mousedown", handleClickOutside);
    }, []);

    const removeSkill = (skillToRemove: string) => {
        setSkills(skills.filter(s => s !== skillToRemove));
    };

    const handleAnalyze = async () => {
        if (!name.trim()) {
            toast.error("Please enter your name");
            return;
        }
        if (skills.length === 0) {
            toast.error("Please add at least one skill");
            return;
        }

        setLoading(true);
        setResult(null);
        setRoadmap(null); // Reset roadmap on new analysis

        try {
            const data = await StudentService.analyzeProfile(skills, dept, name);
            setResult(data);
            toast.success("Analysis Complete!");
        } catch (error) {
            toast.error("Analysis Failed");
        } finally {
            setLoading(false);
        }
    };

    const handleGenerateRoadmap = async () => {
        if (!result) return;
        setRoadmapLoading(true);
        try {
            const data = await StudentService.generateRoadmap(result.role, skills);
            setRoadmap(data);
            toast.success("Roadmap Generated!");

            // Smooth scroll to roadmap
            setTimeout(() => {
                const roadmapElement = document.getElementById('roadmap-section');
                if (roadmapElement) {
                    roadmapElement.scrollIntoView({ behavior: 'smooth' });
                }
            }, 100);

        } catch (error) {
            toast.error("Failed to generate roadmap");
        } finally {
            setRoadmapLoading(false);
        }
    };

    return (
        <div className="w-full bg-zinc-50 dark:bg-zinc-950 flex flex-col items-center justify-start pt-32 pb-12 px-4 md:px-8 relative overflow-x-hidden">
            {/* Background Gradients */}
            <div className="absolute top-[-10%] right-[-5%] w-[500px] h-[500px] bg-blue-500/10 rounded-full blur-[100px] pointer-events-none" />
            <div className="absolute bottom-[-10%] left-[-5%] w-[500px] h-[500px] bg-purple-500/10 rounded-full blur-[100px] pointer-events-none" />

            <div className="w-full max-w-6xl grid grid-cols-1 lg:grid-cols-2 gap-6 relative z-10 transition-all">

                {/* LEFT COLUMN: INPUTS */}
                <motion.div
                    initial={{ x: -20, opacity: 0 }}
                    animate={{ x: 0, opacity: 1 }}
                    transition={{ duration: 0.5 }}
                >
                    <MagicCard className="h-full p-8 shadow-2xl border-zinc-200 dark:border-zinc-800 bg-white/80 dark:bg-zinc-900/80 backdrop-blur-xl">
                        <div className="mb-8">
                            <h2 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-violet-600 bg-clip-text text-transparent flex items-center gap-3">
                                <BrainCircuit className="w-8 h-8 text-blue-600" />
                                A.S.P.I.R.E. Engine
                            </h2>
                            <p className="text-zinc-500 dark:text-zinc-400 mt-2">
                                AI-Driven Student Profile & Industry Readiness Engine
                            </p>
                        </div>

                        <div className="space-y-6">
                            {/* Personal Info */}
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div className="space-y-2">
                                    <Label className="text-zinc-600">Full Name</Label>
                                    <Input
                                        placeholder="Enter your name"
                                        value={name}
                                        onChange={(e) => setName(e.target.value)}
                                        className="bg-zinc-50/50 dark:bg-zinc-800/50 border-zinc-200 focus:ring-blue-500"
                                    />
                                </div>
                                <div className="space-y-2">
                                    <Label className="text-zinc-600">Department</Label>
                                    <div className="relative">
                                        <select
                                            className="w-full flex h-9 w-full rounded-md border border-input bg-zinc-50/50 dark:bg-zinc-800/50 px-3 py-1 text-sm shadow-sm transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50"
                                            value={dept}
                                            onChange={handleDeptChange}
                                        >
                                            <option value="BSCS">BS Computer Science</option>
                                            <option value="BSIT">BS Information Technology</option>
                                        </select>
                                    </div>
                                </div>
                            </div>

                            <Separator className="bg-zinc-200 dark:bg-zinc-800" />

                            {/* Skills Section */}
                            <div className="space-y-3 relative z-20" ref={suggestionsRef}>
                                <Label className="text-zinc-600 flex items-center justify-between">
                                    <span>Technical Skills</span>
                                    <span className="text-xs text-zinc-400 font-normal">{skills.length} skills added</span>
                                </Label>

                                <div className="relative">
                                    <Search className="absolute left-3 top-2.5 w-4 h-4 text-zinc-400" />
                                    <Input
                                        placeholder="Type a skill (e.g. Python, React)..."
                                        value={currentSkill}
                                        onChange={(e) => setCurrentSkill(e.target.value)}
                                        onKeyDown={handleKeyDown}
                                        onFocus={() => currentSkill.length > 1 && setShowSuggestions(true)}
                                        className="pl-9 bg-zinc-50/50 dark:bg-zinc-800/50 border-zinc-200 focus:ring-blue-500"
                                    />

                                    {/* Autocomplete Dropdown */}
                                    <AnimatePresence>
                                        {showSuggestions && filteredSuggestions.length > 0 && (
                                            <motion.div
                                                initial={{ opacity: 0, y: -10 }}
                                                animate={{ opacity: 1, y: 0 }}
                                                exit={{ opacity: 0, y: -10 }}
                                                className="absolute top-full left-0 right-0 mt-1 bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-700 rounded-lg shadow-xl z-50 max-h-60 overflow-y-auto"
                                            >
                                                {filteredSuggestions.map((suggestion, index) => (
                                                    <div
                                                        key={suggestion}
                                                        className={`px-4 py-2 cursor-pointer flex items-center justify-between text-sm transition-colors ${index === activeIndex
                                                            ? "bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300"
                                                            : "text-zinc-700 dark:text-zinc-300 hover:bg-zinc-50 dark:hover:bg-zinc-800"
                                                            }`}
                                                        onClick={() => addSkill(suggestion)}
                                                        onMouseEnter={() => setActiveIndex(index)}
                                                    >
                                                        <span>{suggestion}</span>
                                                        {index === activeIndex && <ChevronRight className="w-4 h-4 opacity-50" />}
                                                    </div>
                                                ))}
                                            </motion.div>
                                        )}
                                    </AnimatePresence>
                                </div>

                                {/* Skills Tag Cloud */}
                                <div className="flex flex-wrap gap-2 min-h-[5rem] p-4 bg-zinc-50/50 dark:bg-zinc-900/30 rounded-xl border border-dashed border-zinc-300 dark:border-zinc-700 transition-all">
                                    {skills.length === 0 && (
                                        <div className="w-full h-full flex items-center justify-center text-zinc-400 text-sm italic">
                                            Start typing to look up skills...
                                        </div>
                                    )}
                                    <AnimatePresence>
                                        {skills.map((skill) => (
                                            <motion.div
                                                key={skill}
                                                initial={{ scale: 0.8, opacity: 0 }}
                                                animate={{ scale: 1, opacity: 1 }}
                                                exit={{ scale: 0, opacity: 0 }}
                                            >
                                                <Badge
                                                    variant="secondary"
                                                    className="pl-3 pr-1 py-1 text-sm bg-white dark:bg-zinc-800 border-zinc-200 shadow-sm hover:bg-red-50 hover:text-red-600 hover:border-red-200 transition-colors group cursor-pointer gap-1"
                                                    onClick={() => removeSkill(skill)}
                                                >
                                                    {skill}
                                                    <div className="p-0.5 rounded-full hover:bg-red-100 dark:hover:bg-red-900/30">
                                                        <X className="w-3 h-3 text-zinc-400 group-hover:text-red-500" />
                                                    </div>
                                                </Badge>
                                            </motion.div>
                                        ))}
                                    </AnimatePresence>
                                </div>
                            </div>

                            <div className="pt-4">
                                <ShimmerButton
                                    onClick={handleAnalyze}
                                    className="w-full text-lg font-bold shadow-xl"
                                    background="#2563eb"
                                    shimmerColor="#93c5fd"
                                    disabled={loading}
                                >
                                    {loading ? (
                                        <div className="flex items-center gap-2">
                                            <Loader2 className="w-5 h-5 animate-spin" />
                                            Analyzing...
                                        </div>
                                    ) : (
                                        <span className="flex items-center gap-2">
                                            <Sparkles className="w-5 h-5 fill-white" />
                                            Analyze Career Path
                                        </span>
                                    )}
                                </ShimmerButton>
                            </div>
                        </div>
                    </MagicCard>
                </motion.div>

                {/* RIGHT COLUMN: RESULTS */}
                <div className="relative h-full min-h-[500px]">
                    <AnimatePresence mode="wait">
                        {!result && !loading && (
                            <motion.div
                                key="empty"
                                initial={{ opacity: 0, scale: 0.9 }}
                                animate={{ opacity: 1, scale: 1 }}
                                className="h-full flex flex-col items-center justify-center text-center p-8 bg-white/50 dark:bg-zinc-900/50 backdrop-blur-sm border border-dashed border-zinc-300 dark:border-zinc-700 rounded-3xl"
                            >
                                <div className="w-24 h-24 bg-zinc-100 dark:bg-zinc-800 rounded-full flex items-center justify-center mb-6">
                                    <BrainCircuit className="w-10 h-10 text-zinc-400" />
                                </div>
                                <h3 className="text-xl font-bold text-zinc-700 dark:text-zinc-200">Waiting for Data</h3>
                                <p className="text-zinc-500 max-w-sm mt-2">
                                    Enter your academic details and technical skills to generate a personalized career analysis.
                                </p>
                            </motion.div>
                        )}

                        {loading && (
                            <motion.div
                                key="loading"
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                exit={{ opacity: 0 }}
                                className="h-full flex flex-col items-center justify-center p-8 bg-white/50 dark:bg-zinc-900/50 backdrop-blur-sm border border-zinc-200 dark:border-zinc-800 rounded-3xl"
                            >
                                <div className="relative w-32 h-32 mb-8">
                                    <div className="absolute inset-0 border-t-4 border-blue-500 border-solid rounded-full animate-spin"></div>
                                    <div className="absolute inset-0 flex items-center justify-center">
                                        <BrainCircuit className="w-12 h-12 text-blue-500 animate-pulse" />
                                    </div>
                                </div>
                                <h3 className="text-xl font-bold text-zinc-800 dark:text-zinc-100">Crunching Numbers</h3>
                                <p className="text-zinc-500 animate-pulse mt-2">Consulting the Knowledge Graph...</p>
                            </motion.div>
                        )}

                        {result && (
                            <motion.div
                                key="result"
                                initial={{ x: 50, opacity: 0 }}
                                animate={{ x: 0, opacity: 1 }}
                                transition={{ type: "spring", bounce: 0.3 }}
                                className="h-full flex flex-col gap-4"
                            >
                                <Card className="border-blue-200/50 dark:border-blue-800/50 bg-white/90 dark:bg-zinc-900/90 backdrop-blur shadow-2xl overflow-hidden flex flex-col">
                                    <div className="absolute top-0 left-0 w-full h-2 bg-gradient-to-r from-blue-500 to-purple-600" />

                                    <CardHeader className="text-center pb-2 pt-8">
                                        <CardDescription className="uppercase tracking-widest text-xs font-bold text-blue-600 dark:text-blue-400 mb-1">
                                            {name}'s Recommended Role
                                        </CardDescription>
                                        <CardTitle className="text-4xl font-extrabold bg-gradient-to-br from-zinc-900 to-zinc-600 dark:from-white dark:to-zinc-400 bg-clip-text text-transparent">
                                            {result.role}
                                        </CardTitle>
                                        <div className="flex justify-center mt-4">
                                            <Badge variant="outline" className="bg-green-50 text-green-700 border-green-200 px-3 py-1 text-sm gap-2">
                                                <CheckCircle className="w-4 h-4" />
                                                Match Confidence: {(result.confidence * 100).toFixed(0)}%
                                            </Badge>
                                        </div>
                                    </CardHeader>

                                    <CardContent className="flex-1 p-6 md:p-8 space-y-8">
                                        {/* Gaps Section */}
                                        <div className="bg-zinc-50 dark:bg-zinc-800/50 rounded-2xl p-6 border border-zinc-100 dark:border-zinc-800 hover:border-blue-100 transition-colors">
                                            <h4 className="flex items-center gap-2 text-lg font-bold mb-4 text-zinc-800 dark:text-zinc-100">
                                                {result.missingSkills.length > 0 ? (
                                                    <>
                                                        <AlertTriangle className="text-amber-500 w-5 h-5" />
                                                        Skill Gaps Detected
                                                    </>
                                                ) : (
                                                    <>
                                                        <CheckCircle className="text-green-500 w-5 h-5" />
                                                        Ready for Deployment!
                                                    </>
                                                )}
                                            </h4>

                                            {result.missingSkills.length > 0 ? (
                                                <div className="space-y-3">
                                                    <p className="text-sm text-zinc-500">
                                                        To maximize your employability as a <span className="font-semibold text-zinc-700 dark:text-zinc-300">{result.role}</span>, consider learning:
                                                    </p>
                                                    <div className="flex flex-wrap gap-2">
                                                        {result.missingSkills.map(skill => (
                                                            <Badge
                                                                key={skill}
                                                                variant="destructive"
                                                                className="bg-amber-50 text-amber-700 hover:bg-amber-100 border-amber-200 px-3 py-1 font-medium text-sm"
                                                            >
                                                                + {skill}
                                                            </Badge>
                                                        ))}
                                                    </div>
                                                </div>
                                            ) : (
                                                <p className="text-zinc-600 dark:text-zinc-400">
                                                    You have all the core competencies required for this role. Excellent work!
                                                </p>
                                            )}
                                        </div>

                                        {/* Advice Section */}
                                        <div className="relative pl-6">
                                            <div className="absolute left-0 top-0 bottom-0 w-1 bg-gradient-to-b from-blue-500 to-purple-500 rounded-full" />
                                            <h4 className="text-sm font-bold text-zinc-400 uppercase tracking-widest mb-2">Strategic Advice</h4>
                                            <p className="text-lg text-zinc-700 dark:text-zinc-300 leading-relaxed font-medium">
                                                "{result.advice}"
                                            </p>
                                        </div>

                                        {/* Generate Roadmap Button */}
                                        <div className="pt-2">
                                            <Button
                                                onClick={handleGenerateRoadmap}
                                                disabled={roadmapLoading}
                                                className="w-full bg-zinc-900 dark:bg-white text-white dark:text-zinc-900 hover:bg-zinc-800 dark:hover:bg-zinc-200 py-6 text-lg rounded-xl shadow-lg transition-all active:scale-[0.98]"
                                            >
                                                {roadmapLoading ? (
                                                    <>
                                                        <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                                                        Generating Roadmap...
                                                    </>
                                                ) : (
                                                    <>
                                                        <Map className="w-5 h-5 mr-2" />
                                                        Generate Learning Roadmap
                                                    </>
                                                )}
                                            </Button>
                                        </div>
                                    </CardContent>
                                </Card>
                            </motion.div>
                        )}
                    </AnimatePresence>
                </div>
            </div>

            {/* ROADMAP SECTION (Appears below) */}
            <AnimatePresence>
                {roadmap && (
                    <motion.div
                        id="roadmap-section"
                        initial={{ opacity: 0, y: 50 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: 50 }}
                        transition={{ duration: 0.6, delay: 0.2 }}
                        className="w-full max-w-4xl mt-12 mb-20 relative z-10"
                    >
                        <h2 className="text-3xl font-bold text-center mb-8 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent flex items-center justify-center gap-3">
                            <Map className="w-8 h-8 text-blue-600" />
                            Your Personalized Learning Path
                        </h2>

                        <div className="relative space-y-8 before:absolute before:inset-0 before:ml-5 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-slate-300 before:to-transparent">
                            {roadmap.map((step, index) => (
                                <motion.div
                                    key={step.title}
                                    initial={{ opacity: 0, x: index % 2 === 0 ? -50 : 50 }}
                                    whileInView={{ opacity: 1, x: 0 }}
                                    viewport={{ once: true }}
                                    transition={{ duration: 0.5, delay: index * 0.2 }}
                                    className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active"
                                >
                                    {/* Icon */}
                                    <div className="flex items-center justify-center w-10 h-10 rounded-full border border-white bg-slate-300 group-[.is-active]:bg-blue-500 text-slate-500 group-[.is-active]:text-emerald-50 shadow shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 relative z-10">
                                        <BookOpen className="w-5 h-5 text-white" />
                                    </div>

                                    {/* Content Card */}
                                    <Card className="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] p-6 rounded-2xl shadow border-zinc-200 dark:border-zinc-800 bg-white/80 dark:bg-zinc-900/80 backdrop-blur-sm hover:border-blue-300 dark:hover:border-blue-700 transition-colors">
                                        <div className="flex flex-col space-y-2">
                                            <div className="flex items-center justify-between mb-1">
                                                <span className="font-bold text-blue-600 dark:text-blue-400 text-sm tracking-uppercase">
                                                    {step.title}
                                                </span>
                                                <Badge variant="secondary" className="text-xs font-normal gap-1">
                                                    <Clock className="w-3 h-3" /> {step.duration}
                                                </Badge>
                                            </div>
                                            <p className="text-zinc-600 dark:text-zinc-300 text-sm leading-relaxed">
                                                {step.description}
                                            </p>

                                            {step.resources.length > 0 && (
                                                <div className="mt-4 pt-3 border-t border-zinc-100 dark:border-zinc-800">
                                                    <p className="text-xs font-semibold text-zinc-400 mb-2 uppercase">Recommended Resources:</p>
                                                    <div className="flex flex-wrap gap-2">
                                                        {step.resources.map(res => (
                                                            <span key={res} className="text-xs bg-zinc-100 dark:bg-zinc-800 px-2 py-1 rounded text-zinc-600 dark:text-zinc-400 border border-zinc-200 dark:border-zinc-700">
                                                                {res}
                                                            </span>
                                                        ))}
                                                    </div>
                                                </div>
                                            )}
                                        </div>
                                    </Card>
                                </motion.div>
                            ))}
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
}
