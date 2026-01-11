'use client';
import { motion } from 'framer-motion';

export function Hero() {
    return (
        <div className="relative flex flex-col items-center justify-center py-16 z-10 w-full max-w-4xl mx-auto">
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, ease: "easeOut" }}
                className="text-center space-y-4"
            >
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/10 text-xs font-medium text-purple-300 mb-4 animate-fadeIn">
                    <span>✨ Domain-Specific AI Builder</span>
                </div>

                <h1 className="text-5xl md:text-7xl font-bold tracking-tight text-white leading-[1.1]">
                    Build AI that knows <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400">your niche.</span>
                </h1>

                <p className="text-lg md:text-xl text-slate-400 font-light max-w-2xl mx-auto leading-relaxed">
                    Create, train, and deploy specialized language models with your own data in minutes, not months.
                </p>
            </motion.div>
        </div>
    );
}
