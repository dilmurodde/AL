import os
import logging
import asyncio
import google.generativeai as genai
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message

# ==========================================
# SOZLAMALAR
# ==========================================
TOKEN = "8670543048:AAFw3ZgKX99s0XjFtRF03hWY7LfdTbu6E9A"
GEMINI_API_KEY = "AIzaSyBp9lxZNDKZFf6VcuTR_BnF7u56hwFxNCc"

# Logging
logging.basicConfig(level=logging.INFO)

# Gemini AI ni sozlash
genai.configure(api_key=GEMINI_API_KEY)

# Bot va Dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Ishlaydigan modelni avtomatik aniqlash
def get_working_model():
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_methods]
        if available_models:
            # Eng yaxshi modellarni tartib bilan qidiramiz
            for preferred in ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-pro']:
                if preferred in available_models:
                    logging.info(f"Tanlangan model: {preferred}")
                    return genai.GenerativeModel(preferred)
            # Agar afzal ko'rilganlar bo'lmasa, birinchisini olamiz
            logging.info(f"Avtomatik tanlangan model: {available_models[0]}")
            return genai.GenerativeModel(available_models[0])
    except Exception as e:
        logging.error(f"Modellarni olishda xatolik: {e}")
    return genai.GenerativeModel('gemini-pro') # Oxirgi chora

model = get_working_model()

@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "Salom! Men sizning aqlli AI yordamchingizman.\n"
        "Men hozirgina tizimingizdagi eng mos modelni aniqlab, ishga tushdim.\n\n"
        "Nima yordam kerak? Shunchaki yozing!"
    )

@dp.message()
async def chat_handler(message: Message):
    msg = await message.answer("O'ylayapman...")
    
    try:
        # Gemini-ga so'rov yuborish
        prompt = (
            f"Sen aqlli dasturchi AI yordamchisan. Javoblarni o'zbek tilida ber. "
            f"Foydalanuvchi so'rovi: {message.text}"
        )
        
        response = model.generate_content(prompt)
        answer = response.text
        
        if len(answer) > 4000:
            for i in range(0, len(answer), 4000):
                await message.answer(answer[i:i+4000], parse_mode="Markdown")
            await msg.delete()
        else:
            await msg.edit_text(answer, parse_mode="Markdown")
            
    except Exception as e:
        logging.error(f"Xatolik: {e}")
        await msg.edit_text(f"Xatolik yuz berdi. Iltimos, birozdan so'ng qayta urinib ko'ring.\n\nTexnik xabar: {str(e)}")

async def main():
    print("--- Bot ishga tushishga tayyor ---")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("--- Bot to'xtatildi ---")
        
