import os
import signal
import telebot
from telebot import types
from django.core.management.base import BaseCommand
from django.conf import settings

bot = telebot.TeleBot(settings.TOKEN_ADMIN)


class Command(BaseCommand):
    help = 'Админка MeFi'

    def handle(self, *args, **options):
        bot.polling(none_stop=True)


@bot.message_handler(content_types=['text'])
def message_handler(message):
    if message.text.lower() == "/start" or message.text.lower() == "старт" or message.text.lower() == "начать" or message.text.lower() == "привет" or message.text.lower() == "привет!":
        bot.send_message(message.chat.id,
                         'Привет. Этот бот создан для администраторов сервиса Meetup Finder',
                         reply_markup=button_menu())
    elif message.text.lower() == "выкл. вк":
        vkpid = open('vkpid.txt', 'r')
        os.kill(int(vkpid.readline()), signal.SIGTERM)
        vkpid.close()
        bot.send_message(message.chat.id, "ВК бот перезапущен", reply_markup=button_menu())

    elif message.text.lower() == "выкл. тг":
        tgpid = open('tgpid.txt', 'r')
        os.kill(int(tgpid.readline()), signal.SIGTERM)
        tgpid.close()
        bot.send_message(message.chat.id, "ТГ бот перезапущен", reply_markup=button_menu())


def button_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.InlineKeyboardButton(text='Выкл. ВК', callback_data='/off_vk'),
               types.InlineKeyboardButton(text='Выкл. ТГ', callback_data='/off_tg'))
    return markup


# def admin(tgpid):
#     quest = input('Kill Tg? (Y/n)').lower()
#     if quest == 'y':
#         os.kill(int(tgpid.readline()), signal.SIGTERM)
#     elif quest == 'n':
#         admin(tgpid)
#     else:
#         print('Бля ты тупой нах?? ')
#         admin(tgpid)
