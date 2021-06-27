#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

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
import random
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters



# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

import numpy as np
import pandas as pd
import string 
import re
import nltk
# nltk.download('stopwords')
# nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


import tensorflow as tf
from tensorflow import keras
lstm = keras.models.load_model('LSTM_Model.h5')


import pickle
tok = loaded_tokenizer_model = pickle.load(open("tokenizer_file.sav", 'rb'))
from processing.helpers import *
from processing.preprocessing import overall_cleantext

# env config for local
# SECRET_TOKEN = "1856799840:AAHCwlC5PGKQj9aZacEe42nq_nAJv9RjC90"
# PORT = int(os.environ.get('PORT', 5000))

# env config for deployment
SECRET_TOKEN = os.getenv("SECRET_TOKEN")
PORT = int(os.environ.get('PORT', 8443))


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

    vector = overall_cleantext(str(update.message.text), tok)
    prediction = lstm.predict(vector)
    result = []
    is_toxic = False
    for v in prediction[0]:
        if v >= 0.5:
            result.append(1)
            is_toxic = True
        else:
            result.append(0)
    labels = ["toxic", "severely toxic", "obscene","threatening","insulting","a form of identity hate"]
    actions_list = [
        'Do you kiss your mother with that mouth?',
        'Please mind your language.',
        'We have a good track record of working together, no reason to change that now.',
        "Surely you're educated enough to say that in a pleasant way.",
        "Fortunately, I'm not offended, especially by one-off situations like this."
    ]
    your_comment_is = "Your comment is"
    if is_toxic == True:
        for i in range(len(labels)):
            if result[i] == 1:
                your_comment_is += " " + labels[i] + ","
        your_comment_is = your_comment_is.rstrip(",")
        your_comment_is += '. '
        your_comment_is += actions_list[int(random.randrange(0, len(actions_list)))]
        update.message.reply_text(your_comment_is)
    


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(SECRET_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    # updater.start_polling()
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=SECRET_TOKEN,
                          webhook_url='https://serene-oasis-90115.herokuapp.com/' + SECRET_TOKEN)


    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()