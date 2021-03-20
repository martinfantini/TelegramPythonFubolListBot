import logging

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import re

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

players_id_name = {}

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')

def return_list_players(update: Update) -> None:
    str_players = "The players are : \n"
    i=1
    for the_key, the_value in players_id_name.items():
        str_players = str_players +  str(i) + ". " + the_value + "\n"
        i=i+1
    update.message.reply_text( str_players,  quote=False)


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text("Envia la palabra \"Juego\" o \"juego\" para anotarte",  quote=False)

def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    logger.info(update)
    if type(update.message.text) != str:
        update.message.reply_text("Manda algo coherente",  quote=False)
        return
    
    if len(players_id_name) > 9:
        update.message.reply_text("Estamos completos",  quote=False)
        return
    
    result_lista = re.match(".*(lista|Lista).*", update.message.text)
    if result_lista:
        return_list_players(update)  
        return

    result_baja = re.match(".*(baja|Baja).*", update.message.text)
    if result_baja:
        del players_id_name[update.message.from_user.id]
        update.message.reply_text("Removed from the list of players")
        return

    result_juego = re.match(".*(Juego|juego).*", update.message.text)
    if not result_juego:
        return
    
    if (update.message.from_user.id in players_id_name):
        if type(update.message.from_user.first_name) == str and type(update.message.from_user.last_name) == str :
            update.message.reply_text("Ya estas anotado. ( " + update.message.from_user.first_name + " " + update.message.from_user.last_name + " )",  quote=False)
        elif type(update.message.from_user.last_name) != str :
            update.message.reply_text("Ya estas anotado. ( " + update.message.from_user.first_name + " )",  quote=False)
        return
    
    if type(update.message.from_user.first_name) != str and type(update.message.from_user.last_name) != str :
        update.message.reply_text("Hola Desconocido! Ponete un nombre boludo",  quote=False)
    elif type(update.message.from_user.last_name) != str :
        players_id_name[update.message.from_user.id] = update.message.from_user.first_name
    else:
        players_id_name[update.message.from_user.id] = update.message.from_user.first_name + " " + update.message.from_user.last_name
    
    return_list_players(update)

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("ADD YOUR TOKEN HERE")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    #dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    
    # on noncommand i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
