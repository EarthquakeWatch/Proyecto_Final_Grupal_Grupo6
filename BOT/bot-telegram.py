from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import pandas as pd
# Para generar valores aleatorios(Esto es de prueba, para mostrar como funciona.)
import random

chat_state = {}
df = pd.read_csv('datos_eeuu.csv')


def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id

    if chat_id not in chat_state:
        chat_state[chat_id] = {"start": False}

    context.bot.send_message(chat_id=chat_id, text="¡Alerta sismos!")
    chat_state[chat_id]["start"] = True

    peligrosidad(update, context)
    localizacion(update, context)


def peligrosidad(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id

    # Convertimos la columna 'mag' en una lista de magnitudes para luego arroje una mag aleatoria
    magnitudes = df['mag'].tolist()
    # Asegurar que arroje una magnitud diferente
    magnitud = random.choice(magnitudes)

    if magnitud < 5.0:
        nivel = "bajo"
    elif magnitud < 7.0:
        nivel = "mediano"
    else:
        nivel = "alto"

    context.bot.send_message(
        chat_id=chat_id, text=f"Nivel de peligrosidad: {nivel}. Magnitud del sismo: {magnitud}")


def localizacion(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id

    # generamos un índice aleatorio dentro del rango válido de filas en el DataFrame.
    random_index = random.randint(0, len(df) - 1)
    title = df['title'][random_index]
    Longitud = df['Longitud'][random_index]
    Latitud = df['Latitud'][random_index]

    context.bot.send_message(
        chat_id=chat_id, text="Información de localización:")
    context.bot.send_message(chat_id=chat_id, text=f"title: {title}")
    context.bot.send_message(chat_id=chat_id, text=f"Latitud: {Latitud}")
    context.bot.send_message(chat_id=chat_id, text=f"Longitud: {Longitud}")
    context.bot.send_location(
        chat_id=chat_id, latitude=Latitud, longitude=Longitud, live_period=60)


def main():
    updater = Updater(
        token="6283832471:AAGoH7EEKXw3cHs56lXegB6ZbXRLlAen09k", use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
