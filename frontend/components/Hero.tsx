'use client';
import { motion } from 'framer-motion';

export function Hero() {
    return (
        <div className="relative flex flex-col items-center justify-center py-20 z-10">
            <motion.div
                initial={{ opacity: 0, scale: 0.5 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.5 }}
                className="text-center"
            >
                <h1 className="text-6xl md:text-8xl font-bold tracking-tighter bg-clip-text text-transparent bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 drop-shadow-sm">
                    NicheForge
                </h1>
                <motion.p
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2, duration: 0.5 }}
                    className="mt-4 text-xl md:text-2xl text-slate-400 font-light"
                >
                    The Domain-Specific AI Builder
                </motion.p>
            </motion.div>
        </div>
    );
}
