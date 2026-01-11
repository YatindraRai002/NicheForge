'use client';
import { useState } from 'react';
import { motion } from 'framer-motion';
import { Upload, FileText, CheckCircle, AlertCircle, Loader2, Database } from 'lucide-react';
import { cn } from '@/libs/utils';

export function DatasetGenerator() {
    const [files, setFiles] = useState<File[]>([]);
    const [isLoading, setIsLoading] = useState(false);
    const [status, setStatus] = useState<'idle' | 'success' | 'error'>('idle');
    const [result, setResult] = useState<any>(null);
    const [message, setMessage] = useState('');

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files) {
            setFiles(Array.from(e.target.files));
            setStatus('idle');
            setResult(null);
        }
    };

    const handleGenerate = async () => {
        if (files.length === 0) return;

        setIsLoading(true);
        setStatus('idle');

        const formData = new FormData();
        files.forEach(file => {
            formData.append('files', file);
        });

        try {
            const res = await fetch('http://localhost:8000/generate', {
                method: 'POST',
                body: formData,
            });

            if (!res.ok) {
                const errData = await res.json();
                throw new Error(errData.detail || 'Generation failed');
            }

            const data = await res.json();
            setResult(data);
            setStatus('success');
            setMessage(data.message);
        } catch (error: any) {
            console.error(error);
            setStatus('error');
            setMessage(error.message || "An error occurred during generation.");
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="w-full max-w-4xl mx-auto px-4 pb-20 z-20">
            <motion.div
                initial={{ opacity: 0, scale: 0.98 }}
                animate={{ opacity: 1, scale: 1 }}
                className="bg-neutral-900/40 backdrop-blur-xl border border-white/10 rounded-3xl shadow-2xl p-8 min-h-[500px] ring-1 ring-white/5"
            >
                <div className="flex flex-col items-center justify-center p-12 border-2 border-dashed border-white/5 rounded-2xl bg-white/[0.02] hover:bg-white/[0.04] hover:border-purple-500/30 transition-all group relative cursor-pointer">
                    <input
                        type="file"
                        multiple
                        accept=".txt"
                        onChange={handleFileChange}
                        className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-50"
                    />
                    <div className="p-4 rounded-full bg-white/5 mb-4 group-hover:scale-110 transition-transform duration-300">
                        <Upload className="w-8 h-8 text-slate-400 group-hover:text-purple-400" />
                    </div>
                    <p className="text-xl font-medium text-slate-200 group-hover:text-purple-200 transition-colors">
                        {files.length > 0 ? `${files.length} file(s) selected` : "Drop text files here"}
                    </p>
                    <p className="text-sm text-slate-500 mt-2">Supports multiple .txt documents</p>
                </div>

                {files.length > 0 && (
                    <div className="mt-6 flex flex-col gap-2">
                        {files.map((f, i) => (
                            <div key={i} className="flex items-center gap-3 text-sm text-slate-300 bg-white/5 px-4 py-3 rounded-xl border border-white/5">
                                <FileText size={16} className="text-purple-400" />
                                <span className="truncate">{f.name}</span>
                                <span className="ml-auto text-xs text-slate-500 font-mono">{(f.size / 1024).toFixed(1)} KB</span>
                            </div>
                        ))}
                    </div>
                )}

                <div className="mt-8 flex justify-center">
                    <button
                        onClick={handleGenerate}
                        disabled={files.length === 0 || isLoading}
                        className={cn(
                            "flex items-center gap-2 px-8 py-4 rounded-2xl font-bold text-lg transition-all shadow-xl",
                            files.length === 0
                                ? "bg-white/5 text-slate-600 cursor-not-allowed"
                                : "bg-white text-black hover:bg-purple-50 hover:scale-[1.02] active:scale-[0.98]"
                        )}
                    >
                        {isLoading ? <Loader2 className="animate-spin" /> : <Database size={20} />}
                        {isLoading ? "Forging Dataset..." : "Generate Dataset"}
                    </button>
                </div>

                {/* Status & Results */}
                <div className="mt-8">
                    {status === 'error' && (
                        <div className="p-4 bg-red-500/10 border border-red-500/20 rounded-xl flex items-center gap-3 text-red-200 animate-fadeIn">
                            <AlertCircle />
                            {message}
                        </div>
                    )}

                    {status === 'success' && result && (
                        <div className="space-y-6 animate-fadeIn">
                            <div className="p-4 bg-green-500/10 border border-green-500/20 rounded-xl flex items-center gap-3 text-green-200">
                                <CheckCircle />
                                {message}
                            </div>

                            <div className="bg-black/40 rounded-xl p-6 border border-white/5 overflow-hidden ring-1 ring-white/5">
                                <h3 className="text-sm font-medium mb-4 text-slate-400 uppercase tracking-wider">Preview</h3>
                                <pre className="text-xs text-slate-300 font-mono overflow-auto max-h-[400px]">
                                    {JSON.stringify(result.preview, null, 2)}
                                </pre>
                            </div>
                        </div>
                    )}
                </div>

            </motion.div>
        </div>
    );
}
