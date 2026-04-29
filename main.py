import os
import logging
import asyncio
import google.generativeai as genai
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv

# .env faylidan ma'lumotlarni yuklash
load_dotenv()

# Tokenlarni xavfsiz tarzda olish
TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini AI ni sozlash
genai.configure(api_key=GEMINI_API_KEY)
logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Ishlaydigan modelni avtomatik aniqlash
def get_working_model():
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_methods]
        for preferred in ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-pro']:
            if preferred in available_models:
                return genai.GenerativeModel(preferred)
        return genai.GenerativeModel(available_models[0])
    except:
        return genai.GenerativeModel('gemini-1.5-flash')

model = get_working_model()

@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Salom! Men xavfsiz va aqlli AI yordamchingizman. Nima yordam kerak?")

@dp.message()
async def chat_handler(message: Message):
    msg = await message.answer("O'ylayapman...")
    try:
        response = model.generate_content(f"Javobni o'zbek tilida ber: {message.text}")
        await msg.edit_text(response.text, parse_mode="Markdown")
    except Exception as e:
        await msg.edit_text(f"Xatolik: {str(e)}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
