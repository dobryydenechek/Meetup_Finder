import telebot
from telebot import apihelper
from django.core.management.base import BaseCommand
from django.conf import settings
from ...models import Eventlist, Userlist, Taglist, Usertaglist, Eventtaglist
import datetime

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


@bot.message_handler(commands=['start'])
def start_message(message):
    # print(message.chat.username)
    all_objects_userlist = Userlist.objects.all()
    exist_user = False
    for i in range(len(all_objects_userlist)):
        if str(message.chat.id) == all_objects_userlist[i].ul_linktgmessage:
            bot.send_message(message.chat.id, 'С возвращением, друг! ')
            exist_user = True
    if not exist_user:
        bot.send_message(message.chat.id, 'Привет, друг! Введи свой id с сайта, чтобы мы слогли подключить бота')
        bot.register_next_step_handler(message, send_id)


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
def id_on_the_site(message):
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


@bot.message_handler(commands=['link', 'account', 'change_tags', 'options'])
def site_link(message):
    bot.send_message(message.chat.id, 'Ссылка на сайт: ')


@bot.message_handler(commands=['events'])
def events(message):
    all_objects_userlist = Userlist.objects.all()
    all_objects_eventlist = Eventlist.objects.all()
    all_objects_eventtaglist = Eventtaglist.objects.all()
    all_objects_userlist = Userlist.objects.all()
    all_objects_usertaglist = Usertaglist.objects.all()
    exist_user = False
    tags = []
    for i in range(len(all_objects_userlist)):
        if str(message.chat.id) == all_objects_userlist[i].ul_linktgmessage:
            user_id = all_objects_userlist[i].ul_id
            for j in range(len(all_objects_usertaglist)):
                if all_objects_userlist[i].ul_id == all_objects_usertaglist[j].utl_id_user.ul_id:
                    tags.append(all_objects_usertaglist[j].utl_id_tag.tl_title)
            exist_user = True
    if not exist_user:
        bot.send_message(message.chat.id, 'Вы не зарегистрированы на нашем сайте')
    else:
        if tags:
            repeat_events = []
            for i in range(len(all_objects_eventtaglist)):
                if all_objects_eventtaglist[i].etl_id_tag.tl_title in tags and all_objects_eventtaglist[i].etl_id_event.el_id not in repeat_events:
                    event = all_objects_eventtaglist[i].etl_id_event.el_title + '\n\n' + 'Описание:\n' \
                    + all_objects_eventtaglist[i].etl_id_event.el_description + '\n\n' + 'Дата и время проведения:\n' \
                    + str(all_objects_eventtaglist[i].etl_id_event.el_date)
                    if str(all_objects_eventtaglist[i].etl_id_event.el_time) != '00:00:00':
                        event += '\nВремя:\n' + str(all_objects_eventtaglist[i].etl_id_event.el_time)
                    if all_objects_eventtaglist[i].etl_id_event.el_link != '':
                        event += '\n\n' + 'Сайт:\n' + all_objects_eventtaglist[i].etl_id_event.el_link + '\n\n'

                    place = 'Где это находится:\n' + 'Город: ' + all_objects_eventtaglist[i].etl_id_event.el_id_place.pl_city + '\n' \
                    + 'Улица: ' + all_objects_eventtaglist[i].etl_id_event.el_id_place.pl_str_name + '\n' + 'Дом: ' + \
                    str(all_objects_eventtaglist[i].etl_id_event.el_id_place.pl_house_num) + '\n'
                    if all_objects_eventtaglist[i].etl_id_event.el_id_place.pl_letter is not None:
                        place += 'Буква дома: ' + all_objects_eventtaglist[i].etl_id_event.el_id_place.pl_letter + '\n'
                    if all_objects_eventtaglist[i].etl_id_event.el_id_place.pl_place_name is not None:
                        place += 'Название места проведения: ' + all_objects_eventtaglist[i].etl_id_event.el_id_place.pl_place_name + '\n'

                    event += place
                    repeat_events.append(all_objects_eventtaglist[i].etl_id_event.el_id)
                    bot.send_message(message.chat.id, event)

        else:
            bot.send_message(message.chat.id, 'Вы не указали теги')


# bot.send_message(484231880, 'Ахахахихихи Артем лох')




