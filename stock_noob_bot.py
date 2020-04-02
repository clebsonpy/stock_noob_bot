"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import urllib
import json

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


value = {'ITSA4': 10, 'SULA11': 10, 'BPAC11': 5, 'MYPK3': 5, 'BRAP4': 5, 'ALUP11': 5,
                'CVCB3': 5, 'RLOG3': 5, 'MIDIA3': 5, 'B3SA3': 5, 'KLBN11': 5, 'GEPA4': 10,
                'SUZB3': 5, 'CGRA4': 10, 'COCE5': 5}

dividend = {}

fii = {}

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def get_stock(symbol):
    try:
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=' + symbol + '&interval=1min&outputsize=compact&apikey=<api_thiago>'
        response = urllib.request.urlopen(url)
        data = json.loads(response.read().decode('utf8'), object_pairs_hook=OrderedDict)
        counter = 1
        for tick in data["Time Series (1min)"]:
            if (counter == 1):
                close = float(data["Time Series (1min)"][tick]["4. close"])
                return close
    except:
        return -1

    return -1


def portfolio(update, context):

    str = ""
    try:
        for i in eval(context.args[0]):
            str += "{} [{}%]\n".format(i, value[i])
    except:
        help(update, context)
    update.message.reply_text(str)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1245387288:AAH0uq8Wf3tUvD9mQ80HAPobnLUz4NGnBt0", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("portfolio", portfolio, pass_args=True))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()