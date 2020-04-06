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
import os
import sys
import logging
import json

from collections import OrderedDict
from telegram.ext import Updater, CommandHandler
from urllib import request
import functions as fct

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger()

# Getting mode, so we could define run function for local and Heroku setup
mode = os.getenv("MODE")
TOKEN = os.getenv("TOKEN")
api_key = os.getenv('API_KEY')

if mode == "dev":
    def run(updater):
        updater.start_polling()
elif mode == "prod":
    def run(updater):
        PORT = int(os.environ.get("PORT", "8443"))
        HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=TOKEN)
        updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))
else:
    logger.error("No MODE specified!")
    sys.exit(1)

# Stock Suno Value
value = {'ITSA4': 10, 'SULA11': 10, 'BPAC11': 5, 'MYPK3': 5, 'BRAP4': 5, 'ALUP11': 5,
         'CVCB3': 5, 'RLOG3': 5, 'MDIA3': 5, 'B3SA3': 5, 'KLBN11': 5, 'GEPA4': 10,
         'SUZB3': 5, 'CGRA4': 10, 'COCE5': 5}

# Stock Suno Dividend
dividend = {'ITSA4': 10, 'ENBR3': 10, 'TAEE11': 10, 'BBSE3': 10, 'EGIE3': 5, 'PETR4': 5,
            'ABCB4': 5, 'TUPY3': 5, 'LEVE3': 5, 'UNIP6': 15, 'WIZS3': 5, 'VIVT4': 5,
            'GRND3': 5}

# Stock Suno FII
fii = {'ALZR11': 100/15., 'FIIB11': 100/15., 'HGCR11': 100/15., 'HGLG11': 100/15., 'HGRU11': 100/15.,
       'HSML11': 100/15., 'IRDM11': 100/15., 'MALL11': 100/15., 'RBRP11': 100/15., 'RBRR11': 100/15.,
       'VILG11': 100/15., 'VISC11': 100/15., 'VRTA11': 100/15., 'XPLG11': 100/15., 'XPML11': 100/15.}

portfolios = ['value', 'dividend', 'fii']

commands = ['help', 'portfolio', 'stock_real_time']
# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')
    help(update, context)


def help(update, context):
    """Send a message when the command /help is issued."""

    try:
        if context.kwargs['command'] == 'portfolio':
            msg = 'commands /portfolio [option]\nOptions:\n'
            for i in portfolios:
                msg += '    {}\n'.format(i)
        elif context.kwargs['command'] == 'stock_real_time':
            msg = context.error
        else:
            msg = "commands\n"
            for command in commands:
                msg += '/{}\n'.format(command)
        update.message.reply_text(msg)

    except AttributeError:
        context.kwargs = dict()
        if len(context.args) == 1 and context.args[0] in commands:
            context.kwargs['command'] = context.args[0]
        else:
            context.kwargs['command'] = 'help'
        help(update, context)


def portfolio(update, context):
    context.kwargs = dict()
    context.kwargs['command'] = 'portfolio'
    str = "Ticker     [Value] [Part]\n--------------------------------------------\n"
    try:
        for i in eval(context.args[0]):
            str += "{:10s} [R${:.2f}] [{:.2f}%]\n".format(i, fct.get_stock(i), eval(context.args[0])[i])
        update.message.reply_text(str)
    except:
        help(update, context)


def stock_real_time(update, context):
    context.kwargs = dict()
    context.kwargs['command'] = 'stock_real_time'
    try:
        symbol = context.args[0].upper()
        try:
            value = fct.get_stock(context.args[0])
            _str = '{symbol} [R${value}]'.format(symbol=symbol, value=value)
            update.message.reply_text(_str)
        except AttributeError:
            context.error = 'Quote not found for ticker symbol: {}'.format(symbol)
            help(update, context)
    except IndexError:
        context.error = "commands /stock_real_time [symbol]"
        help(update, context)


if __name__ == '__main__':
    logger.info("Starting bot")
    updater = Updater(TOKEN, use_context=True)

    dp = updater
    dp.dispatcher.add_handler(CommandHandler("start", start))
    dp.dispatcher.add_handler(CommandHandler("help", help))
    dp.dispatcher.add_handler(CommandHandler("portfolio", portfolio, pass_args=True))
    dp.dispatcher.add_handler(CommandHandler("stock_real_time", stock_real_time, pass_args=True))

    run(dp)
