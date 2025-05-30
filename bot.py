import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import cv2
from distorted import distorted_image

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Token del bot (coloca tu token real aquí o usa variables de entorno)
TOKEN = os.getenv("BOT_TOKEN")

# Ruta de descarga de imágenes
DOWNLOAD_PATH = "downloads"
os.makedirs(DOWNLOAD_PATH, exist_ok=True)

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)

    file_path = os.path.join(DOWNLOAD_PATH, "input.jpg")
    await file.download_to_drive(file_path)

    # Procesar la imagen
    result = distorted_image(file_path)

    if result is None:
        await update.message.reply_text("❗ No se detectó ningún rostro. Intenta con otra imagen más clara y de frente.")
        return

    output_path = os.path.join(DOWNLOAD_PATH, "output.jpg")
    cv2.imwrite(output_path, result)

    await update.message.reply_photo(photo=open(output_path, "rb"))
    await update.message.reply_text("✅ Imagen procesada con éxito.")

if name == 'main':
    app = ApplicationBuilder().token(TOKEN).build()

    photo_handler = MessageHandler(filters.PHOTO, handle_photo)
    app.add_handler(photo_handler)

    print("Bot iniciado...")
    app.run_polling()
