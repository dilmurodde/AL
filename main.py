import os
import logging
import asyncio
import google.generativeai as genai
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message

# ==========================================
# SOZLAMALAR (TOKENLAR KOD ICHIGA JOYLANDI)
# ==========================================
TOKEN = "8670543048:AAFw3ZgKX99s0XjFtRF03hWY7LfdTbu6E9A"
GEMINI_API_KEY = "AIzaSyBp9lxZNDKZFf6VcuTR_BnF7u56hwFxNCc"

# Gemini AI ni sozlash
genai.configure(api_key=GEMINI_API_KEY)

# DIQQAT: Bu yerda model nomini 'gemini-1.5-flash' ga o'zgartirdik
# Bu model hozirda eng barqaror va bepul versiya hisoblanadi
model = genai.GenerativeModel('gemini-1.5-flash')

# Logging
logging.basicConfig(level=logging.INFO)

# Bot va Dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "Salom! Men yangilangan Gemini 1.5 Flash yordamida ishlaydigan AI yordamchingizman.\n\n"
        "Men quyidagilarni qila olaman:\n"
        "1. 💻 Murakkab kodlar yozish\n"
        "2. 💡 G'oyalarni loyihalarga aylantirish\n"
        "3. 📝 Har qanday savolga javob berish\n"
        "4. 🌍 O'zbek tilida mukammal muloqot qilish\n\n"
        "Nima yordam kerak?"
    )

@dp.message()
async def chat_handler(message: Message):
    msg = await message.answer("O'ylayapman...")
    
    try:
        # Gemini-ga yuboriladigan ko'rsatma
        prompt = (
            f"Sen aqlli, yordam berishga tayyor va mukammal dasturchi AI yordamchisan. "
            f"Foydalanuvchiga kod yozishda, g'oyalarni shakllantirishda va savollarga javob berishda yordam berasan. "
            f"Javoblaringni o'zbek tilida ber. Foydalanuvchi so'rovi: {message.text}"
        )
        
        # AI dan javob olish
        response = model.generate_content(prompt)
        answer = response.text
        
        if len(answer) > 4000:
            for i in range(0, len(answer), 4000):
                await message.answer(answer[i:i+4000], parse_mode="Markdown")
            await msg.delete()
        else:
            # MarkdownV2 o'rniga oddiy Markdown ishlatamiz, xatolik kamroq bo'lishi uchun
            await msg.edit_text(answer, parse_mode="Markdown")
            
    except Exception as e:
        logging.error(f"Xatolik yuz berdi: {e}")
        # Agar model hali ham topilmasa, xatolikni aniqroq ko'rsatamiz
        await msg.edit_text(f"Xatolik yuz berdi. Iltimos, API kalitingiz Gemini 1.5 modelini qo'llab-quvvatlashini tekshiring.\n\nTexnik xatolik: {str(e)}")

async def main():
    print("--- Bot yangilangan model bilan ishga tushdi ---")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("--- Bot to'xtatildi ---")
        
