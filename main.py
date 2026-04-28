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
model = genai.GenerativeModel('gemini-pro')

# Logging (Xatoliklarni terminalda ko'rish uchun)
logging.basicConfig(level=logging.INFO)

# Bot va Dispatcher obyektlarini yaratish
bot = Bot(token=TOKEN)
dp = Dispatcher()

# /start buyrug'i uchun handler
@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "Salom! Men sizning mukammal AI yordamchingizman.\n\n"
        "Men Google Gemini AI yordamida ishlayman va quyidagilarni qila olaman:\n"
        "1. 💻 Murakkab kodlar yozish\n"
        "2. 💡 G'oyalaringizni loyihalarga aylantirish\n"
        "3. 📝 Har qanday savolga javob berish\n"
        "4. 🌍 O'zbek tilida mukammal muloqot qilish\n\n"
        "Nima yordam kerak? Shunchaki yozing!"
    )

# Barcha matnli xabarlar uchun handler (AI bilan muloqot)
@dp.message()
async def chat_handler(message: Message):
    # Foydalanuvchiga kutish xabarini yuborish
    msg = await message.answer("O'ylayapman...")
    
    try:
        # Gemini-ga yuboriladigan ko'rsatma (System Prompt)
        prompt = (
            f"Sen aqlli, yordam berishga tayyor va mukammal dasturchi AI yordamchisan. "
            f"Foydalanuvchiga kod yozishda, g'oyalarni shakllantirishda va savollarga javob berishda yordam berasan. "
            f"Javoblaringni o'zbek tilida ber. Foydalanuvchi so'rovi: {message.text}"
        )
        
        # AI dan javob olish
        response = model.generate_content(prompt)
        answer = response.text
        
        # Telegramda xabar uzunligi cheklangan (4096 belgi)
        if len(answer) > 4000:
            for i in range(0, len(answer), 4000):
                await message.answer(answer[i:i+4000], parse_mode="Markdown")
            await msg.delete()
        else:
            # Javobni foydalanuvchiga yuborish (Markdown formatida)
            await msg.edit_text(answer, parse_mode="Markdown")
            
    except Exception as e:
        logging.error(f"Xatolik yuz berdi: {e}")
        await msg.edit_text("Kechirasiz, javob tayyorlashda xatolik yuz berdi. Iltimos, birozdan so'ng qayta urinib ko'ring.")

# Botni ishga tushirish funksiyasi
async def main():
    print("--- Bot muvaffaqiyatli ishga tushdi ---")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("--- Bot to'xtatildi ---")
        
