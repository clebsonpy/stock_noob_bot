FROM python:3.7

RUN pip install python-telegram-bot
RUN pip install yahooquery

RUN mkdir /app
ADD . /app
WORKDIR /app

CMD python /app/stock_noob_bot.py