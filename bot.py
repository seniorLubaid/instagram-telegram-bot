import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# استخدام API خارجية لسحب الفيديو من Instagram
def get_instagram_video(insta_url):
    try:
        api_url = f"https://api.keeptube.cc/insta?url={insta_url}"
        response = requests.get(api_url, timeout=10)
        data = response.json()
        if "url" in data:
            return data["url"]
    except Exception as e:
        print("Error fetching video:", e)
    return None

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أرسل لي رابط فيديو من إنستقرام (منشور عام أو Reels)، وسأقوم بتحميله لك!")

# التعامل مع الرسائل
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if "instagram.com" in url:
        video_url = get_instagram_video(url)
        if video_url:
            await update.message.reply_video(video=video_url)
        else:
            await update.message.reply_text("ما قدرت أجيب الفيديو. تأكد إن الرابط عام أو جرب مرة ثانية.")
    else:
        await update.message.reply_text("أرسل رابط إنستقرام صالح.")

# تشغيل البوت
if __name__ == '__main__':
    TOKEN = os.getenv("BOT_TOKEN")  # متغير البيئة من Render
    if not TOKEN:
        raise Exception("BOT_TOKEN environment variable not set.")
    
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot started and polling...")
    app.run_polling()
