import { motion } from 'framer-motion';

export function LoadingScreen() {
    return (
        <motion.div
            className="fixed inset-0 z-[100] flex flex-col items-center justify-center bg-black"
            initial={{ opacity: 1 }}
            exit={{
                opacity: 0,
                transition: { duration: 0.8, ease: "easeInOut" }
            }}
        >
            <div className="relative flex flex-col items-center gap-8">
                {/* Logo Animation */}
                <motion.div
                    initial={{ scale: 0.8, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    transition={{ duration: 0.5, ease: "easeOut" }}
                    className="relative"
                >
                    <img
                        src="/dhekode-logo-black.png"
                        alt="DheKode Logo"
                        className="h-16 w-auto invert md:h-20"
                    />
                    {/* Subtle glow effect behind logo */}
                    <div className="absolute inset-0 bg-indigo-500/20 blur-2xl rounded-full -z-10" />
                </motion.div>

                {/* Progress Bar Container */}
                <div className="w-48 h-1 bg-white/10 rounded-full overflow-hidden">
                    <motion.div
                        className="h-full bg-indigo-500"
                        initial={{ width: "0%" }}
                        animate={{ width: "100%" }}
                        transition={{
                            duration: 2,
                            ease: "easeInOut"
                        }}
                    />
                </div>

                {/* Loading Text */}
                <motion.p
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.2 }}
                    className="text-white/40 text-xs font-mono tracking-[0.2em] uppercase"
                >
                    Initializing System...
                </motion.p>
            </div>

            {/* Background Effects */}
            <div className="absolute inset-0 pointer-events-none">
                <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-indigo-500/10 rounded-full blur-[100px]" />
                <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-500/10 rounded-full blur-[100px]" />
            </div>
        </motion.div>
    );
}
