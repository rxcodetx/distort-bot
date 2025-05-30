from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
import os
import cv2
from distorted import distort_face

BOT_TOKEN = "TU_TOKEN_AQUI"  # Reemplaza esto con tu token

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Envíame una foto y te devolveré una versión caricaturizada.")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_file = await update.message.photo[-1].get_file()
    file_path = f"input_{update.message.from_user.id}.jpg"
    await photo_file.download_to_drive(file_path)

    distorted_image = distort_face(file_path)
    if distorted_image is not None:
        output_path = f"output_{update.message.from_user.id}.jpg"
        cv2.imwrite(output_path, distorted_image)
        await update.message.reply_photo(photo=open(output_path, 'rb'))
        os.remove(output_path)
    else:
        await update.message.reply_text("No pude detectar un rostro en la imagen 😢")

    os.remove(file_path)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

print("🤖 Bot en línea...")
app.run_polling()
