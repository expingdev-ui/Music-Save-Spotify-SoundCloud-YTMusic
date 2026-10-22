import asyncio
import logging
import os
import re
import urllib.request
import json
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from yt_dlp import YoutubeDL

logging.basicConfig(level=logging.INFO)

TOKEN = "8727094689:AAHlR8qMqRW-DlHO89W_axjOuwTS8zWEJUI"
ADMIN_USERNAME = "exping"

bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_spotify_track_name(url: str) -> str:
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            

        match_title = re.search(r'<meta property="og:title" content="([^"]+)"', html)
        if match_title:
            title = match_title.group(1)
            title = title.split('|')[0].strip()
            return title
    except Exception as e:
        logging.error(f"Не удалось распарсить Spotify страницу: {e}")
    return None


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="ℹ️ О Программе", 
        callback_data="about_menu"
    ))
    
    text = (
        "✨ **Привет! Я твой музыкальный помощник.**\n\n"
        "🎵 Отправь мне ссылку на трек, и я быстро подготовлю для тебя **MP3** файл.\n\n"
        "**Поддерживаемые платформы:**\n"
        "• 🟢 Spotify\n"
        "• 🟠 SoundCloud\n"
        "• 🔴 YouTube Music"
    )
    
    await message.answer(text, reply_markup=builder.as_markup(), parse_mode="Markdown")


@dp.callback_query(F.data == "about_menu")
async def show_about(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="🔙 Вернуться обратно", 
        callback_data="back_to_main"
    ))
    
    about_text = (
        "🤖 **О Программе**\n\n"
        "Привет потребитель!\n"
        "Это Telegram-Bot для скачивания музыки с различных музыкальных площадок по URL-ссылке.\n"
        "Бот поддерживает: Spotify, SoundCloud, Youtube Music.\n\n"
        f"👑 **Владелец:** @{ADMIN_USERNAME}"
    )
    
    await callback.message.edit_text(about_text, reply_markup=builder.as_markup(), parse_mode="Markdown")
    await callback.answer()


@dp.callback_query(F.data == "back_to_main")
async def back_to_main(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="ℹ️ О Программе", 
        callback_data="about_menu"
    ))
    
    text = (
        "✨ **Привет! Я твой музыкальный помощник.**\n\n"
        "🎵 Отправь мне ссылку на трек, и я быстро подготовлю для тебя **MP3** файл.\n\n"
        "**Поддерживаемые платформы:**\n"
        "• 🟢 Spotify\n"
        "• 🟠 SoundCloud\n"
        "• 🔴 YouTube Music"
    )
    
    await callback.message.edit_text(text, reply_markup=builder.as_markup(), parse_mode="Markdown")
    await callback.answer()


@dp.message(F.text)
async def handle_url(message: types.Message):
    url = message.text.strip()
    
    if not re.match(r'^https?://', url):
        await message.answer("Пожалуйста, отправь корректную URL-ссылку.")
        return

    status_msg = await message.answer("⏳ Скачиваю трек, подождите...")
    file_path = None

    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': '%(title)s.%(ext)s',
            'restrictfilenames': True,
            'noplaylist': True,
            'extractor_args': {'youtube': {'player_client': ['android']}},
        }

        search_query = url

        
        if "spotify.com" in url:
            await status_msg.edit_text("🔍 Распознаю трек со Spotify...")
            track_info = await asyncio.to_thread(get_spotify_track_name, url)
            if track_info:
                search_query = f"ytsearch1:{track_info}"
            else:
                await status_msg.edit_text("❌ Не удалось получить информацию о треке со Spotify.")
                return

        def download_media():
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(search_query, download=True)
                if 'entries' in info:
                    info = info['entries'][0]
                path = ydl.prepare_filename(info)
                return os.path.splitext(path)[0] + '.mp3'

        file_path = await asyncio.to_thread(download_media)

       
        if file_path and os.path.exists(file_path):
            audio = FSInputFile(file_path)
            await message.answer_audio(audio=audio, caption="🎧 Вот твоя музыка!")
            await status_msg.delete()
        else:
            await status_msg.edit_text("❌ Не удалось получить файл.")

    except Exception as e:
        logging.error(f"Ошибка при скачивании: {e}")
        await status_msg.edit_text(f"❌ Произошла ошибка при скачивании трека: {str(e)}")

    finally:
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                logging.error(f"Ошибка удаления файла: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())