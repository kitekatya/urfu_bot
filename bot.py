import telebot
from telebot import types
import Parser
import re
import threading
import os
from logger import logger

bot = telebot.TeleBot(os.getenv('urfu_bot'))

data: dict[int] = dict()
data_brs: dict[int] = dict()
update = 'Обновить'
subjects_text = 'Предметы'


@bot.message_handler(commands=['start', 'help'])
@logger(bot)
def start(msg: types.Message):

    if msg.text == '/start':
        mess = f'''Привет, <b>{msg.from_user.first_name}</b>! 
    Тут будут баллы БРС
    Тебе нужно будет ввести свой email и пароль от кабинета студента'''

        bot.send_message(msg.chat.id, mess, parse_mode='html')
        if msg.from_user.id not in data:
            bot.send_message(msg.chat.id, 'Пожалуйста, введите email')
            bot.register_next_step_handler(msg, register_email)

    elif msg.text == '/help':
        mess = '''Тут что то есть'''
        bot.send_message(msg.chat.id, mess)


@bot.message_handler(func=lambda msg: msg.text == update)
def update_by_user(msg: types.Message):
    if msg.from_user.id not in data_brs: return

    text = update_info(msg.from_user.id)
    if text is None: return
    if len(text) > 0: bot.send_message(msg.chat.id, text)
    else: bot.send_message(msg.chat.id, 'Проверил. Ничего нового')


@bot.message_handler(func=lambda msg: msg.text == subjects_text)
def show_subject(msg: types.Message):
    if msg.from_user.id not in data_brs: return

    mess = ''
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for subject in data_brs[msg.from_user.id]:
        mess += f'{data_brs[msg.from_user.id][subject].name_subject}\n'
        markup.add(data_brs[msg.from_user.id][subject].name_subject)
    markup.add('Назад')
    bot.send_message(msg.chat.id, mess, reply_markup=markup)
    bot.register_next_step_handler(msg, get_subject)

def get_subject(msg: types.Message):
    if msg.text != 'Назад':
        mess = str(data_brs[msg.from_user.id][msg.text])
        bot.send_message(msg.chat.id, mess)
        bot.register_next_step_handler(msg, get_subject)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(subjects_text, update)
        bot.send_message(msg.chat.id, f'{subjects_text}\n{update}',
                         reply_markup=markup)


def update_info(user_id) -> str | None:
    if user_id not in data_brs:
        bot.send_message(user_id, 'Вашего аккаунта нет')
        return

    mess = ''
    old = data_brs[user_id]
    if try_get(user_id):
        if old == data_brs[user_id]:
            return mess
        for subject in data_brs[user_id]:
            if subject not in old:
                old[subject] = dict()
            for header in data_brs[user_id][subject]:
                if header not in old[subject]:
                    old[subject][header] = dict()
                for name_event in data_brs[user_id][subject][header]:
                    if name_event not in old[subject][header]:
                        mess += f'{subject} {name_event} ' \
                                f'{data_brs[user_id][subject][header][name_event]["dict"]}\n'
                    elif old[subject][header][name_event]['dict'] != \
                            data_brs[user_id][subject][header][name_event][
                                'dict']:
                        mess += f'{subject} {name_event}: {old[subject][header][name_event]["dict"]}' \
                                f' ➞ {data_brs[user_id][subject][header][name_event]["dict"]}\n'
        return mess.strip()


def register_email(msg: types.Message):
    if re.match(r'.+@.+\.((ru)|(com))', msg.text):
        if msg.from_user.id not in data:
            data[msg.from_user.id] = dict()
        data[msg.from_user.id]['username'] = msg.text
        bot.send_message(msg.chat.id, 'Отлично! Теперь введи пароль')
        bot.register_next_step_handler(msg, register_password)
    else:
        bot.send_message(msg.chat.id, 'Такого адреса нет. Если у вас '
                                      'действительно такой адрес,'
                                      ' писать сюда @k1te_kate')


def register_password(msg: types.Message):
    data[msg.from_user.id]['password'] = msg.text
    bot.send_message(msg.chat.id, 'Выполняю попытку входа...')
    if try_get(msg.from_user.id):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(subjects_text, update)
        bot.send_message(msg.chat.id, 'Успешно!', reply_markup=markup)
    else:
        bot.send_message(msg.chat.id, 'Введите email')
        bot.register_next_step_handler(msg, register_email)


def try_get(user_id):
    try:
        parser = Parser.Parser(**data[user_id])
        parser.parse()
        data_brs[user_id] = parser.brs
    except Exception as e:
        bot.send_message(user_id, 'Произошла ошибка в запросе на сайт')
        return False
    return True


def auto_update():
    for user_id in data:
        try:
            text = update_info(user_id)
        except Exception as e:
            bot.send_message(user_id, f'Там короч ошибка {e}, возможно БРС '
                                      f'обновился')
        if text is not None and len(text) > 0:
            bot.send_message(user_id, text)
    bot.send_message(-1001931332770, f'auto upd {user_id}\n'+text)
    threading.Timer(30 * 60, auto_update).start()


def start():
    bot.polling()
