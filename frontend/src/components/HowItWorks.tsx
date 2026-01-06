import { useRef } from 'react';
import { motion, useScroll, useTransform } from 'framer-motion';
import { BrainCircuit, Network, TrendingUp } from 'lucide-react';

const features = [
    {
        title: "Adaptive Prediction",
        icon: BrainCircuit,
        content: "Uses NLP and Neural Networks to decode unstructured student skills and predict career fit with >80% accuracy.",
        color: "blue"
    },
    {
        title: "Symbolic Logic",
        icon: Network,
        content: "A deterministic Knowledge Graph verifies predictions against strict academic baselines to prevent hallucinations.",
        color: "indigo"
    },
    {
        title: "Industry Evaluation",
        icon: TrendingUp,
        content: "Calculates the precise 'Skill Delta' between curriculum outputs and industry requirements to recommend electives.",
        color: "violet"
    }
];

export function HowItWorks() {
    const targetRef = useRef<HTMLDivElement>(null);
    const { scrollYProgress } = useScroll({
        target: targetRef,
    });

    // Horizontal scroll transform
    // We scroll the cards from right to left as the user scrolls down
    const x = useTransform(scrollYProgress, [0.1, 0.9], ["50%", "-50%"]);
    const opacity = useTransform(scrollYProgress, [0, 0.2], [0, 1]);
    const scale = useTransform(scrollYProgress, [0, 0.2], [0.8, 1]);

    return (
        <section ref={targetRef} className="relative h-[300vh] bg-[#030303]">
            <div className="sticky top-0 h-screen flex flex-col justify-center overflow-hidden">

                {/* Background Ambience */}
                <div className="absolute inset-0 pointer-events-none">
                    <div className="absolute top-[20%] left-[20%] w-[500px] h-[500px] bg-blue-600/5 rounded-full blur-[120px]" />
                    <div className="absolute bottom-[20%] right-[20%] w-[400px] h-[400px] bg-purple-600/5 rounded-full blur-[100px]" />
                </div>

                {/* Header Section - Fades in first */}
                <motion.div
                    style={{ opacity, scale }}
                    className="container mx-auto px-4 text-center mb-12 md:mb-20 relative z-10"
                >
                    <h2 className="text-4xl md:text-6xl font-bold mb-6 text-white">
                        Engineered for <span className="text-blue-500">Precision</span>
                    </h2>
                    <p className="text-zinc-400 max-w-2xl mx-auto text-lg md:text-xl">
                        Our hybrid architecture combines probabilistic AI with deterministic logic for reliable results.
                    </p>
                </motion.div>

                {/* Horizontal Scroll Track */}
                <div className="w-full relative z-10">
                    <motion.div
                        style={{ x }}
                        className="flex gap-8 md:gap-12 px-4 md:px-20 w-max mx-auto"
                    >
                        {features.map((feature, index) => (
                            <div
                                key={index}
                                className="w-[85vw] md:w-[600px] h-[400px] md:h-[350px] relative group p-1"
                            >
                                {/* Card Glow Border */}
                                <div className="absolute inset-0 bg-gradient-to-r from-blue-500/0 via-blue-500/20 to-blue-500/0 rounded-3xl opacity-0 group-hover:opacity-100 transition-opacity duration-500" />

                                <div className="relative h-full bg-[#0a0a0a] border border-white/10 rounded-3xl p-8 md:p-12 flex flex-col justify-center backdrop-blur-xl hover:border-blue-500/30 transition-colors duration-300">
                                    {/* Icon */}
                                    <div className="w-16 h-16 rounded-2xl bg-blue-500/10 flex items-center justify-center mb-6 text-blue-400 group-hover:scale-110 group-hover:bg-blue-500/20 transition-all duration-300">
                                        <feature.icon className="h-8 w-8" />
                                    </div>

                                    {/* Content */}
                                    <h3 className="text-2xl md:text-3xl font-bold mb-4 text-white group-hover:text-blue-300 transition-colors">
                                        {feature.title}
                                    </h3>
                                    <p className="text-zinc-400 text-lg leading-relaxed">
                                        {feature.content}
                                    </p>

                                    {/* Decorative number */}
                                    <div className="absolute top-8 right-8 text-8xl font-black text-white/5 select-none font-mono">
                                        0{index + 1}
                                    </div>
                                </div>
                            </div>
                        ))}
                    </motion.div>
                </div>

                {/* Side Fade/Blur Overlays */}
                <div className="pointer-events-none absolute inset-y-0 left-0 w-24 md:w-48 bg-gradient-to-r from-[#030303] via-[#030303]/80 to-transparent z-20" />
                <div className="pointer-events-none absolute inset-y-0 right-0 w-24 md:w-48 bg-gradient-to-l from-[#030303] via-[#030303]/80 to-transparent z-20" />

                {/* Scroll Indicator */}
                <div className="absolute bottom-10 left-1/2 -translate-x-1/2 flex gap-3">
                    {[0, 1, 2].map((i) => {
                        // Calculate active range for each dot
                        // Scroll triggers from 0.1 to 0.9. Split into 3 segments.
                        const start = 0.1 + (i * 0.26);
                        const peak = start + 0.13;
                        const end = start + 0.26;

                        // Transform opacities based on active range
                        const opacity = useTransform(scrollYProgress,
                            [start, peak, end],
                            [0.3, 1, 0.3]
                        );

                        const scale = useTransform(scrollYProgress,
                            [start, peak, end],
                            [1, 1.5, 1]
                        );

                        // Highlight color for active state
                        const backgroundColor = useTransform(scrollYProgress,
                            [start, peak, end],
                            ["rgba(59, 130, 246, 0.3)", "rgba(59, 130, 246, 1)", "rgba(59, 130, 246, 0.3)"]
                        );

                        return (
                            <motion.div
                                key={i}
                                style={{ opacity, scale, backgroundColor }}
                                className="w-2 h-2 rounded-full cursor-pointer"
                            />
                        );
                    })}
                </div>
            </div>
        </section>
    );
}
