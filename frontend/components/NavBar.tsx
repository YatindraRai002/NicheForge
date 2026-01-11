'use client';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/libs/utils';
import { MessageSquare, Database } from 'lucide-react';

export function NavBar() {
    const pathname = usePathname();

    return (
        <nav className="fixed top-0 left-0 right-0 z-50 flex justify-center py-6 pointer-events-none">
            <div className="bg-white/5 backdrop-blur-md border border-white/10 rounded-full px-2 py-2 pointer-events-auto flex items-center gap-2 shadow-2xl">
                <Link href="/" className={cn(
                    "flex items-center gap-2 px-6 py-2 rounded-full transition-all duration-300 text-sm font-medium",
                    pathname === '/'
                        ? "bg-purple-600 text-white shadow-lg shadow-purple-500/25"
                        : "text-slate-400 hover:text-white hover:bg-white/5"
                )}>
                    <MessageSquare size={16} />
                    <span>Chat</span>
                </Link>
                <Link href="/generate" className={cn(
                    "flex items-center gap-2 px-6 py-2 rounded-full transition-all duration-300 text-sm font-medium",
                    pathname === '/generate'
                        ? "bg-purple-600 text-white shadow-lg shadow-purple-500/25"
                        : "text-slate-400 hover:text-white hover:bg-white/5"
                )}>
                    <Database size={16} />
                    <span>Data Gen</span>
                </Link>
            </div>
        </nav>
    );
}
