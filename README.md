# 🎬 Instant Media Streamer & Downloader (منصة البث والتنزيل الفوري)

منصة متكاملة وعالية السرعة للبحث عن وتحميل وبث أي حلقة أنمي، مسلسل، أو فيلم مترجم فورياً بالاعتماد على معمارية الفهرسة الذكية (Intelligent Indexing & Caching Architecture)، وتكامل واجهات TMDB / Jikan، ومحركات البث المباشر عبر تيليجرام ومواقع المشاهدة.

---

## 🌟 مميزات المنصة (Key Features)

1. **محلل الطلبات الذكي (Intelligent Query Parser):**
   - استخراج اسم العمل، رقم الموسم، ورقم الحلقة بدقة من نصوص البحث باللغتين العربية والإنجليزية (مثل: `"ون بيس 1071"`, `"هجوم العمالقة الموسم 4 الحلقة 5"`, `"Inception 1080p"`).

2. **فهرسة البيانات الوصفية (Metadata Enrichment):**
   - ربط تلقائي مع واجهات **TMDB API** (للأفلام والمسلسلات) و **Jikan / AniList API** (للأنمي) لجلب البوسترات، العناوين الرسمية، وتفاصيل الحلقات.

3. **محرك البث والتخزين السحابي الفوري (Zero-Storage Stream Engine):**
   - ربط ملفات التيليجرام السحابية (TG-FileStreamBot) لتوفير روابط بث وتحميل مباشرة بسرعات عالية وبدون تكلفة استضافة تخزين ضخمة.

4. **تخزين مؤقت عالي الأداء (High-Performance Caching):**
   - استخدام **Redis** و **PostgreSQL** للاستجابة اللحظية (<1 ثانية) للطلبات المتكررة.

5. **واجهة مستخدم عصرية (Modern Web UI & Telegram Bot):**
   - واجهة Next.js سريعة وتدعم اللغة العربية والوضع الليلي (Dark Mode) مع شريط بحث تفاعلي.
   - بوت تيليجرام (Aiogram) متكامل للتنزيل المباشر أو استخراج الروابط.

---

## 📐 معمارية النظام (System Architecture)

```
[User / Client] (Web UI / Telegram Bot)
       │
       ▼
[FastAPI Gateway & Query Parser] ────► [TMDB & Jikan APIs] (Metadata)
       │
       ├──► [Redis Cache] (Response < 1s)
       │
       ├──► [PostgreSQL Database] (Indexed Links & History)
       │
       └──► [Stream / Scraper Engine]
                 │
                 ├──► Telegram Cloud Streamer (Pyrogram/TG-FileStream)
                 └──► Web Scrapers (Direct Mediafire / MP4 Links)
```

---

## 🚀 البدء السريع (Quickstart with Docker)

```bash
# 1. استنساخ المستودع
git clone https://github.com/mhommdkuyr/instant-media-streamer.git
cd instant-media-streamer

# 2. إعداد المتغيرات البيئية
cp .env.example .env

# 3. تشغيل الحاويات بالكامل
docker-compose up --build -d
```

- **الواجهة الأمامية (Frontend):** `http://localhost:3000`
- **التوثيق التفاعلي للـ API:** `http://localhost:8000/docs`

---

## 📜 الترخيص (License)
MIT License.
