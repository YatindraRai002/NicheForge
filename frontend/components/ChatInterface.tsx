'use client';
import { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Bot, User, Loader2, Sparkles } from 'lucide-react';
import { cn } from '@/libs/utils';

type Message = {
    id: string;
    role: 'user' | 'assistant';
    content: string;
};

export function ChatInterface() {
    const [messages, setMessages] = useState<Message[]>([
        {
            id: 'welcome',
            role: 'assistant',
            content: "Hello! I'm ready to help you with your domain-specific tasks."
        }
    ]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const scrollRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
    }, [messages]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim() || isLoading) return;

        const userMessage: Message = {
            id: Date.now().toString(),
            role: 'user',
            content: input
        };

        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setIsLoading(true);

        try {
            const res = await fetch('http://localhost:8000/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: userMessage.content })
            });

            if (!res.ok) throw new Error('Failed to fetch response');

            const data = await res.json();

            const botMessage: Message = {
                id: (Date.now() + 1).toString(),
                role: 'assistant',
                content: data.response
            };

            setMessages(prev => [...prev, botMessage]);
        } catch (error) {
            console.error(error);
            setMessages(prev => [...prev, {
                id: Date.now().toString(),
                role: 'assistant',
                content: "Error: Could not connect to the AI backend."
            }]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="w-full max-w-5xl mx-auto px-4 pb-10 z-20 flex flex-col h-[70vh]">
            <div className="flex-1 overflow-y-auto space-y-6 pr-4 scrollbar-thin scrollbar-thumb-white/10 scrollbar-track-transparent" ref={scrollRef}>
                <AnimatePresence initial={false}>
                    {messages.map((msg) => (
                        <motion.div
                            key={msg.id}
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            className={cn(
                                "flex items-start gap-4",
                                msg.role === 'user' ? "flex-row-reverse" : "flex-row"
                            )}
                        >
                            <div className={cn(
                                "w-10 h-10 rounded-full flex items-center justify-center shrink-0 shadow-lg border border-white/10",
                                msg.role === 'user' ? "bg-purple-600" : "bg-neutral-800"
                            )}>
                                {msg.role === 'user' ? <User size={18} className="text-white" /> : <Bot size={18} className="text-purple-400" />}
                            </div>

                            <div className={cn(
                                "p-4 rounded-2xl max-w-[85%] text-sm md:text-base leading-relaxed shadow-sm",
                                msg.role === 'user'
                                    ? "bg-purple-600 text-white rounded-tr-sm"
                                    : "bg-neutral-900/80 backdrop-blur-md border border-white/5 text-slate-200 rounded-tl-sm"
                            )}>
                                <p className="whitespace-pre-wrap">{msg.content}</p>
                            </div>
                        </motion.div>
                    ))}
                </AnimatePresence>

                {isLoading && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        className="flex items-center gap-3 ml-1"
                    >
                        <div className="w-8 h-8 rounded-full bg-neutral-800 flex items-center justify-center border border-white/10">
                            <Sparkles size={14} className="text-purple-400 animate-pulse" />
                        </div>
                        <div className="text-slate-500 text-sm animate-pulse font-medium">Thinking...</div>
                    </motion.div>
                )}
            </div>

            {/* Floating Input Area */}
            <div className="mt-6 sticky bottom-6">
                <form onSubmit={handleSubmit} className="relative max-w-4xl mx-auto">
                    <div className="relative overflow-hidden rounded-2xl bg-neutral-900/50 backdrop-blur-xl border border-white/10 shadow-2xl ring-1 ring-white/5 focus-within:ring-purple-500/50 transition-all">
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            placeholder="Message NicheForge AI..."
                            className="w-full bg-transparent text-white placeholder-slate-500 py-4 pl-6 pr-16 text-lg outline-none"
                            autoFocus
                        />
                        <button
                            type="submit"
                            disabled={isLoading || !input.trim()}
                            className="absolute right-2 top-1/2 -translate-y-1/2 p-2.5 bg-white text-black rounded-xl hover:bg-purple-50 disabled:opacity-50 disabled:hover:bg-white disabled:cursor-not-allowed transition-all"
                        >
                            {isLoading ? <Loader2 size={20} className="animate-spin" /> : <Send size={20} className="ml-0.5" />}
                        </button>
                    </div>
                    <div className="text-center mt-2 text-xs text-slate-600">
                        AI can make mistakes. Check important info.
                    </div>
                </form>
            </div>
        </div>
    );
}
