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
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl shadow-2xl p-8 min-h-[500px]"
            >
                <div className="flex flex-col items-center justify-center p-8 border-2 border-dashed border-white/10 rounded-xl bg-black/20 hover:border-purple-500/50 transition-colors group relative cursor-pointer">
                    <input
                        type="file"
                        multiple
                        accept=".txt"
                        onChange={handleFileChange}
                        className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                    />
                    <Upload className="w-12 h-12 text-slate-500 group-hover:text-purple-400 mb-4 transition-colors" />
                    <p className="text-lg font-medium text-slate-300">
                        {files.length > 0 ? `${files.length} file(s) selected` : "Drop .txt files here or click to upload"}
                    </p>
                    <p className="text-sm text-slate-500 mt-2">Supports multiple text documents</p>
                </div>

                {files.length > 0 && (
                    <div className="mt-6 flex flex-col gap-2">
                        {files.map((f, i) => (
                            <div key={i} className="flex items-center gap-3 text-sm text-slate-400 bg-white/5 px-4 py-2 rounded-lg">
                                <FileText size={16} />
                                <span className="truncate">{f.name}</span>
                                <span className="ml-auto text-xs text-slate-600">{(f.size / 1024).toFixed(1)} KB</span>
                            </div>
                        ))}
                    </div>
                )}

                <div className="mt-8 flex justify-center">
                    <button
                        onClick={handleGenerate}
                        disabled={files.length === 0 || isLoading}
                        className={cn(
                            "flex items-center gap-2 px-8 py-4 rounded-xl font-bold text-lg transition-all",
                            files.length === 0
                                ? "bg-white/5 text-slate-600 cursor-not-allowed"
                                : "bg-gradient-to-r from-indigo-500 to-purple-600 text-white shadow-lg hover:shadow-purple-500/25 hover:scale-105 active:scale-95"
                        )}
                    >
                        {isLoading ? <Loader2 className="animate-spin" /> : <Database />}
                        {isLoading ? "Generating Dataset..." : "Start Generation"}
                    </button>
                </div>

                {/* Status & Results */}
                <div className="mt-8">
                    {status === 'error' && (
                        <div className="p-4 bg-red-500/10 border border-red-500/20 rounded-xl flex items-center gap-3 text-red-200">
                            <AlertCircle />
                            {message}
                        </div>
                    )}

                    {status === 'success' && result && (
                        <div className="space-y-6">
                            <div className="p-4 bg-green-500/10 border border-green-500/20 rounded-xl flex items-center gap-3 text-green-200">
                                <CheckCircle />
                                {message}
                            </div>

                            <div className="bg-black/40 rounded-xl p-6 border border-white/5 overflow-hidden">
                                <h3 className="text-lg font-semibold mb-4 text-slate-300">Preview (First 5 Pairs)</h3>
                                <pre className="text-xs text-slate-400 font-mono overflow-auto max-h-[400px]">
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
