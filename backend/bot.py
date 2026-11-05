import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from backend.config import settings
from backend.services.query_parser import QueryParser
from backend.services.metadata_service import MetadataService
from backend.services.stream_fetcher import StreamFetcher

logging.basicConfig(level=logging.INFO)
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN) if settings.TELEGRAM_BOT_TOKEN else None
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.reply(
        "👋 مرحباً بك في بوت التنزيل والبث الفوري!\n\n"
        "أرسل اسم الفيلم أو الأنمي أو رقم الحلقة التي تبحث عنها، وسنقوم بتجهيز رابط البث والتحميل فورياً.\n"
        "مثال:\n"
        "• `ون بيس حلقة 1071`\n"
        "• `هجوم العمالقة الموسم 4 حلقة 5`\n"
        "• `فيلم Inception`",
        parse_mode="Markdown"
    )

@dp.message()
async def handle_search(message: types.Message):
    query = message.text.strip()
    parsed = QueryParser.parse(query)
    
    await message.reply(f"🔍 جاري البحث عن: *{parsed.title}* (الموسم {parsed.season} - الحلقة {parsed.episode})...", parse_mode="Markdown")
    
    # Resolve Streams
    options = await StreamFetcher.resolve_streams(
        canonical_id=parsed.title.replace(" ", "_").lower(),
        season=parsed.season or 1,
        episode=parsed.episode or 1
    )
    
    keyboard = []
    for opt in options:
        keyboard.append([
            InlineKeyboardButton(text=f"⬇️ تحميل ({opt.quality})", url=opt.direct_download_url),
            InlineKeyboardButton(text=f"▶️ مشاهدة ({opt.quality})", url=opt.stream_url)
        ])
        
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    await message.reply(
        f"🎬 *{parsed.title}* (الحلقة {parsed.episode})\n"
        f"اختر جودة التحميل أو البث المباشر أدناه:",
        reply_markup=markup,
        parse_mode="Markdown"
    )

async def main():
    if not bot:
        logging.warning("TELEGRAM_BOT_TOKEN is not set. Bot polling aborted.")
        return
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
