'use client';

export function Background() {
    return (
        <div className="fixed inset-0 -z-50 overflow-hidden pointer-events-none">
            {/* Deep Dark Gradient */}
            <div className="absolute inset-0 bg-neutral-950" />

            {/* Subtle Gradient Spots */}
            <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-purple-900/10 rounded-full blur-[128px] animate-pulse-slow" />
            <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-indigo-900/10 rounded-full blur-[128px] animate-pulse-slow" style={{ animationDelay: '2s' }} />

            {/* Grid Pattern */}
            <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_0%,#000_70%,transparent_100%)]" />
        </div>
    );
}
