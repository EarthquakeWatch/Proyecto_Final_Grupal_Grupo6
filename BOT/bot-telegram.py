from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import pandas as pd

chat_state = {}
df = pd.read_csv('datos_eeuu.csv')  # Ruta y nombre de tu archivo CSV


def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id

    if chat_id not in chat_state:
        chat_state[chat_id] = {"start": False}

    if not chat_state[chat_id]["start"]:
        context.bot.send_message(chat_id=chat_id, text="¡Alerta sismos!")
        chat_state[chat_id]["start"] = True

    peligrosidad(update, context)
    localizacion(update, context)


def peligrosidad(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id

    if chat_id not in chat_state:
        chat_state[chat_id] = {}

    if "peligrosidad" not in chat_state[chat_id]:
        chat_state[chat_id]["peligrosidad"] = False

    if not chat_state[chat_id]["peligrosidad"]:
        magnitud = df['mag'][0]

        if magnitud < 5.0:
            nivel = "bajo"
        elif magnitud < 7.0:
            nivel = "mediano"
        else:
            nivel = "alto"

        context.bot.send_message(
            chat_id=chat_id, text=f"Nivel de peligrosidad: {nivel}. Magnitud del sismo: {magnitud}")
        chat_state[chat_id]["peligrosidad"] = True


def localizacion(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id

    title = df['title'][0]
    Longitud = df['Longitud'][0]
    Latitud = df['Latitud'][0]

    context.bot.send_message(
        chat_id=chat_id, text="Información de localización:")
    context.bot.send_message(chat_id=chat_id, text=f"title: {title}")
    context.bot.send_message(chat_id=chat_id, text=f"Latitud: {Latitud}")
    context.bot.send_message(chat_id=chat_id, text=f"Longitud: {Longitud}")
    context.bot.send_location(
        chat_id=chat_id, latitude=Latitud, longitude=Longitud, live_period=60)


def main():
    updater = Updater(
        token="6283832471:AAGoH7EEKXw3cHs56lXegB6ZbXRLlAen09k", use_context=True)  # Reemplaza "TOKEN" por tu token de bot
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
