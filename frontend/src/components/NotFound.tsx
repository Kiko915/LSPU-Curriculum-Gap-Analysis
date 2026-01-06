import { Link } from '@tanstack/react-router'
import { ShimmerButton } from '@/components/ui/shimmer-button'
import { motion } from 'framer-motion'
import { AlertTriangle } from 'lucide-react'

export function NotFound() {
    return (
        <div className="min-h-[calc(100vh-4rem)] flex flex-col items-center justify-center p-4 text-center space-y-8">
            <motion.div
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.5, ease: "backOut" }}
                className="relative"
            >
                <h1 className="text-9xl font-black tracking-tighter text-primary/20 select-none">
                    404
                </h1>
                <div className="absolute inset-0 flex items-center justify-center">
                    <h1 className="text-9xl font-black tracking-tighter text-primary/40 blur-sm animate-pulse select-none">
                        404
                    </h1>
                </div>
                <div className="absolute inset-0 flex items-center justify-center">
                    <h1 className="text-9xl font-black tracking-tighter text-foreground mix-blend-overlay select-none">
                        404
                    </h1>
                </div>
            </motion.div>

            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
                className="space-y-4 max-w-md"
            >
                <div className="flex items-center justify-center gap-2 text-destructive font-mono text-lg tracking-widest uppercase font-bold">
                    <AlertTriangle className="w-5 h-5" />
                    PROTOCOL_FAILURE
                </div>
                <p className="text-xl text-muted-foreground font-medium">
                    The requested route is outside of operational parameters.
                </p>
            </motion.div>

            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4 }}
            >
                <Link to="/">
                    <ShimmerButton className="font-bold text-lg">
                        Return to Base
                    </ShimmerButton>
                </Link>
            </motion.div>
        </div>
    )
}
