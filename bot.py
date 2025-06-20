import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import random
import os

# 🔑 API-ключи
GEMINI_API_KEY = "AIzaSyAaPCjYO4xVOcQx8_PgvH1gX7bSRWPfr3c"
TELEGRAM_BOT_TOKEN = "7760792899:AAG_KTwM_SXQQO6OINo7nkvv4goriB-RasI"

# ⚙️ Настройка Google Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

async def toxic_funny_response(update: Update, context: CallbackContext):
    """Обработчик команды /toxic — отвечает токсично на сообщение пользователя."""
    chat = update.message.chat
    user_message = update.message.text

    prompt = f"""
    Отвечай коротко, нагло и с матами. Будь токсичным, говори так, будто тебя всё раздражает, но ты всё равно отвечаешь. 
    Используй сарказм, резкие выражения и чёрный юмор. Если собеседник тупит — подначивай его. Если говорит очевидное — высмеивай.
    Отвечай так, будто тебе вообще плевать, но ты всё равно делаешь это ради забавы.

    Пользователь: {user_message}
    """

    try:
        response = model.generate_content(prompt)
        toxic_reply = response.text if hasattr(
            response, "text") else "Ошибка генерации. Даже ИИ заскучал."
    except Exception as e:
        toxic_reply = f"Ошибка ИИ: {str(e)}"

    await update.message.reply_text(toxic_reply)


def main():
    """Запуск Telegram-бота"""
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("toxic", toxic_funny_response))

    print("🤖 Бот запущен... Вводи /toxic!")
    app.run_polling()
