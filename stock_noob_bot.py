import os
import sys
import logging

from telegram.ext import Updater, CommandHandler
from telegram.bot import Bot
import telegram
import functions as fct

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger()

# Getting mode, so we could define run function for local and Heroku setup
mode = os.getenv("MODE")
TOKEN = os.getenv("TOKEN")
api_key = os.getenv('API_KEY')

bot = Bot(token=TOKEN)

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
    bot.send_message(chat_id=update.message.chat_id, text='Hello {}'.format(update.message.from_user.first_name))
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
            msg = "Commands\n"
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
    str = '<pre>Symbol |  Price  | Part | Change\n-------|---------|------|-------\n'
    try:
        sum_percent = 0
        for i in eval(context.args[0]):
            value_stock, percent = fct.get_stock(i)
            str += "{symbol:7s}|R${value:7.2f}|{part:5.2f}%|{var:5.2f}%\n".format(
                symbol=i, value=value_stock, var=percent, part=eval(context.args[0])[i])
            sum_percent += (percent*eval(context.args[0])[i])/100
        perf = "Performance day [{perf_day:.2f}%]".format(perf_day=sum_percent)
        str += '</pre>'
        bot.send_message(chat_id=update.message.chat_id, text=str, parse_mode=telegram.ParseMode.HTML)
        update.message.reply_text(perf)
    except Exception as e:
        print(e)
        help(update, context)


def stock_real_time(update, context):
    context.kwargs = dict()
    context.kwargs['command'] = 'stock_real_time'
    try:
        try:
            if len(context.args) == 0:
                raise IndexError
            _str = '<pre>Symbol |  Price  | Change\n-------|-------|-------\n'
            for i in context.args:
                symbol = i.upper()
                value_stock, percent_day = fct.get_stock(symbol)
                _str += '{symbol:7s}|R${value:7.2f}|{var:5.2f}%\n'.format(symbol=symbol, value=value_stock,
                                                                          var=percent_day)
            _str += '</pre>'
            bot.send_message(chat_id=update.message.chat_id, text=_str, parse_mode=telegram.ParseMode.HTML)

        except AttributeError:
            context.error = 'Quote not found for ticker symbol: {}'.format(symbol)
            help(update, context)
    except IndexError:
        context.error = "commands\n /stock_real_time [symbol] [symbol] ..."
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
