'use client';
import { Hero } from '@/components/Hero';
import { ChatInterface } from '@/components/ChatInterface';

export default function Home() {
  return (
    <main className="min-h-screen bg-black text-white selection:bg-purple-500/30 overflow-hidden flex flex-col items-center justify-start relative">
      {/* Background Ambience */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-slate-900 via-black to-black -z-10 pointer-events-none" />
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[1000px] h-[500px] bg-purple-500/10 rounded-full blur-3xl -z-10 pointer-events-none" />

      <div className="w-full max-w-7xl mx-auto flex flex-col items-center gap-8 px-4">
        <Hero />
        <ChatInterface />
      </div>
    </main>
  );
}
