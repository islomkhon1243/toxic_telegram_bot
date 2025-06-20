import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import random
from background import keep_alive

# 🔑 API-ключи
GEMINI_API_KEY = "AIzaSyAaPCjYO4xVOcQx8_PgvH1gX7bSRWPfr3c"
TELEGRAM_BOT_TOKEN = "7760792899:AAG_KTwM_SXQQO6OINo7nkvv4goriB-RasI"

# ⚙️ Настройка Google Gemini API
client = genai.Client(api_key=GEMINI_API_KEY)


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
        response = client.models.generate_content(model="gemini-2.0-flash",
                                                  contents=prompt)
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


keep_alive()
if __name__ == "__main__":
    main()
