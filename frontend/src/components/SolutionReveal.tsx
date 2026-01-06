import { useRef } from 'react';
import { motion, useScroll, useTransform, useSpring } from 'framer-motion';

export function SolutionReveal() {
    const containerRef = useRef<HTMLDivElement>(null);
    const { scrollYProgress } = useScroll({
        target: containerRef,
        offset: ["start start", "end end"]
    });

    // Smooth out the scroll progress with snappier physics
    const smoothProgress = useSpring(scrollYProgress, {
        stiffness: 200,
        damping: 20,
        restDelta: 0.001
    });

    const headerOpacity = useTransform(smoothProgress, [0, 0.1], [0, 1]);
    const headerScale = useTransform(smoothProgress, [0, 0.1], [0.8, 1]);

    const letters = "ASPIRE".split("");

    return (
        <section ref={containerRef} className="h-[400vh] relative bg-[#030303]">
            <div className="sticky top-0 h-screen flex flex-col items-center justify-center overflow-hidden perspective-[2000px]">
                {/* Refined Ambient Background */}
                <motion.div
                    className="absolute inset-0 pointer-events-none"
                    style={{ opacity: useTransform(smoothProgress, [0, 0.2], [0, 1]) }}
                >
                    <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-blue-600/10 rounded-full blur-[120px]" />
                    <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-blue-600/5 rounded-full blur-[100px]" />
                </motion.div>

                {/* Introductory Header */}
                <motion.div
                    style={{ opacity: headerOpacity, scale: headerScale }}
                    className="mb-16 md:mb-24 relative z-10"
                >
                    <span className="inline-block px-4 py-1.5 rounded-full border border-blue-500/20 bg-blue-500/10 text-blue-300 text-sm font-medium tracking-wide">
                        THE ARCHITECTURE
                    </span>
                </motion.div>

                {/* 3D Acronym Container */}
                <div className="flex gap-2 md:gap-6 relative z-10" style={{ transformStyle: "preserve-3d" }}>
                    {letters.map((letter, i) => {
                        const step = 0.6 / letters.length;
                        const start = 0.1 + (step * i);
                        const end = start + step;

                        // 3D & Pop Animation transforms
                        // We use a sub-range for the "pop" to make it faster than the full step
                        const popEnd = start + (step * 0.8);

                        const opacity = useTransform(smoothProgress, [start, popEnd], [0, 1]);
                        const scale = useTransform(smoothProgress, [start, popEnd], [0.2, 1]);
                        const z = useTransform(smoothProgress, [start, popEnd], [100, 0]); // Comes from slightly in front
                        const rotateX = useTransform(smoothProgress, [start, popEnd], [45, 0]);
                        const filter = useTransform(smoothProgress, [start, popEnd], ["blur(10px) brightness(2)", "blur(0px) brightness(1)"]);

                        // Text Gradient Effect
                        const textGradient = "bg-gradient-to-b from-white via-blue-100 to-blue-200/50 bg-clip-text text-transparent";
                        // Using blue-500 rgb values (59, 130, 246)
                        const shadow = "drop-shadow-[0_0_15px_rgba(59,130,246,0.6)]";

                        return (
                            <div key={i} className="flex items-baseline relative" style={{ perspective: "1000px" }}>
                                <motion.span
                                    style={{ opacity, scale, z, rotateX, filter }}
                                    className={`text-[80px] md:text-[160px] font-black tracking-tighter leading-none ${textGradient} ${shadow}`}
                                >
                                    {letter}
                                </motion.span>

                                {/* Animated Dot - Delayed slightly */}
                                <motion.span
                                    style={{
                                        opacity: useTransform(smoothProgress, [popEnd - 0.05, popEnd], [0, 1]),
                                        scale: useTransform(smoothProgress, [popEnd - 0.05, popEnd], [0, 1]),
                                        y: useTransform(smoothProgress, [popEnd - 0.05, popEnd], [20, 0])
                                    }}
                                    className="text-4xl md:text-8xl font-bold text-blue-400 ml-1 md:ml-2 drop-shadow-[0_0_10px_rgba(59,130,246,1)]"
                                >
                                    .
                                </motion.span>
                            </div>
                        );
                    })}
                </div>

                {/* Full Definition Reveal */}
                <motion.div
                    className="mt-16 text-center relative z-10 max-w-5xl px-6"
                    style={{
                        opacity: useTransform(smoothProgress, [0.8, 0.9], [0, 1]),
                        y: useTransform(smoothProgress, [0.8, 0.9], [60, 0]),
                        filter: useTransform(smoothProgress, [0.8, 0.9], ["blur(10px)", "blur(0px)"])
                    }}
                >
                    <h2 className="text-xl md:text-3xl font-bold text-white mb-6 leading-tight">
                        <span className="text-blue-400">A</span>utomated{" "}
                        <span className="text-blue-400">S</span>kill{" "}
                        <span className="text-blue-400">P</span>rediction &{" "}
                        <span className="text-blue-400">I</span>ndustry{" "}
                        <span className="text-blue-400">R</span>easoning{" "}
                        <span className="text-blue-400">E</span>ngine
                    </h2>
                    <p className="text-zinc-400 text-lg md:text-xl max-w-2xl mx-auto leading-relaxed">
                        A real-time synchronization layer ensuring academic output matches modern industry velocity.
                    </p>
                </motion.div>

                {/* Progress Indicator */}
                <motion.div
                    className="absolute bottom-12 left-1/2 -translate-x-1/2 w-64 h-1 bg-white/5 rounded-full overflow-hidden"
                    style={{ opacity: useTransform(smoothProgress, [0.1, 0.9], [1, 0]) }}
                >
                    <motion.div
                        className="h-full bg-blue-500"
                        style={{ scaleX: smoothProgress, transformOrigin: "left" }}
                    />
                </motion.div>
            </div>
        </section>
    );
}
