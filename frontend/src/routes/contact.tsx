import { createFileRoute } from '@tanstack/react-router'
import { motion } from 'framer-motion'
import { Mail, MapPin, Phone, Send, Sparkles } from 'lucide-react'
import { ShimmerButton } from '@/components/ui/shimmer-button'
import { MagicCard } from '@/components/ui/magic-card'
import { Card, CardContent } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import * as z from "zod"
import { toast } from "sonner"
import * as React from "react"
import {
    Form,
    FormControl,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from "@/components/ui/form"

import { Turnstile } from '@marsidev/react-turnstile'

export const Route = createFileRoute('/contact')({
    component: ContactPage,
})

const formSchema = z.object({
    name: z.string().min(2, {
        message: "Name must be at least 2 characters.",
    }),
    email: z.string().email({
        message: "Please enter a valid email address.",
    }),
    subject: z.string().min(5, {
        message: "Subject must be at least 5 characters.",
    }),
    message: z.string().min(10, {
        message: "Message must be at least 10 characters.",
    }),
})

function ContactPage() {
    const [isLoading, setIsLoading] = React.useState(false)
    const [turnstileToken, setTurnstileToken] = React.useState<string | null>(null)
    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            name: "",
            email: "",
            subject: "",
            message: "",
        },
    })

    async function onSubmit(values: z.infer<typeof formSchema>) {
        setIsLoading(true)
        try {
            const response = await fetch(`${import.meta.env.VITE_API_URL || "http://localhost:8000"}/contact`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ ...values, turnstile_token: turnstileToken }),
            })

            const data = await response.json()

            if (!response.ok) {
                throw new Error(data.detail || 'Failed to send message')
            }

            toast.success("Message sent successfully!", {
                description: "We'll get back to you as soon as possible.",
            })
            form.reset()
        } catch (error) {
            console.error(error)
            toast.error("Failed to send message", {
                description: error instanceof Error ? error.message : "Please try again later.",
            })
        } finally {
            setIsLoading(false)
        }
    }

    return (
        <div className="min-h-[calc(100vh-4rem)] flex flex-col justify-center items-center relative overflow-hidden p-6 md:p-12">
            {/* Background Gradients */}
            <div className="absolute inset-0 pointer-events-none">
                <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-indigo-500/10 rounded-full blur-[100px] -translate-y-1/2 translate-x-1/2" />
                <div className="absolute bottom-0 left-0 w-[500px] h-[500px] bg-purple-500/10 rounded-full blur-[100px] translate-y-1/2 -translate-x-1/2" />
            </div>

            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6 }}
                className="w-full max-w-6xl z-10 grid grid-cols-1 lg:grid-cols-2 gap-12 items-start"
            >
                {/* Left Column: Header & Info */}
                <div className="space-y-8">
                    <div className="space-y-4">
                        <motion.div
                            initial={{ opacity: 0, scale: 0.9 }}
                            animate={{ opacity: 1, scale: 1 }}
                            transition={{ delay: 0.2 }}
                            className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 text-indigo-400 text-sm font-medium"
                        >
                            <Sparkles className="size-4" />
                            <span>Get in Touch</span>
                        </motion.div>
                        <h1 className="text-4xl md:text-5xl font-bold tracking-tight text-white">
                            Let's start a <span className="text-indigo-400">conversation.</span>
                        </h1>
                        <p className="text-zinc-400 text-lg leading-relaxed max-w-md">
                            Have questions about our predictive analysis platform? We're here to help you bridge the gap between curriculum and industry.
                        </p>
                    </div>

                    <div className="grid gap-6">
                        {[
                            { icon: Mail, label: 'Email', value: 'contact@dhekode.com', href: 'mailto:contact@dhekode.com' },
                            { icon: Phone, label: 'Phone', value: '+1 (555) 000-0000', href: 'tel:+15550000000' },
                            { icon: MapPin, label: 'Office', value: 'LSPU-SCC, Santa Cruz, Laguna', href: '#' },
                        ].map((item, index) => (
                            <motion.div
                                key={item.label}
                                initial={{ opacity: 0, x: -20 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ delay: 0.4 + index * 0.1 }}
                            >
                                <a href={item.href} className="group block cursor-pointer">
                                    <MagicCard
                                        className="flex items-center gap-6 p-6 border-white/5 bg-transparent"
                                        gradientColor="#6366f1"
                                        gradientOpacity={0.4}
                                    >
                                        <div className="text-indigo-400 transition-transform duration-300">
                                            <item.icon className="size-8 stroke-[1.5]" />
                                        </div>
                                        <div className="space-y-1">
                                            <div className="text-sm font-medium text-zinc-500 uppercase tracking-wider">{item.label}</div>
                                            <div className="text-lg font-semibold text-white group-hover:text-indigo-300 transition-colors">{item.value}</div>
                                        </div>
                                    </MagicCard>
                                </a>
                            </motion.div>
                        ))}
                    </div>
                </div>

                {/* Right Column: Contact Form */}
                <motion.div
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.4 }}
                >
                    <Card className="border-white/10 bg-black/40 backdrop-blur-xl">
                        <CardContent className="p-6 md:p-8">
                            <Form {...form}>
                                <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
                                    <div className="grid grid-cols-2 gap-4">
                                        <FormField
                                            control={form.control}
                                            name="name"
                                            render={({ field }) => (
                                                <FormItem>
                                                    <FormLabel className="text-zinc-400">Name</FormLabel>
                                                    <FormControl>
                                                        <Input placeholder="John Doe" className="bg-white/5 border-white/10 text-white placeholder:text-zinc-600 focus-visible:ring-indigo-500" {...field} />
                                                    </FormControl>
                                                    <FormMessage />
                                                </FormItem>
                                            )}
                                        />
                                        <FormField
                                            control={form.control}
                                            name="email"
                                            render={({ field }) => (
                                                <FormItem>
                                                    <FormLabel className="text-zinc-400">Email</FormLabel>
                                                    <FormControl>
                                                        <Input placeholder="john@example.com" className="bg-white/5 border-white/10 text-white placeholder:text-zinc-600 focus-visible:ring-indigo-500" {...field} />
                                                    </FormControl>
                                                    <FormMessage />
                                                </FormItem>
                                            )}
                                        />
                                    </div>
                                    <FormField
                                        control={form.control}
                                        name="subject"
                                        render={({ field }) => (
                                            <FormItem>
                                                <FormLabel className="text-zinc-400">Subject</FormLabel>
                                                <FormControl>
                                                    <Input placeholder="How can we help?" className="bg-white/5 border-white/10 text-white placeholder:text-zinc-600 focus-visible:ring-indigo-500" {...field} />
                                                </FormControl>
                                                <FormMessage />
                                            </FormItem>
                                        )}
                                    />
                                    <FormField
                                        control={form.control}
                                        name="message"
                                        render={({ field }) => (
                                            <FormItem>
                                                <FormLabel className="text-zinc-400">Message</FormLabel>
                                                <FormControl>
                                                    <Textarea placeholder="Tell us more about your inquiry..." className="min-h-[150px] bg-white/5 border-white/10 text-white placeholder:text-zinc-600 focus-visible:ring-indigo-500 resize-none" {...field} />
                                                </FormControl>
                                                <FormMessage />
                                            </FormItem>
                                        )}
                                    />

                                    <div className="flex justify-center py-2">
                                        <Turnstile
                                            siteKey="0x4AAAAAACI1nJJ80o6uCSuC"
                                            onSuccess={(token) => setTurnstileToken(token)}
                                            options={{ theme: 'dark' }}
                                        />
                                    </div>

                                    <ShimmerButton
                                        className="w-full text-foreground font-medium flex items-center justify-center gap-2 group disabled:opacity-50 disabled:cursor-not-allowed"
                                        background="var(--primary)"
                                        type="submit"
                                        disabled={isLoading || !turnstileToken}
                                    >
                                        {isLoading ? (
                                            <div className="flex items-center gap-2">
                                                <div className="h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
                                                <span>Sending...</span>
                                            </div>
                                        ) : (
                                            <>
                                                <span>Send Message</span>
                                                <Send className="size-4 group-hover:translate-x-1 transition-transform" />
                                            </>
                                        )}
                                    </ShimmerButton>
                                </form>
                            </Form>
                        </CardContent>
                    </Card>
                </motion.div>
            </motion.div>
        </div>
    )
}
