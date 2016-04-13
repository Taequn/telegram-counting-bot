from __future__ import division
import graphlab
graphlab.product_key.set_product_key('<your product key>')
from telegram.ext import Updater
import logging

logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)

url = 'reading.csv'
read = graphlab.SFrame.read_csv(url, header=True, column_type_hints=int)
read_model = graphlab.linear_regression.create(read, target='Time',
                                               features=['Words'],validation_set=None)

def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hello and welcome. All you need to do is to type a number of words.')


def help(bot, update):
    bot.sendMessage(update.message.chat_id, text="OK, just type a number, that's all")


def echo(bot, update):
    try:
        print update.message.date
        words = int(update.message.text)
        longread = {'Words':[words]}
        prep1 = read_model.predict(graphlab.SFrame(longread))
        prep2 = graphlab.SArray(data=prep1, dtype=str)
        prep3 = prep2/60
        final = ''.join(str(e) for e in prep2)
        final1 = ''.join(str(e) for e in prep3)
        bot.sendMessage(update.message.chat_id, 'It will take %s seconds or %s minutes' % (final, final1))
    except IndexError:
        bot.sendMessage(update.message.chat_id, "Are you even listening? Give me numbers!")
    except ValueError:
        bot.sendMessage(update.message.chat_id, "Are you even listening? Give me numbers!")


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    updater = Updater("<Your telegram token")

    dp = updater.dispatcher

    dp.addTelegramCommandHandler("start", start)
    dp.addTelegramCommandHandler("help", help)

    dp.addTelegramMessageHandler(echo)

    dp.addErrorHandler(error)

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
