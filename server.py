from flask import Flask
from threading import Thread
from bot import bot


app = Flask('')


@app.route('/')
def home():
    return "I'm alive"


@app.route('/iot', methods=['GET'])
def arduino():
    return 'iot_alive'


def run():
    app.run(host='0.0.0.0', port=80)


def bot_run():
    bot.infinity_polling(none_stop=True)


def keep_alive():
    t = Thread(target=run)
    t.start()
