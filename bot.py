import os
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# محاولة استخراج الفيديو من صفحة HTML مباشرة (يدعم Reels)
def get_instagram_video(insta_url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept-Language": "en-US,en;q=0.9",
        }
        res = requests.get(insta_url, headers=headers)
        if res.status_code != 200:
            print("Error: status code", res.status_code)
            return None
        soup = BeautifulSoup(res.text, 'html.parser')
        video_tags = soup.find_all("meta", property="og:video")
        if video_tags:
            return video_tags[0].get("content")
    except Exception as e:
        print("Error while scraping video:", e)
    return None

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أرسل رابط فيديو من إنستقرام (منشور أو Reels عام)، وسأقوم بتحميله لك!")

# التعامل مع الرسائل
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if "instagram.com" in url:
        video_url = get_instagram_video(url)
        if video_url:
            await update.message.reply_video(video=video_url)
        else:
            await update.message.reply_text("ما قدرت أجيب الفيديو. تأكد إن الرابط عام أو جرب رابط ثاني.")
    else:
        await update.message.reply_text("أرسل رابط إنستقرام صالح.")

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
