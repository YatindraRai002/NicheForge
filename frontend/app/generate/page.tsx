'use client';
import { Hero } from '@/components/Hero';
import { DatasetGenerator } from '@/components/DatasetGenerator';

export default function GeneratePage() {
    return (
        <main className="min-h-screen bg-black text-white selection:bg-purple-500/30 overflow-hidden flex flex-col items-center justify-start relative pt-20">
            {/* Background Ambience */}
            <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-slate-900 via-black to-black -z-10 pointer-events-none" />
            <div className="absolute top-0 right-1/4 translate-x-1/2 w-[800px] h-[400px] bg-indigo-500/10 rounded-full blur-3xl -z-10 pointer-events-none" />

            <div className="w-full max-w-7xl mx-auto flex flex-col items-center gap-8 px-4">
                {/* We can re-use Hero or make a smaller header */}
                <div className="text-center py-10">
                    <h1 className="text-4xl md:text-5xl font-bold tracking-tighter text-white mb-4">
                        Data Generation Pipeline
                    </h1>
                    <p className="text-slate-400 text-lg">
                        Turn your raw text documents into high-quality instruction datasets.
                    </p>
                </div>

                <DatasetGenerator />
            </div>
        </main>
    );
}
