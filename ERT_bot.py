from __future__ import division
import graphlab
graphlab.product_key.set_product_key('KEY')
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
    bot.sendMessage(update.message.chat_id, text='Hello and welcome. Make sure to check /help section if you have ane questions.')


def help(bot, update):
    bot.sendMessage(update.message.chat_id, text="The bot can give you the estimated reading time based\
        on a number of symbols you fed him. Just use /estimate command and give him a number.")

def estimate(bot, update, args):
    try:
        print update.message.date
        words = int(args[0])
        if words > 0:
            longread = {'Words':[words]}
            prep1 = read_model.predict(graphlab.SFrame(longread))
            prep2 = graphlab.SArray(data=prep1, dtype=str)
            prep3 = prep2/60
            prep4 = ''.join(str(e) for e in prep2)
            prep5 = ''.join(str(e) for e in prep3)
            final = prep4[:prep4.find(".")+3]
            final1 = prep5[:prep5.find(".")+3]
            bot.sendMessage(update.message.chat_id, 'It will take %s seconds or %s minutes.' % (final, final1))
        else:
            bot.sendMessage(update.message.chat_id, "Nope, I can't do that. Please, try again.")
    except IndexError:
        bot.sendMessage(update.message.chat_id, "Are you even listening? Give me numbers!")
    except ValueError:
        bot.sendMessage(update.message.chat_id, "_Mistakes were made_! You need to use /estimate and then feed the bot a number.", parse_mode = "Markdown")

def speaking(bot, update):
    try:
        words = int(update.message.text)
        if type(words) == int:
            bot.sendMessage(update.message.chat_id, 'Please, use /estimate command to get the result.')
    except ValueError, IndexError:
        bot.sendMessage(update.message.chat_id, "Ok, firstly, the bot needs numbers. Secondly, make sure to use /estimate command.")

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    updater = Updater("TOKEN")

    dp = updater.dispatcher

    dp.addHandler(CommandHandler("start", start))
    dp.addHandler(CommandHandler("help", help))
    dp.addHandler(CommandHandler("estimate", estimate))

    dp.addHandler(MessageHandler(speaking))

    dp.addErrorHandler(error)

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
