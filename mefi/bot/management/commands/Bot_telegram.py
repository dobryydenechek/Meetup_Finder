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

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Добро пожаловать в meetup_finder\n'
                                      'Благодаря нашему боту вы сможете получать список нужных вам мероприятий, проходящих в Ростове-на-Дону\n'
                                      'Так же вы подписались на рассылку (она проходит каждый понедельник в 12 часов)\n'
                                      'Чтобы отписаться просто зайдите в меню "Настройки" и отключите все дни недели, так же в этом меню вы можете настроить время в которое будете получать рассылку\n'
                                      'В меню "Тэги" можно будет посмотреть и поменять выбранные вами тэги\n'
                                      'В будущем мы добавим напоминание о мероприятиях\n')


def button_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.InlineKeyboardButton(text='Ивенты', callback_data='/events'))
    markup.add(types.InlineKeyboardButton(text='Теги', callback_data='/tags'))
    markup.add(types.InlineKeyboardButton(text='Настройки', callback_data='/options'))
    markup.add(types.InlineKeyboardButton(text='Ссылка на сайт', callback_data='/link'))
    return markup


@bot.message_handler(content_types=['text'])
def message_handler(message):
    if message.text.lower() == "/start" or message.text.lower() == "старт" or message.text.lower() == "начать" or message.text.lower() == "привет" or message.text.lower() == "привет!":
        start_message(message)
    # ----Подменю тэгов-----#
    elif message.text.lower() == "/tags" or message.text.lower() == "теги":
        bot.send_message(message.chat.id, "Выберите настройку", reply_markup=tags_menu())
    elif message.text.lower() == 'изменить мои тэги':
        change_tags(message)
    elif message.text.lower() == "посмотреть мои тэги":
        show_tags(message)
    # ----Подменю тэгов-----#
    # ----Подменю настроек-----#
    elif message.text.lower() == 'настройки':
        bot.send_message(message.chat.id, "Выберите настройку", reply_markup=options())
    elif message.text.lower() == 'изменить время':
        change_time(message)
    elif message.text.lower() == 'изменить дни недели':
        day_change(message)
    # ----Подменю настроек-----#
    elif message.text.lower() == "/link" or message.text.lower() == "/account" or message.text.lower() == "/options" or message.text.lower() == "ссылка на сайт":
        site_link(message)
    elif message.text.lower() == "/events" or message.text.lower() == "ивенты":
        events(message)
    elif message.text.lower() == "в главное меню":
        bot.send_message(message.chat.id, 'Перехожу в главное меню', reply_markup=button_menu())
    else:
        bot.send_message(message.chat.id, 'Произошла ошибка, давай сделаем вид, что этого не было. Перехожу в главное меню', reply_markup=button_menu())


# @bot.message_handler(commands=['start'])
def start_message(message):
    
    all_objects_userlist = Userlist.objects.all()
    exist_user = False
    for i in range(len(all_objects_userlist)):
        if str(message.chat.id) == all_objects_userlist[i].ul_linktgmessage:
            bot.send_message(message.chat.id, 'С возвращением, друг! ', reply_markup=button_menu())
            exist_user = True
    if not exist_user:
        #---Создание клавиатуры---
        new_user = Userlist(ul_linktgmessage=message.chat.id, ul_mailing_time='12', ul_mailing_days='1')
        new_user.save()

        all_objects_userlist = Userlist.objects.get(ul_linktgmessage=message.chat.id)

        tags = ''
        num_of_tag = 0
        all_objects_usertaglist = Usertaglist.objects.all()
        for j in range(len(all_objects_usertaglist)):
            if all_objects_userlist.ul_id == all_objects_usertaglist[j].utl_id_user.ul_id:
                num_of_tag += 1
                tags += str(num_of_tag) + ') ' + \
                        all_objects_usertaglist[j].utl_id_tag.tl_title + '\n'

        tags = tags_without_usertags(message, 'tags')

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Готово')

        for i in range(0, len(tags.keys()), 2):
            rev_tag_title = {}
            for k, v in tag_title.items():
                rev_tag_title[v] = rev_tag_title.get(v, []) + [k]

            str1 = ''.join(tags[list(tags.keys())[i]])
            str2 = ''.join(tags[list(tags.keys())[i + 1]])
            print(str1, str2)
            markup.add(str1, str2)
        if len(tags.keys()) - len(tags.keys()) // 2 != len(tags.keys()) // 2:
            markup.add(str2)

        #---Создание клавиатуры---
        help(message)
        bot.send_message(message.chat.id, 'Привет, чтобы получать список нужных тебе мероприятий каждую неделю тебе нужно выбрать тэги, которые тебе подходят', reply_markup=markup)
        bot.register_next_step_handler(message, add_tags)

def send_id(message):
    id_in_base = False
    all_objects_userlist = Userlist.objects.all()
    for i in range(len(all_objects_userlist)):
        # print(all_objects[i].ul_id)
        if message.text == str(all_objects_userlist[i].ul_id):
            # print('Success!')
            all_objects_userlist[i].ul_linktgmessage = message.chat.id
            all_objects_userlist[i].save()
            bot.send_message(message.chat.id, 'Телеграм-аккаунт подключен к рассылке', reply_markup=button_menu())
            id_in_base = True
    if not id_in_base:
        bot.send_message(message.chat.id, 'Мы не нашли ваш id в базе данных', reply_markup=button_menu())


# @bot.message_handler(commands=['id'])
def id_on_the_site(message):
    exist_user = False
    all_objects_userlist = Userlist.objects.all()
    for i in range(len(all_objects_userlist)):
        if str(message.chat.id) == all_objects_userlist[i].ul_linktgmessage:
            bot.send_message(message.chat.id, f'Ваш id на сайте: {all_objects_userlist[i].ul_id}')
            bot.register_next_step_handler(message, choose_option)
            exist_user = True
    if not exist_user:
        bot.send_message(message.chat.id, 'Вы не зарегистрированы на нашем сайте', reply_markup=button_menu())

# @bot.message_handler(commands=['/tags'])
def tags_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('В главное меню')
    markup.add('Посмотреть мои тэги', 'Изменить мои тэги')
    markup.add('Что означают тэги?')
    print(130)
    return markup

# def tags(message):
#     bot.send_message(message.chat.id, 'Выберите настройку', reply_markup=tags_menu())
#     print("---------------------------")
#     print(message.text)
#     print("---------------------------")
#     print(message)
#     if message.text.lower() == 'посмотреть мои тэги':
#         show_tags(message)
#     elif message.text.lower() == 'изменить мои тэги':
#         change_tags(message)
#     elif message.text.lower() == 'в главное меню':
#         bot.send_message(message.chat.id, 'Готово', reply_markup=button_menu())
#     else:
#         bot.send_message(message.chat.id, 'Это не один из вариантов меню')
#         bot.register_next_step_handler(message, tags)

# @bot.message_handler(commands=['tags'])
def show_tags(message):
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
                bot.send_message(message.chat.id, f'Ваши теги: \n{tags}', reply_markup=tags_menu())
            else:
                bot.send_message(message.chat.id, 'Вы не указали теги', reply_markup=tags_menu())
            exist_user = True
    if not exist_user:
        bot.send_message(message.chat.id, 'Вы не зарегистрированы на нашем сайте', reply_markup=button_menu())


# @bot.message_handler(commands=['link', 'account', 'options'])
def site_link(message):
    bot.send_message(message.chat.id, 'Ссылка на сайт: https://project2205235.tilda.ws/', reply_markup=button_menu())


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
        bot.send_message(message.chat.id, 'Вы не зарегистрированы на нашем сайте', reply_markup=button_menu())
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
                    bot.send_message(message.chat.id, event, reply_markup=button_menu())
            if not events_alive:
                bot.send_message(message.chat.id, 'Мы не нашли эвенты для Вас :(', reply_markup=button_menu())
        else:
            bot.send_message(message.chat.id, 'Вы не указали теги')
            change_tags(message)

@bot.message_handler(commands=['change_tags'])
def change_tags(message):

    # Клавиатура
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Добавить')
    # item2 = types.KeyboardButton('Удалить')
    # markup.add(item1, item2)

    all_objects_userlist = Userlist.objects.all()
    exist_user = False
    global tag_title
    tag_title = dict(
        Безопасность = 'Безопасность',
        Бэк= 'Backend',
        АдминистрированиеиDevOps='Системное администрирование',
        HardиIoT= 'Hard и IoT',
        Аналитикаиdatascience = 'Аналитика и data science',
        Фронт ='Frontend',
        Процессы= 'Командные процессы',
        QA='Тестирование(QA)',
        Mobile= 'Mobile',
        Продукт='Project Product',
        Геймдев='Геймдев',
        Карьера= 'Карьера',
        Роботы='Роботы',
        Клиенты='Клиенты',
    )
    for i in range(len(all_objects_userlist)):
        if str(message.chat.id) == all_objects_userlist[i].ul_linktgmessage:
            tags = ''
            num_of_tag = 0
            all_objects_usertaglist = Usertaglist.objects.all()
            for j in range(len(all_objects_usertaglist)):
                print(all_objects_usertaglist[j].utl_id_tag.tl_id)
                if all_objects_userlist[i].ul_id == all_objects_usertaglist[j].utl_id_user.ul_id:
                    num_of_tag += 1
                    tags += str(num_of_tag) + ') ' + \
                            tag_title[all_objects_usertaglist[j].utl_id_tag.tl_title.replace(' ', '')] + '\n'
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
                    user_tags[all_objects_usertaglist[j].utl_id_tag.tl_id] = tag_title[all_objects_usertaglist[j].utl_id_tag.tl_title.replace(' ', '')]
    for i in range(len(all_objects_taglist)):
        if all_objects_taglist[i].tl_title not in user_tags.values():
            tags[all_objects_taglist[i].tl_id] = tag_title[all_objects_taglist[i].tl_title.replace(' ', '')]

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
        for i in range(0, len(tags.keys()), 2):
            print(i, i+1, len(tags.keys()))
            print(len(tags.keys()) - (i + 1) ==0)
            rev_tag_title = {}
            for k, v in tag_title.items():
                rev_tag_title[v] = rev_tag_title.get(v, []) + [k]

            str1 = ''.join(tags[list(tags.keys())[i]])
            print(tags[list(tags.keys())[i]])
            if (len(tags.keys()) - (i + 1) == 0):
                markup.add(str1)
            else:
                str2 = ''.join(tags[list(tags.keys())[i + 1]])
                markup.add(str1, str2)
        bot.send_message(message.chat.id, 'Добавьте нужные теги. Список с тэгами можно листать', reply_markup=markup)

        bot.register_next_step_handler(message, add_tags)
    elif message.text.lower() == 'удалить':
        tags = tags_without_usertags(message, 'usertags')

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Готово')
        for i in range(0, len(tags.keys()), 2):

            rev_tag_title = {}
            for k, v in tag_title.items():
                rev_tag_title[v] = rev_tag_title.get(v, []) + [k]

            str1 = ''.join(tags[list(tags.keys())[i]])
            if (len(tags.keys()) - (i+1) == 0):
                markup.add(str1)
            else:
                str2 = ''.join(tags[list(tags.keys())[i + 1]])
                markup.add(str1, str2)
        bot.send_message(message.chat.id, 'Удалите ненужные теги. Список с тэгами можно листать', reply_markup=markup)

        bot.register_next_step_handler(message, del_tags)
    elif message.text.lower() == 'в тэги':
        bot.send_message(message.chat.id, 'Ваши тэги не изменились', reply_markup=tags_menu())
    else:
        bot.send_message(message.chat.id, 'Произошла ошибка, давай сделаем вид, что этого не было. Перехожу в главное меню', reply_markup=button_menu())



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
        # hide_markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Изменения сохранены', reply_markup=tags_menu())


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
        # hide_markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Изменения сохранены', reply_markup=tags_menu())


def options():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('В главное меню')
    markup.add('Изменить время','Изменить дни недели')
    markup.add(types.InlineKeyboardButton(text='Мой id', callback_data='/id'))
    return markup

def show_days(message):
    print(382)
    user = Userlist.objects.get(ul_linktgmessage = message.chat.id)
    user_days = []

    for i in range(len(str(user.ul_mailing_days))):
        if user.ul_mailing_days != None:
            user_days.append(int(str(user.ul_mailing_days)[len(str(user.ul_mailing_days)) - i - 1:len(str(user.ul_mailing_days)) - i ]))

    days = {1 : 'Понедельник', 2 : 'Вторник', 3 : 'Среда', 4 : 'Четверг', 5 : 'Пятница', 6 : 'Суббота', 7 : 'Воскресенье'}

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if message.text.lower() == 'изменить дни недели':
        markup.add('В настройки')
    else:
        markup.add('Готово')

    for i in range(1, len(days) + 1):
        if list(days.keys())[i - 1] in user_days:
            markup.add('✅ ' + str(days[i]) + ' ✅')
        else:
            markup.add('❌ ' + str(days[i]) + ' ❌')
    return markup



def day_change(message):
    days = {'Понедельник' : 1, 
            'Вторник' : 2, 
            'Среда' : 3, 
            'Четверг' : 4, 
            'Пятница' : 5, 
            'Суббота' : 6, 
            'Воскресенье' : 7}

    if message.text.lower() == 'готово':
        bot.send_message(message.chat.id, 'Изменения сохранены', reply_markup=options())
    elif message.text.lower() == 'в настройки':
        bot.send_message(message.chat.id, 'Выбранные дни для рассылки не изменились', reply_markup=options())

    elif message.text[2 : len(message.text) - 2] in list(days): #если сообщение равно одному из дней недели
        user = Userlist.objects.get(ul_linktgmessage=message.chat.id)
        user_days = []

        if user.ul_mailing_days == None:
            user.ul_mailing_days = ""
            user.save()

        for i in range(len(str(user.ul_mailing_days))):
            user_days.append(int(str(user.ul_mailing_days)[len(str(user.ul_mailing_days)) - i - 1:len(str(user.ul_mailing_days)) - i ]))  #обращаемся к бд и разбиваем строку на отдельные символы
        print(user_days)    
        if days[message.text[2 : len(message.text) - 2]] in user_days: #формируем новый список дней пользователя
            user_days.remove(days[message.text[2 : len(message.text) - 2]])
            ans = f'удалили {message.text[2 : len(message.text) - 2]}'
        else:
            ans = f'добавили {message.text[2 : len(message.text) - 2]}'
            user_days.append(days[message.text[2 : len(message.text) - 2]])

        print(user_days)
        new_days=''
        for i in user_days:# формируем новую строку из отдельных символов
            new_days += str(i)

        user = Userlist.objects.get(ul_linktgmessage=message.chat.id)
        user.ul_mailing_days = new_days
        user.save()
        #отображаем новую клавиатуру
        markup = show_days(message)
        bot.send_message(message.chat.id, f'Вы {ans}', reply_markup=markup)
        bot.register_next_step_handler(message,day_change)

    elif message.text.lower() == 'изменить дни недели':
        markup = show_days(message)
        bot.send_message(message.chat.id, 'Выбирите день для рассылки', reply_markup=markup)
        bot.register_next_step_handler(message,day_change)

    else:
        bot.send_message(message.chat.id, 'Нажимайте на кнопки')
        bot.register_next_step_handler(message,day_change)


def change_time(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        markup.add('В настройки')
        markup.add('00:00', '01:00', '02:00')
        markup.add('03:00', '04:00', '05:00')
        markup.add('06:00', '07:00', '08:00')
        markup.add('09:00', '10:00', '11:00')
        markup.add('12:00', '13:00', '14:00')
        markup.add('15:00', '16:00', '17:00')
        markup.add('18:00', '19:00', '20:00')
        markup.add('21:00', '22:00', '23:00')

        bot.send_message(message.chat.id, 'Выбирите время рассылки', reply_markup=markup)
        bot.register_next_step_handler(message, new_time)


def new_time(message):
    if message.text.lower() != 'в настройки':
        all_objects_userlist = Userlist.objects.get(ul_linktgmessage=message.chat.id) #Нынешний пользователь

        all_objects_userlist.ul_mailing_time = message.text[:2]
        all_objects_userlist.save()

        bot.send_message(message.chat.id, f'Следующая рассылка будет в {message.text}', reply_markup=options())
    else:
        bot.send_message(message.chat.id, 'Время рассылки не изменилось', reply_markup=options())