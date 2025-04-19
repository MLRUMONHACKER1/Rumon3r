import os
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# remove.bg API Key
REMOVE_BG_API_KEY = "zjBNiMgR2YoYkqmddsnmkW7J"

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("হ্যালো! আমাকে একটি ছবি পাঠান, আমি এর ব্যাকগ্রাউন্ড সরিয়ে দেব!")

# Function to remove background
async def remove_background(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_file = await update.message.photo[-1].get_file()
    photo_path = "input.jpg"
    await photo_file.download_to_drive(photo_path)

    with open(photo_path, 'rb') as image_file:
        response = requests.post(
            'https://api.remove.bg/v1.0/removebg',
            files={'image_file': image_file},
            data={'size': 'auto'},
            headers={'X-Api-Key': REMOVE_BG_API_KEY},
        )

    if response.status_code == 200:
        output_path = "no_bg.png"
        with open(output_path, 'wb') as out:
            out.write(response.content)
        await update.message.reply_photo(photo=open(output_path, 'rb'))
    else:
        await update.message.reply_text("দুঃখিত, ব্যাকগ্রাউন্ড রিমুভ করতে সমস্যা হয়েছে।")

# Main function
def main():
    TOKEN = "7879948390:AAH7HhCt7jhwU3vIjxjy-aGNkHmqDyy3JoU"

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, remove_background))

    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()