import { useState, useEffect } from 'react'
import { createRootRoute, Link, Outlet } from '@tanstack/react-router'
import { TanStackRouterDevtools } from '@tanstack/react-router-devtools'
import { Button } from '@/components/ui/button'
import { NotFound } from '@/components/NotFound'
import { Footer } from '@/components/Footer'
import { Toaster } from "@/components/ui/sonner"
import { Menu, X } from 'lucide-react'
import { AnimatePresence, motion } from 'framer-motion'
import { LoadingScreen } from '@/components/ui/loading-screen'

export const Route = createRootRoute({
    notFoundComponent: NotFound,
    component: RootComponent,
})

const menuVariants = {
    closed: {
        opacity: 0,
        x: "100%",
        transition: {
            duration: 0.5,
            ease: "easeInOut",
            when: "afterChildren"
        }
    },
    open: {
        opacity: 1,
        x: 0,
        transition: {
            duration: 0.5,
            ease: "easeInOut",
            when: "beforeChildren",
            staggerChildren: 0.1
        }
    }
} as const

const menuItemVariants = {
    closed: { opacity: 0, y: 20 },
    open: { opacity: 1, y: 0, transition: { duration: 0.5, ease: "easeInOut" } }
} as const

function RootComponent() {
    const [isOpen, setIsOpen] = useState(false)
    const [isGlobalLoading, setIsGlobalLoading] = useState(true)

    // Simulate initial loading
    useEffect(() => {
        const timer = setTimeout(() => {
            setIsGlobalLoading(false)
        }, 2200) // Slightly longer than the progress bar animation (2s)
        return () => clearTimeout(timer)
    }, [])

    // Lock body scroll when menu is open or loading
    useEffect(() => {
        if (isOpen || isGlobalLoading) {
            document.body.style.overflow = 'hidden'
        } else {
            document.body.style.overflow = 'unset'
        }
        return () => {
            document.body.style.overflow = 'unset'
        }
    }, [isOpen, isGlobalLoading])

    return (
        <div className="min-h-screen bg-background text-foreground font-mono flex flex-col">
            {/* Top Banner */}
            <div className="w-full bg-blue-600 text-white py-2 text-center text-xs md:text-sm font-medium z-50 relative px-4">
                ML Finals: Predictive Analysis of Industry Skill Demand using LSPU-SCC Computer Studies Curriculum Data
            </div>

            <AnimatePresence mode="wait">
                {isGlobalLoading && <LoadingScreen />}
            </AnimatePresence>

            <header className="border-b border-border/40 sticky top-0 z-50 bg-background/80 backdrop-blur-sm">
                <div className="container mx-auto px-4 h-16 flex items-center justify-between">
                    {/* Logo - Left */}
                    <Link to="/" className="font-black text-xl tracking-tighter flex items-center gap-2 z-50 relative" onClick={() => setIsOpen(false)}>
                        <img
                            src="/dhekode-logo-black.png"
                            alt="DheKode Logo"
                            className="h-6 w-auto invert"
                        />
                    </Link>

                    {/* Desktop Navigation - Center */}
                    <nav className="hidden md:flex items-center gap-8 absolute left-1/2 -translate-x-1/2 font-medium text-sm text-muted-foreground">
                        <Link to="/" className="hover:text-foreground transition-colors" activeProps={{ className: 'text-foreground font-bold' }} activeOptions={{ exact: true }}>Home</Link>
                        <Link to="/student" className="hover:text-foreground transition-colors" activeProps={{ className: 'text-foreground font-bold' }}>Student</Link>
                        <Link to="/admin" className="hover:text-foreground transition-colors" activeProps={{ className: 'text-foreground font-bold' }}>Faculty</Link>
                    </nav>

                    {/* Desktop Auth Buttons - Right */}
                    <div className="hidden md:flex items-center gap-4">
                        <Link to="/contact">
                            <Button size="sm" className="rounded-full px-6 font-semibold bg-primary text-white hover:bg-primary/90">
                                Contact Us
                            </Button>
                        </Link>
                    </div>

                    {/* Mobile Menu Open Button */}
                    <button
                        className="md:hidden p-2 text-foreground relative transition-opacity hover:opacity-80"
                        onClick={() => setIsOpen(true)}
                        aria-label="Open menu"
                    >
                        <Menu className="h-8 w-8" />
                    </button>

                </div>
            </header>

            {/* Mobile Menu Overlay - Moved outside header to avoid containment issues */}
            <AnimatePresence>
                {isOpen && (
                    <motion.div
                        key="mobile-menu"
                        initial="closed"
                        animate="open"
                        exit="closed"
                        variants={menuVariants}
                        className="fixed inset-0 z-60 bg-background flex flex-col md:hidden"
                    >
                        {/* Mobile Menu Header with Logo and Close Button */}
                        <div className="h-16 flex items-center justify-between px-4 border-b border-border/40 container mx-auto">
                            <Link to="/" className="font-black text-xl tracking-tighter flex items-center gap-2" onClick={() => setIsOpen(false)}>
                                <img
                                    src="/dhekode-logo-black.png"
                                    alt="DheKode Logo"
                                    className="h-6 w-auto invert"
                                />
                            </Link>

                            <button
                                className="p-2 text-foreground relative transition-opacity hover:opacity-80"
                                onClick={() => setIsOpen(false)}
                                aria-label="Close menu"
                            >
                                <X className="h-8 w-8" />
                            </button>
                        </div>

                        {/* Mobile Menu Links */}
                        <nav className="flex-1 flex flex-col justify-center items-center gap-8 font-black text-2xl text-center tracking-tighter p-6">
                            <motion.div variants={menuItemVariants}>
                                <Link
                                    to="/"
                                    className="hover:text-primary transition-colors block"
                                    activeProps={{ className: 'text-foreground' }}
                                    activeOptions={{ exact: true }}
                                    onClick={() => setIsOpen(false)}
                                >
                                    Home
                                </Link>
                            </motion.div>
                            <motion.div variants={menuItemVariants}>
                                <Link
                                    to="/student"
                                    className="hover:text-primary transition-colors block"
                                    activeProps={{ className: 'text-foreground' }}
                                    onClick={() => setIsOpen(false)}
                                >
                                    Student
                                </Link>
                            </motion.div>
                            <motion.div variants={menuItemVariants}>
                                <Link
                                    to="/admin"
                                    className="hover:text-primary transition-colors block"
                                    activeProps={{ className: 'text-foreground' }}
                                    onClick={() => setIsOpen(false)}
                                >
                                    Faculty
                                </Link>
                            </motion.div>
                            <motion.div variants={menuItemVariants} className="pt-8">
                                <Link to="/contact" onClick={() => setIsOpen(false)} className="w-full flex justify-center">
                                    <Button size="lg" className="w-full max-w-xs rounded-none font-bold text-xl py-8 bg-primary text-white">
                                        Contact Us
                                    </Button>
                                </Link>
                            </motion.div>
                        </nav>
                    </motion.div>
                )}
            </AnimatePresence>

            <div className="flex-1 relative">
                <Outlet />
            </div>
            <Footer />
            <Toaster />
            <TanStackRouterDevtools />
        </div>
    )
}
