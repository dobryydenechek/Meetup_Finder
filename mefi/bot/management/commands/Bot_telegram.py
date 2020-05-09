# coding=utf-8
import telebot
from telebot import apihelper
from telebot import types
from django.core.management.base import BaseCommand
from django.conf import settings
from ...models import Eventlist, Userlist, Taglist, Usertaglist, Eventtaglist
import datetime
import time
import threading

bot = telebot.TeleBot(settings.TOKEN)

apihelper.proxy = {
    'https': settings.PROXY_URL
}

logs_error = open('logs_error.txt', 'a+')


# Отлов ошибок
def log_error(f):

    def inner(*args, **options):
        try:
            return f(*args, **options)
        except Exception as e:

            error_message = f'Произошла ошибка: {e}'
            print(error_message)
            logs_error.write(error_message + '\n')
            logs_error.close()
            raise e

    return inner


class Command(BaseCommand):
    help = 'Телеграм-бот'

    def handle(self, *args, **options):
        bot.polling(none_stop=True)


# a = Taglist.objects.get(tl_id=1)
# print(a.tl_title)

# a = Taglist.objects.all()
# print(a)
# all_objects = Taglist.objects.all()
# for i in range(len(all_objects)):
#     print(all_objects[i].tl_id)

# all_objects = Userlist.objects.all()
# print(all_objects[0].ul_linktgmessage)

# ------ Старое подключение телеги --------
# @bot.message_handler(commands=['start'])
# def start_message(message):
#     # print(message.chat.username)
#     all_objects_userlist = Userlist.objects.all()
#     exist_user = False
#     for i in range(len(all_objects_userlist)):
#         if str(message.chat.id) == all_objects_userlist[i].ul_linktgmessage:
#             bot.send_message(message.chat.id, 'С возвращением, друг! ')
#             exist_user = True
#     if not exist_user:
#         bot.send_message(message.chat.id, 'Привет, друг! Введи свой id с сайта, чтобы мы слогли подключить бота')
#         bot.register_next_step_handler(message, send_id)


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Основные функции бота:\n'
                                      '/id - Выводит Ваш id на сайте (но сайт мы еще не допилили хихи)\n'
                                      '/tags - Ваши теги\n'
                                      '/change_tags - Изменить теги\n'
                                      '/events - Все эвенты по тегам\n'
                                      'а так же бот напоминает о эвентах каждый день в 12 часов\n')


@bot.message_handler(commands=['start'])
def start_message(message):
    all_objects_userlist = Userlist.objects.all()
    exist_user = False
    for i in range(len(all_objects_userlist)):
        if str(message.chat.id) == all_objects_userlist[i].ul_linktgmessage:
            bot.send_message(message.chat.id, 'С возвращением, друг! ')
            exist_user = True
    if not exist_user:
        bot.send_message(message.chat.id, 'Привет, друг! Чтобы начать пользоваться ботом, тебе нужно выбрать теги.')
        help(message)
        new_user = Userlist(ul_linktgmessage=message.chat.id)
        new_user.save()
        change_tags(message)


def send_id(message):
    id_in_base = False
    all_objects_userlist = Userlist.objects.all()
    for i in range(len(all_objects_userlist)):
        # print(all_objects[i].ul_id)
        if message.text == str(all_objects_userlist[i].ul_id):
            # print('Success!')
            all_objects_userlist[i].ul_linktgmessage = message.chat.id
            all_objects_userlist[i].save()
            bot.send_message(message.chat.id, 'Телеграм-аккаунт подключен к рассылке')
            id_in_base = True
    if not id_in_base:
        bot.send_message(message.chat.id, 'Мы не нашли ваш id в базе данных')


@bot.message_handler(commands=['id'])
def id_on_the_site(message):
    exist_user = False
    all_objects_userlist = Userlist.objects.all()
    for i in range(len(all_objects_userlist)):
        if str(message.chat.id) == all_objects_userlist[i].ul_linktgmessage:
            bot.send_message(message.chat.id, f'Ваш id на сайте: {all_objects_userlist[i].ul_id}')
            exist_user = True
    if not exist_user:
        bot.send_message(message.chat.id, 'Вы не зарегистрированы на нашем сайте')


@bot.message_handler(commands=['tags'])
def tags(message):
    all_objects_userlist = Userlist.objects.all()
    exist_user = False
    for i in range(len(all_objects_userlist)):
        if str(message.chat.id) == all_objects_userlist[i].ul_linktgmessage:
            tags = ''
            num_of_tag = 0
            all_objects_usertaglist = Usertaglist.objects.all()
            for j in range(len(all_objects_usertaglist)):
                if all_objects_userlist[i].ul_id == all_objects_usertaglist[j].utl_id_user.ul_id:
                    num_of_tag += 1
                    # print(all_objects_usertaglist[j].utl_id_tag.tl_title)
                    tags += str(num_of_tag) + ') ' + \
                            all_objects_usertaglist[j].utl_id_tag.tl_title + '\n'
            if tags != '':
                bot.send_message(message.chat.id, f'Ваши теги: \n{tags}')
            else:
                bot.send_message(message.chat.id, 'Вы не указали теги')
            exist_user = True
    if not exist_user:
        bot.send_message(message.chat.id, 'Вы не зарегистрированы на нашем сайте')


@bot.message_handler(commands=['link', 'account', 'options'])
def site_link(message):
    bot.send_message(message.chat.id, 'Ссылка на сайт: ')


@bot.message_handler(commands=['events'])
def events(message):
    # all_objects_userlist = Userlist.objects.all()
    # all_objects_eventlist = Eventlist.objects.all()
    all_objects_eventtaglist = Eventtaglist.objects.all()
    all_objects_userlist = Userlist.objects.all()
    all_objects_usertaglist = Usertaglist.objects.all()
    exist_user = False
    tags = []
    for i in range(len(all_objects_userlist)):
        if str(message.chat.id) == all_objects_userlist[i].ul_linktgmessage:
            for j in range(len(all_objects_usertaglist)):
                if all_objects_userlist[i].ul_id == all_objects_usertaglist[j].utl_id_user.ul_id:
                    tags.append(all_objects_usertaglist[j].utl_id_tag.tl_title)
            exist_user = True
    if not exist_user:
        bot.send_message(message.chat.id, 'Вы не зарегистрированы на нашем сайте')
    else:
        if tags:
            repeat_events = []
            events_alive = False  # есть ли эвенты для пользователя
            for i in range(len(all_objects_eventtaglist)):
                if all_objects_eventtaglist[i].etl_id_tag.tl_title in tags and all_objects_eventtaglist[i].etl_id_event.el_id not in repeat_events \
                        and all_objects_eventtaglist[i].etl_id_event.el_date.date() >= datetime.datetime.today().date():
                    event = all_objects_eventtaglist[i].etl_id_event.el_title + '\n\n'

                    if all_objects_eventtaglist[i].etl_id_event.el_description != '﻿ ' and all_objects_eventtaglist[i].etl_id_event.el_description != '':
                        event += 'Описание:\n' + all_objects_eventtaglist[i].etl_id_event.el_description + '\n\n'

                    event += 'Дата:\n' + str(all_objects_eventtaglist[i].etl_id_event.el_date.date())

                    if str(all_objects_eventtaglist[i].etl_id_event.el_time) != '00:00:00' and \
                            all_objects_eventtaglist[i].etl_id_event.el_time is not None:
                        event += '\nВремя:\n' + str(all_objects_eventtaglist[i].etl_id_event.el_time)
                    else:
                        event += '\nВремя:\n' + str(all_objects_eventtaglist[i].etl_id_event.el_date.time())

                    if all_objects_eventtaglist[i].etl_id_event.el_link != '':
                        event += '\n\n' + 'Сайт:\n' + all_objects_eventtaglist[i].etl_id_event.el_link + '\n\n'

                    if all_objects_eventtaglist[i].etl_id_event.el_id_place is not None:
                        place = 'Где это находится:\n' + 'Город: ' + all_objects_eventtaglist[i].etl_id_event.el_id_place.pl_city + '\n' \
                        + 'Улица: ' + all_objects_eventtaglist[i].etl_id_event.el_id_place.pl_str_name + '\n' + 'Дом: ' + \
                        str(all_objects_eventtaglist[i].etl_id_event.el_id_place.pl_house_num) + '\n'
                        if all_objects_eventtaglist[i].etl_id_event.el_id_place.pl_letter is not None:
                            place += 'Буква дома: ' + all_objects_eventtaglist[i].etl_id_event.el_id_place.pl_letter + '\n'
                        if all_objects_eventtaglist[i].etl_id_event.el_id_place.pl_place_name is not None:
                            place += 'Название места проведения: ' + all_objects_eventtaglist[i].etl_id_event.el_id_place.pl_place_name + '\n'

                        event += place

                    repeat_events.append(all_objects_eventtaglist[i].etl_id_event.el_id)
                    events_alive = True
                    bot.send_message(message.chat.id, event)
            if not events_alive:
                bot.send_message(message.chat.id, 'Мы не нашли эвенты для Вас :(')
        else:
            bot.send_message(message.chat.id, 'Вы не указали теги')


def autosending_events():
    if datetime.datetime.today().time().strftime('%H:%M') == '12:00' and datetime.datetime.today().date().isoweekday() == 7:
        # print('aaa')
        all_objects_eventtaglist = Eventtaglist.objects.all()
        all_objects_userlist = Userlist.objects.all()
        all_objects_usertaglist = Usertaglist.objects.all()
        # user_tg_id = []
        for i in range(len(all_objects_userlist)):
            tags = []
            if all_objects_userlist[i].ul_linktgmessage is not None:
                for j in range(len(all_objects_usertaglist)):
                    if all_objects_userlist[i].ul_id == all_objects_usertaglist[j].utl_id_user.ul_id:
                        tags.append(all_objects_usertaglist[j].utl_id_tag.tl_title)
            if tags:
                repeat_events = []
                events_alive = False
                for j in range(len(all_objects_eventtaglist)):
                    if all_objects_eventtaglist[j].etl_id_tag.tl_title in tags and all_objects_eventtaglist[j].etl_id_event.el_id not in repeat_events \
                            and all_objects_eventtaglist[j].etl_id_event.el_date.date() >= datetime.datetime.today().date():
                        event = all_objects_eventtaglist[j].etl_id_event.el_title + '\n\n'

                        if all_objects_eventtaglist[j].etl_id_event.el_description != '﻿ ' and all_objects_eventtaglist[i].etl_id_event.el_description != '':
                            event += 'Описание:\n' + all_objects_eventtaglist[j].etl_id_event.el_description + '\n\n'

                        event += 'Дата:\n' + str(all_objects_eventtaglist[j].etl_id_event.el_date.date())

                        if str(all_objects_eventtaglist[j].etl_id_event.el_time) != '00:00:00' and \
                                all_objects_eventtaglist[j].etl_id_event.el_time is not None:
                            event += '\nВремя:\n' + str(all_objects_eventtaglist[j].etl_id_event.el_time)
                        else:
                            event += '\nВремя:\n' + str(all_objects_eventtaglist[j].etl_id_event.el_date.time())

                        if all_objects_eventtaglist[j].etl_id_event.el_link != '':
                            event += '\n\n' + 'Сайт:\n' + all_objects_eventtaglist[j].etl_id_event.el_link + '\n\n'

                        if all_objects_eventtaglist[j].etl_id_event.el_id_place is not None:
                            place = 'Где это находится:\n' + 'Город: ' + all_objects_eventtaglist[j].etl_id_event.el_id_place.pl_city + '\n' \
                            + 'Улица: ' + all_objects_eventtaglist[j].etl_id_event.el_id_place.pl_str_name + '\n' + 'Дом: ' + \
                            str(all_objects_eventtaglist[j].etl_id_event.el_id_place.pl_house_num) + '\n'
                            if all_objects_eventtaglist[j].etl_id_event.el_id_place.pl_letter is not None:
                                place += 'Буква дома: ' + all_objects_eventtaglist[j].etl_id_event.el_id_place.pl_letter + '\n'
                            if all_objects_eventtaglist[j].etl_id_event.el_id_place.pl_place_name is not None:
                                place += 'Название места проведения: ' + all_objects_eventtaglist[j].etl_id_event.el_id_place.pl_place_name + '\n'

                            event += place

                        repeat_events.append(all_objects_eventtaglist[j].etl_id_event.el_id)
                        events_alive = True
                        bot.send_message(all_objects_userlist[i].ul_linktgmessage, event)
                if not events_alive:
                    bot.send_message(all_objects_userlist[i].ul_linktgmessage, 'Мы не нашли эвенты для Вас :(')


@bot.message_handler(commands=['change_tags'])
def change_tags(message):

    # Клавиатура
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Добавить')
    # item2 = types.KeyboardButton('Удалить')
    # markup.add(item1, item2)

    all_objects_userlist = Userlist.objects.all()
    exist_user = False
    for i in range(len(all_objects_userlist)):
        if str(message.chat.id) == all_objects_userlist[i].ul_linktgmessage:
            tags = ''
            num_of_tag = 0
            all_objects_usertaglist = Usertaglist.objects.all()
            for j in range(len(all_objects_usertaglist)):
                if all_objects_userlist[i].ul_id == all_objects_usertaglist[j].utl_id_user.ul_id:
                    num_of_tag += 1
                    # print(all_objects_usertaglist[j].utl_id_tag.tl_title)
                    tags += str(num_of_tag) + ') ' + \
                            all_objects_usertaglist[j].utl_id_tag.tl_title + '\n'
            if tags != '':
                item2 = types.KeyboardButton('Удалить')
                markup.add(item1, item2)
                bot.send_message(message.chat.id, f'Ваши теги: \n{tags}', reply_markup=markup)
            else:
                markup.add(item1)
                bot.send_message(message.chat.id, 'У вас нет тегов', reply_markup=markup)
            exist_user = True
    if not exist_user:
        bot.send_message(message.chat.id, 'Вы не зарегистрированы на нашем сайте')
    bot.register_next_step_handler(message, add_del_tags)


def tags_without_usertags(message, tags_or_usertags):
    all_objects_taglist = Taglist.objects.all()
    all_objects_usertaglist = Usertaglist.objects.all()
    all_objects_userlist = Userlist.objects.all()
    tags = {}
    user_tags = {}
    for i in range(len(all_objects_userlist)):
        if str(message.chat.id) == all_objects_userlist[i].ul_linktgmessage:
            for j in range(len(all_objects_usertaglist)):
                if all_objects_userlist[i].ul_id == all_objects_usertaglist[j].utl_id_user.ul_id:
                    user_tags[all_objects_usertaglist[j].utl_id_tag.tl_id] = all_objects_usertaglist[j].utl_id_tag.tl_title
    for i in range(len(all_objects_taglist)):
        if all_objects_taglist[i].tl_title not in user_tags.values():
            tags[all_objects_taglist[i].tl_id] = all_objects_taglist[i].tl_title

    if tags_or_usertags == 'tags':
        return tags
    elif tags_or_usertags == 'usertags':
        return user_tags


# @bot.message_handler(content_types=['text'])
def add_del_tags(message):
    if message.text.lower() == 'добавить':
        tags = tags_without_usertags(message, 'tags')

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Готово')
        for i in range(len(tags.keys()) // 2):
            markup.add(tags[list(tags.keys())[i]], tags[list(tags.keys())[-i-1]])
        if len(tags.keys()) - len(tags.keys()) // 2 != len(tags.keys()) // 2:
            markup.add(tags[list(tags.keys())[len(tags.keys()) // 2]])
        bot.send_message(message.chat.id, 'Добавьте нужные теги. Список с тэгами можно листать', reply_markup=markup)

        bot.register_next_step_handler(message, add_tags)
    elif message.text.lower() == 'удалить':
        tags = tags_without_usertags(message, 'usertags')

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Готово')
        for i in range(len(tags.keys()) // 2):
            markup.add(tags[list(tags.keys())[i]], tags[list(tags.keys())[-i-1]])
        if len(tags.keys()) - len(tags.keys()) // 2 != len(tags.keys()) // 2:
            markup.add(tags[list(tags.keys())[len(tags.keys()) // 2]])
        bot.send_message(message.chat.id, 'Удалите ненужные теги. Список с тэгами можно листать', reply_markup=markup)

        bot.register_next_step_handler(message, del_tags)


def add_tags(message):
    tags = tags_without_usertags(message, 'tags')
    all_objects_userlist = Userlist.objects.all()
    if message.text in tags.values():
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Готово')
        del_tag = None
        internal_user_id = None  # id юзера в бд (не id тг чата)
        for i in tags.keys():
            if tags[i] == message.text:
                del_tag = i

        for i in range(len(all_objects_userlist)):
            if str(message.chat.id) == all_objects_userlist[i].ul_linktgmessage:
                internal_user_id = all_objects_userlist[i].ul_id
        new_tag = Usertaglist(utl_id_user=Userlist.objects.get(ul_id=internal_user_id), utl_id_tag=Taglist.objects.get(tl_id=del_tag))
        new_tag.save()

        del tags[del_tag]
        for i in range(len(tags.keys()) // 2):
            markup.add(tags[list(tags.keys())[i]], tags[list(tags.keys())[-i-1]])
        if len(tags.keys()) - len(tags.keys()) // 2 != len(tags.keys()) // 2:
            markup.add(tags[list(tags.keys())[len(tags.keys()) // 2]])
        bot.send_message(message.chat.id, f'Тэг {message.text} добавлен', reply_markup=markup)
        bot.register_next_step_handler(message, add_tags)

    if message.text == 'Готово':
        hide_markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Изменения сохранены', reply_markup=hide_markup)


def del_tags(message):
    tags = tags_without_usertags(message, 'usertags')
    all_objects_userlist = Userlist.objects.all()
    if message.text in tags.values():
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Готово')
        del_tag = None
        internal_user_id = None  # id юзера в бд (не id тг чата)
        for i in tags.keys():
            if tags[i] == message.text:
                del_tag = i

        for i in range(len(all_objects_userlist)):
            if str(message.chat.id) == all_objects_userlist[i].ul_linktgmessage:
                internal_user_id = all_objects_userlist[i].ul_id

        del_user_tag = Usertaglist.objects.get(utl_id_user=internal_user_id, utl_id_tag=del_tag)
        del_user_tag.delete()

        del tags[del_tag]
        for i in range(len(tags.keys()) // 2):
            markup.add(tags[list(tags.keys())[i]], tags[list(tags.keys())[-i-1]])
        if len(tags.keys()) - len(tags.keys()) // 2 != len(tags.keys()) // 2:
            markup.add(tags[list(tags.keys())[len(tags.keys()) // 2]])
        bot.send_message(message.chat.id, f'Тэг {message.text} удалён', reply_markup=markup)
        bot.register_next_step_handler(message, del_tags)

    if message.text == 'Готово':
        hide_markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Изменения сохранены', reply_markup=hide_markup)


# bot.send_message(484231880, 'Ахахахихихи Артем лох')
def sleeper(n, name):
    while True:
        autosending_events()
        time.sleep(n)
        # print(datetime.datetime.today().time().strftime('%H:%M:%S'))


thread = threading.Thread(target=sleeper, name='Thread1', args=(60, 'Thread1'))
thread.start()




