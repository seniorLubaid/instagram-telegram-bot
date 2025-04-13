import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# رابط الـ API الخاص بك على Render
API_URL = "https://instagram-api-xlhn.onrender.com/instagram?url="

# يرسل رابط إنستقرام إلى API ويستقبل رابط الفيديو
def get_instagram_video(insta_url):
    try:
        response = requests.get(API_URL + insta_url)
        if response.status_code == 200:
            data = response.json()
            return data.get("url")
    except Exception as e:
        print("Error contacting API:", e)
    return None

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أرسل رابط إنستقرام (Post أو Reel عام)، وسأرسل لك الفيديو مباشرة!")

# استقبال الروابط من المستخدم
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if "instagram.com" in url:
        video_url = get_instagram_video(url)
        if video_url:
            await update.message.reply_video(video=video_url)
        else:
            await update.message.reply_text("ما قدرت أجيب الفيديو. تأكد إن الرابط عام أو جرب رابط ثاني.")
    else:
        await update.message.reply_text("أرسل رابط إنستقرام فقط.")

# تشغيل البوت
if __name__ == '__main__':
    TOKEN = os.getenv("BOT_TOKEN")
    if not TOKEN:
        raise Exception("BOT_TOKEN environment variable not set.")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot started and polling...")
    app.run_polling()
