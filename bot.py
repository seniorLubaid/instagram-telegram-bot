import os
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# استخراج رابط الفيديو من إنستقرام
def get_instagram_video(insta_url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    res = requests.get(insta_url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    for meta in soup.find_all("meta"):
        if meta.get("property") == "og:video":
            return meta.get("content")
    return None

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أرسل لي رابط فيديو من إنستقرام (منشور عام) وسأقوم بتحميله لك!")

# التعامل مع الرسائل
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if "instagram.com" in url:
        video_url = get_instagram_video(url)
        if video_url:
            await update.message.reply_video(video=video_url)
        else:
            await update.message.reply_text("ما قدرت أجيب الفيديو. تأكد إن الرابط عام.")
    else:
        await update.message.reply_text("أرسل رابط إنستقرام صالح.")

# تشغيل البوت
if __name__ == '__main__':
    TOKEN = os.getenv("BOT_TOKEN")  # يسحب التوكن من Environment Variable
    if not TOKEN:
        raise Exception("BOT_TOKEN environment variable not set.")
    
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()
