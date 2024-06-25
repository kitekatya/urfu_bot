from telebot.types import Message
from functools import wraps
from datetime import datetime


def logger(bot):
    def log(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            if len(args) == 1 and type(args[0]) is Message:
                message: Message = args[0]
                s = f'{message.from_user.id} {message.from_user.full_name} '\
                      f'{message.from_user.username} {message.text} '\
                      f'{datetime.fromtimestamp(message.date)}'
                bot.send_message(-1001931332770, s)
            return function(*args, **kwargs)
        return wrapper
    return log
