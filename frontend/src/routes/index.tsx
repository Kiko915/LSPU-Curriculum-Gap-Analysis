import { createFileRoute, Link } from '@tanstack/react-router'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Brain, Briefcase, GraduationCap, Shield, Sparkles } from 'lucide-react'
import { motion } from 'framer-motion'
import { AnimatedShinyText } from '@/components/ui/animated-shiny-text'
import { ShimmerButton } from '@/components/ui/shimmer-button'
import { SolutionReveal } from '@/components/SolutionReveal'
import { HowItWorks } from '@/components/HowItWorks'
import { TeamSection } from '@/components/TeamSection'
import { ResearchPaperCTA } from '@/components/ResearchPaperCTA'

export const Route = createFileRoute('/')({
  component: Index,
})

import { useRef } from 'react'
import { AnimatedBeam } from '@/components/ui/animated-beam'

function Index() {
  const containerRef = useRef<HTMLDivElement>(null)
  const studentRef = useRef<HTMLDivElement>(null)
  const aiRef = useRef<HTMLDivElement>(null)
  const industryRef = useRef<HTMLDivElement>(null)

  const contentVariants = {
    initial: { opacity: 0 },
    in: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
        delayChildren: 0.2, // Wait for page transition a bit
      },
    },
  }

  const itemVariants = {
    initial: { opacity: 0, y: 20 },
    in: { opacity: 1, y: 0 },
  }

  return (
    <>
      <div
        className="container mx-auto max-w-6xl px-4 flex flex-col justify-center min-h-[calc(100vh-8rem)] overflow-x-hidden relative"
      >
        {/* Background Ambience */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[1000px] h-[600px] bg-indigo-600/20 rounded-full blur-[120px] -z-10 pointer-events-none mix-blend-screen" />
        <div className="absolute bottom-0 left-0 right-0 h-[400px] bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_0%,#000_70%,transparent_100%)] -z-10 pointer-events-none" />

        <motion.div
          variants={contentVariants}
          initial="initial"
          animate="in"
          className="w-full space-y-16 md:space-y-24 py-12 md:py-20"
        >
          {/* New Hero Section */}
          <motion.div variants={itemVariants} className="text-center space-y-8 relative">

            {/* Connected Icon Visual */}
            <div ref={containerRef} className="flex items-center justify-center gap-4 mb-12 relative w-full">
              <div className="relative z-10">
                <div ref={studentRef} className="size-12 rounded-full border border-white/10 bg-white/5 backdrop-blur-md flex items-center justify-center shadow-lg shadow-indigo-500/10">
                  <GraduationCap className="size-5 text-indigo-300" />
                </div>
              </div>

              {/* Spacer for Beam 1 */}
              <div className="w-16 md:w-32" />

              <div className="relative z-10">
                <div className="absolute inset-0 bg-indigo-500/20 blur-xl rounded-full" />
                <div ref={aiRef} className="size-16 rounded-2xl border border-indigo-400/30 bg-indigo-950/50 backdrop-blur-xl flex items-center justify-center relative shadow-[0_0_30px_-5px_rgba(99,102,241,0.3)]">
                  <Sparkles className="size-8 text-indigo-400 fill-indigo-400/20" />
                </div>
              </div>

              {/* Spacer for Beam 2 */}
              <div className="w-16 md:w-32" />

              <div className="relative z-10">
                <div ref={industryRef} className="size-12 rounded-full border border-white/10 bg-white/5 backdrop-blur-md flex items-center justify-center shadow-lg shadow-indigo-500/10">
                  <Briefcase className="size-5 text-indigo-300" />
                </div>
              </div>

              <AnimatedBeam
                containerRef={containerRef}
                fromRef={studentRef}
                toRef={aiRef}
                curvature={-20}
                endYOffset={0}
              />
              <AnimatedBeam
                containerRef={containerRef}
                fromRef={aiRef}
                toRef={industryRef}
                curvature={20}
                reverse
                startYOffset={0}
              />
            </div>

            <h1 className="text-5xl md:text-7xl font-bold tracking-tight text-white leading-[1.1] drop-shadow-sm">
              The intelligent way to <br />
              <AnimatedShinyText className="text-5xl md:text-7xl font-bold tracking-tight py-2 transition-ease-in-out">
                <span>align skills & industry</span>
              </AnimatedShinyText>
            </h1>

            <p className="max-w-2xl mx-auto text-lg md:text-xl text-indigo-200/80 font-normal leading-relaxed text-balance">
              DheKode utilizes a hybrid AI engine to predict student career paths and audit curriculum relevance in real-time.
            </p>

            <div className="flex justify-center">
              <Link to="/student">
                <ShimmerButton className="shadow-2xl">
                  <span className="whitespace-pre-wrap text-center text-sm font-medium leading-none tracking-tight lg:text-lg">
                    Get Started
                  </span>
                </ShimmerButton>
              </Link>
            </div>
          </motion.div>

          {/* Split Choice Grid */}
          <motion.div
            variants={itemVariants}
            className="grid md:grid-cols-2 gap-6 md:gap-8 max-w-4xl mx-auto w-full px-4"
          >
            {/* Student Card */}
            <Link to="/student" className="group">
              <Card className="h-full border border-white/10 hover:border-indigo-500/50 transition-all duration-300 cursor-pointer bg-black/40 backdrop-blur-md relative overflow-hidden active:scale-[0.98]">
                <div className="absolute inset-0 bg-indigo-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
                <CardHeader className="relative z-10 space-y-4 pb-4">
                  <div className="size-12 rounded-lg bg-indigo-500/10 flex items-center justify-center text-indigo-400 group-hover:scale-110 transition-transform duration-300 group-hover:bg-indigo-500/20">
                    <Brain className="size-6" />
                  </div>
                  <CardTitle className="text-xl md:text-2xl font-bold text-white group-hover:text-indigo-300 transition-colors">
                    Student Analyzer
                  </CardTitle>
                </CardHeader>
                <CardContent className="relative z-10">
                  <CardDescription className="text-sm md:text-base font-medium text-zinc-400 group-hover:text-zinc-300 transition-colors">
                    Discover your career fit based on your current skillset and predicted industry trends.
                  </CardDescription>
                </CardContent>
              </Card>
            </Link>

            {/* Faculty Card */}
            <Link to="/admin" className="group">
              <Card className="h-full border border-white/10 hover:border-indigo-500/50 transition-all duration-300 cursor-pointer bg-black/40 backdrop-blur-md relative overflow-hidden active:scale-[0.98]">
                <div className="absolute inset-0 bg-indigo-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
                <CardHeader className="relative z-10 space-y-4 pb-4">
                  <div className="size-12 rounded-lg bg-indigo-500/10 flex items-center justify-center text-indigo-400 group-hover:scale-110 transition-transform duration-300 group-hover:bg-indigo-500/20">
                    <Shield className="size-6" />
                  </div>
                  <CardTitle className="text-xl md:text-2xl font-bold text-white group-hover:text-indigo-300 transition-colors">
                    Curriculum Audit
                  </CardTitle>
                </CardHeader>
                <CardContent className="relative z-10">
                  <CardDescription className="text-sm md:text-base font-medium text-zinc-400 group-hover:text-zinc-300 transition-colors">
                    Analyze knowledge gaps, view skills analytics, and modify curriculum requirements.
                  </CardDescription>
                </CardContent>
              </Card>
            </Link>
          </motion.div>
        </motion.div>
      </div>

      {/* Problem Statement Section - Full Width */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.8 }}
        className="w-full relative border-y border-white/10 bg-white/5 backdrop-blur-md overflow-hidden py-16 md:py-24 text-center mt-12 md:mt-20"
      >
        <div className="absolute inset-0 bg-linear-to-br from-indigo-500/10 via-transparent to-purple-500/10" />

        <div className="relative z-10 max-w-4xl mx-auto px-4 space-y-6">
          <h2 className="text-3xl md:text-5xl font-bold tracking-tight bg-clip-text text-transparent bg-linear-to-r from-white via-indigo-200 to-white/80">
            Bridging the Skills Gap
          </h2>

          <p className="text-lg md:text-xl text-zinc-400 leading-relaxed max-w-3xl mx-auto">
            Current curriculums struggle to keep pace with the tech industry's evolution.
            We address the lack of data-driven curriculum assessment at LSPU College of Computer Studies to prevent
            talent shortages and ensure student employability.
          </p>
        </div>

      </motion.div >

      {/* The Solution - Scroll Reveal */}
      <SolutionReveal />

      {/* How It Works - Cards */}
      <HowItWorks />

      {/* Team Section */}
      <TeamSection />

      {/* Research Paper CTA */}
      <ResearchPaperCTA />
    </>
  )
}

