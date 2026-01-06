import { motion } from 'framer-motion';
import { ArrowRight, FileText } from 'lucide-react';
import { InteractiveHoverButton } from '@/components/ui/interactive-hover-button';
import { Meteors } from '@/components/ui/meteors';

export function ResearchPaperCTA() {
    return (
        <section className="py-32 relative bg-[#030303] overflow-hidden">
            {/* Ambient Background Glows */}
            <div className="absolute inset-0 pointer-events-none">
                <div className="absolute top-0 left-1/4 w-[800px] h-[800px] bg-blue-600/5 rounded-full blur-[120px] -translate-y-1/2" />
                <div className="absolute bottom-0 right-1/4 w-[600px] h-[600px] bg-indigo-600/5 rounded-full blur-[100px] translate-y-1/2" />
            </div>

            <div className="container mx-auto px-4 relative z-10">
                <motion.div
                    initial={{ opacity: 0, y: 30 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.7 }}
                    className="max-w-4xl mx-auto text-center"
                >
                    {/* Icon Bubble */}
                    <div className="inline-flex items-center justify-center p-4 rounded-2xl bg-blue-500/10 text-blue-400 mb-8 border border-blue-500/20 shadow-[0_0_30px_rgba(59,130,246,0.15)]">
                        <FileText className="w-8 h-8" />
                    </div>

                    <h2 className="text-4xl md:text-6xl font-bold text-white mb-6 tracking-tight">
                        Want to know <span className="text-blue-500">more?</span>
                    </h2>

                    <p className="text-zinc-400 text-lg md:text-xl mb-12 leading-relaxed max-w-2xl mx-auto">
                        Dive deep into the methodology, algorithms, and results behind A.S.P.I.R.E. Access the comprehensive research paper below.
                    </p>

                    <div className="flex justify-center">
                        <InteractiveHoverButton
                            onClick={() => window.open("#", "_blank")}
                            className="text-blue-500 border-blue-500/20 hover:bg-blue-500/10"
                        >
                            Read the Full Paper
                        </InteractiveHoverButton>
                    </div>
                </motion.div>
            </div>

            {/* Decorative Grid Overlay */}
            <div className="absolute inset-0 bg-[url('/grid.svg')] bg-center [mask-image:linear-gradient(180deg,white,rgba(255,255,255,0))] opacity-5 pointer-events-none" />

            <Meteors number={20} />
        </section>
    );
}
