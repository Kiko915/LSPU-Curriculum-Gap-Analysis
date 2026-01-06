import { motion } from 'framer-motion';
import { Github } from 'lucide-react';

const teamMembers = [
    {
        name: "Francis Neil Mistica",
        role: "Researcher",
        image1: "/team_members/kiko-1.png",
        image2: "/team_members/kiko-2.png",
        github: "https://github.com/Kiko915"
    },
    {
        name: "Ian Patrick Mesias",
        role: "Researcher",
        image1: "/team_members/ian-1.jpg",
        image2: "/team_members/ian-2.jpg",
        github: "https://github.com"
    },
    {
        name: "Dheyn Michael Orlanda",
        role: "Researcher",
        image1: "/team_members/Orlanda_Dheyn_AI.png",
        image2: "/team_members/Orlanda_Dheyn_AI.png",
        github: "https://github.com"
    }
];

export function TeamSection() {
    return (
        <section className="py-32 bg-[#030303] text-white relative overflow-hidden">
            {/* Gradient Backgrounds */}
            <div className="absolute inset-0 pointer-events-none">
                <div className="absolute top-[10%] left-[30%] w-[600px] h-[600px] bg-blue-600/5 rounded-full blur-[120px]" />
                <div className="absolute bottom-[10%] right-[10%] w-[500px] h-[500px] bg-indigo-600/5 rounded-full blur-[100px]" />
            </div>

            <div className="container mx-auto px-4 relative z-10">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    className="text-center mb-20"
                >
                    <h2 className="text-3xl md:text-5xl font-bold mb-6">
                        Meet the <span className="text-blue-500">Minds</span>
                    </h2>
                    <p className="text-zinc-400 max-w-2xl mx-auto text-lg">
                        The architects behind the A.S.P.I.R.E ecosystem.
                    </p>
                </motion.div>

                <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
                    {teamMembers.map((member, index) => (
                        <motion.div
                            key={index}
                            initial={{ opacity: 0, y: 30 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                            transition={{ delay: index * 0.1, duration: 0.5 }}
                            className="group relative rounded-3xl overflow-hidden bg-white/5 border border-white/10"
                        >
                            {/* Card Glow Effect */}
                            <div className="absolute inset-0 bg-gradient-to-tr from-blue-500/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none z-10" />

                            {/* Image Container */}
                            <div className="aspect-[3/4] relative overflow-hidden">
                                {/* Secondary Image (Zoom effect) */}
                                <img
                                    src={member.image2}
                                    alt={`${member.name} fun`}
                                    className="absolute inset-0 w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
                                />

                                {/* Primary Image (Fades out) */}
                                <img
                                    src={member.image1}
                                    alt={`${member.name} professional`}
                                    className="absolute inset-0 w-full h-full object-cover transition-opacity duration-500 group-hover:opacity-0"
                                />

                                {/* Overlay Gradient for Text Readability */}
                                <div className="absolute inset-0 bg-gradient-to-t from-[#030303] via-transparent to-transparent opacity-80" />

                                {/* Content Overlay (Positioned at bottom) */}
                                <div className="absolute bottom-0 left-0 w-full p-6 z-20 translate-y-6 group-hover:translate-y-0 transition-transform duration-500">
                                    <h3 className="text-xl md:text-2xl font-bold mb-1 text-white group-hover:text-blue-200 transition-colors">
                                        {member.name}
                                    </h3>
                                    <p className="text-blue-200/80 font-medium text-sm md:text-base mb-3">
                                        {member.role}
                                    </p>

                                    {/* Social Icon Row */}
                                    <div className="flex gap-4 opacity-0 group-hover:opacity-100 transition-all duration-300 transform translate-y-4 group-hover:translate-y-0">
                                        <a
                                            href={member.github}
                                            target="_blank"
                                            rel="noreferrer"
                                            className="p-2 bg-white/10 backdrop-blur-md rounded-full hover:bg-white hover:text-black transition-all border border-white/10"
                                        >
                                            <Github className="w-4 h-4" />
                                        </a>
                                    </div>
                                </div>
                            </div>
                        </motion.div>
                    ))}
                </div>
            </div>
        </section>
    );
}
