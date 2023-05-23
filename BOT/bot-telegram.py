from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import pandas as pd
import random

chat_state = {}
df = pd.read_csv('datos_eeuu.csv')

# JobQueue permite programar y ejecutar trabajos o tareas en momentos específicos o con una periodicidad determinada(es una caracteristica de la biblioteca de python-telegram-bot)
# Cada persona que envie /start tendra su propio trabajo programado en el JobQueue lo que permite enviar actualizacion automaticas periodiacas a cada persona


def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id

    if chat_id not in chat_state:
        chat_state[chat_id] = {"start": False, "job_queue": None}

    context.bot.send_message(chat_id=chat_id, text="¡Alerta sismos!")
    chat_state[chat_id]["start"] = True

    peligrosidad(context.bot, chat_id)
    localizacion(context.bot, chat_id)

    # Verificamos si el job_queue no está configurado para este chat_id y si no esta crearlo
    if chat_state[chat_id]["job_queue"] is None:
        job_queue = context.job_queue
        job = job_queue.run_repeating(
            send_sismo, interval=30, first=30, context=chat_id)
        chat_state[chat_id]["job_queue"] = job_queue


def send_sismo(context: CallbackContext):
    chat_id = context.job.context

    # Enviamos alerta de sismo, peligrosidad y localización
    context.bot.send_message(chat_id=chat_id, text="¡Alerta sismos!")
    peligrosidad(context.bot, chat_id)
    localizacion(context.bot, chat_id)


def peligrosidad(bot, chat_id):
    magnitudes = df['mag'].tolist()
    magnitud = random.choice(magnitudes)

    if magnitud < 5.0:
        nivel = "bajo"
    elif magnitud < 7.0:
        nivel = "mediano"
    else:
        nivel = "alto"

    bot.send_message(
        chat_id=chat_id, text=f"Nivel de peligrosidad: {nivel}. Magnitud del sismo: {magnitud}")


def localizacion(bot, chat_id):
    random_index = random.randint(0, len(df) - 1)
    title = df['title'][random_index]
    Longitud = df['Longitud'][random_index]
    Latitud = df['Latitud'][random_index]

    bot.send_message(chat_id=chat_id, text="Información de localización:")
    bot.send_message(chat_id=chat_id, text=f"title: {title}")
    bot.send_message(chat_id=chat_id, text=f"Latitud: {Latitud}")
    bot.send_message(chat_id=chat_id, text=f"Longitud: {Longitud}")
    bot.send_location(chat_id=chat_id, latitude=Latitud,
                      longitude=Longitud, live_period=60)


def main():
    updater = Updater(
        "6283832471:AAGoH7EEKXw3cHs56lXegB6ZbXRLlAen09k", use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
