# Telegram counting bot
That's the bot that gives you the estimated reading time based on a number of words you fed him. Everything is based on the data I collected (the example is in .csv file) and fancy ML algorithms.

You'll need `graphlab-create` and python Telegram API wrapper for this bot. You simply download the both .py and .csv file and fire it up.

## Requirenments

- GraphLab-Create:
- `$ pip install graphlab-create`
- You should also visit their website and get the product key.
- `$ pip install python-telegram-bot`

Everything's build with Python 2.7. It should also work with the Python 3, but I haven't tested it myself, so I am not so sure. 

## How to:
Plainly speaking, the bot as simple as it gets. You just send him a number of words and it will give you the estimated reading time both in seconds and in minutes.
