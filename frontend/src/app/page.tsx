'use client';

import React, { useState } from 'react';
import { Search, Play, Download, Film, Tv, Sparkles } from 'lucide-react';

interface StreamOption {
  quality: string;
  direct_download_url: string;
  stream_url: string;
  source: string;
  is_cached: boolean;
}

export default function Home() {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [options, setOptions] = useState<StreamOption[]>([]);
  const [parsedInfo, setParsedInfo] = useState<any>(null);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setOptions([]);
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      
      // Parse query
      const parseRes = await fetch(`${apiUrl}/api/v1/parse?q=${encodeURIComponent(query)}`);
      const parseData = await parseRes.json();
      setParsedInfo(parseData);

      // Get stream options
      const streamRes = await fetch(
        `${apiUrl}/api/v1/stream/${encodeURIComponent(parseData.title.toLowerCase())}?season=${parseData.season || 1}&episode=${parseData.episode || 1}`
      );
      const streamData = await streamRes.json();
      setOptions(streamData);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main dir="rtl" className="min-h-screen bg-slate-950 text-slate-100 flex flex-col items-center p-6">
      <header className="w-full max-w-4xl flex items-center justify-between py-6">
        <div className="flex items-center gap-2">
          <Film className="w-8 h-8 text-amber-500" />
          <h1 className="text-2xl font-bold tracking-tight">بث وتنزيل فوري</h1>
        </div>
        <span className="text-xs px-3 py-1 bg-slate-800 text-slate-400 rounded-full border border-slate-700">
          V1.0 High-Speed CDN
        </span>
      </header>

      <section className="w-full max-w-2xl mt-16 text-center">
        <h2 className="text-4xl font-extrabold mb-3">
          ابحث عن أي <span className="text-amber-500">أنمي</span> أو <span className="text-indigo-400">فيلم</span>
        </h2>
        <p className="text-slate-400 mb-8">
          اكتب اسم العمل ورقم الحلقة أو الموسم لتحصل على رابط البث والتحميل فورياً بدون إعلانات.
        </p>

        <form onSubmit={handleSearch} className="relative flex items-center">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="مثال: ون بيس 1071، هجوم العمالقة الموسم 4 حلقة 5..."
            className="w-full bg-slate-900 border border-slate-700 rounded-2xl py-4 pr-12 pl-32 text-lg focus:outline-none focus:ring-2 focus:ring-amber-500 transition-all text-slate-100 placeholder-slate-500"
          />
          <Search className="absolute right-4 w-6 h-6 text-slate-500" />
          <button
            type="submit"
            disabled={loading}
            className="absolute left-3 bg-amber-500 hover:bg-amber-600 disabled:opacity-50 text-slate-950 font-bold px-6 py-2 rounded-xl transition-all flex items-center gap-2"
          >
            {loading ? 'جاري البحث...' : 'تجهيز الرابط'}
          </button>
        </form>
      </section>

      {parsedInfo && (
        <div className="w-full max-w-2xl mt-8 p-4 bg-slate-900/60 rounded-xl border border-slate-800 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Sparkles className="w-5 h-5 text-amber-400" />
            <div>
              <span className="text-xs text-slate-400">الطلب المكتشف:</span>
              <p className="font-semibold text-slate-200">
                {parsedInfo.title} • الموسم {parsedInfo.season} • الحلقة {parsedInfo.episode}
              </p>
            </div>
          </div>
          <span className="text-xs bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 px-2.5 py-1 rounded-md">
            جاهز للبث فورياً
          </span>
        </div>
      )}

      {options.length > 0 && (
        <section className="w-full max-w-2xl mt-6 space-y-3">
          <h3 className="text-sm font-medium text-slate-400">خيارات التحميل والمشاهدة المتوفرة:</h3>
          {options.map((opt, idx) => (
            <div
              key={idx}
              className="p-4 bg-slate-900 border border-slate-800 rounded-xl flex items-center justify-between hover:border-slate-700 transition"
            >
              <div>
                <span className="font-bold text-slate-100">{opt.quality}</span>
                <p className="text-xs text-slate-500">{opt.source}</p>
              </div>
              <div className="flex gap-2">
                <a
                  href={opt.stream_url}
                  target="_blank"
                  rel="noreferrer"
                  className="flex items-center gap-1.5 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-medium rounded-lg transition"
                >
                  <Play className="w-4 h-4" /> مشاهدة
                </a>
                <a
                  href={opt.direct_download_url}
                  target="_blank"
                  rel="noreferrer"
                  className="flex items-center gap-1.5 px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white text-sm font-medium rounded-lg transition"
                >
                  <Download className="w-4 h-4" /> تحميل
                </a>
              </div>
            </div>
          ))}
        </section>
      )}
    </main>
  );
}
