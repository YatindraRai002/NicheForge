'use client';
import { Hero } from '@/components/Hero';
import { ChatInterface } from '@/components/ChatInterface';

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-start relative pt-20">
      <div className="w-full max-w-7xl mx-auto flex flex-col items-center gap-8 px-4">
        <Hero />
        <ChatInterface />
      </div>
    </main>
  );
}
