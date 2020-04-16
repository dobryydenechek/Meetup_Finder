from ...models import Eventlist, Userlist, Taglist, Usertaglist, Eventtaglist
from django.core.management.base import BaseCommand
import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
import random
import requests
import bs4
import pyowm
import os
import time


a = random.randint(0, 200000)

name = '5'
allid = [521574415, 544416745]
inwait = []
class Command(BaseCommand):
    help = 'вк-бот'

    def handle(self, *args, **options):
        token = "9a3bacad4b8ddf056532171ff562678143251178082472860aa6468283654cd8fa0aab54afbfada72dcc9"

        # Авторизуемся как сообщество
        vk = vk_api.VkApi(token=token)

        # Работа с сообщениями
        longpoll = VkLongPoll(vk)


#----------------------------------------

#@bot.message_handler(commands=['start'])
def start_message(message):
    # print(message.chat.username)
    all_objects_userlist = Userlist.objects.all()
    exist_user = False
    for i in range(len(all_objects_userlist)):
        if str(event.user_id) == all_objects_userlist[i].ul_linkvkmessage:
            _get_user_name_from_vk_id(event.user_id, 'С возвращением, друг!', a, keyboard=keyboard)
            exist_user = True
        if not exist_user:
            write_msg(event.user_id, 'Привет, друг! Введи свой id с сайта, чтобы мы слогли подключить бота', a)
            inwait.append(event.user_id)
            print(inwait)


def send_id(message):
    id_in_base = False
    all_objects_userlist = Userlist.objects.all()
    for i in range(len(all_objects_userlist)):
        # print(all_objects[i].ul_id)
        if message == str(all_objects_userlist[i].ul_id):
            # print('Success!')
            all_objects_userlist[i].ul_linkvkmessage = str(event.user_id)
            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! .chat.id

            all_objects_userlist[i].save()
            write_msg(event.user_id, 'vk-аккаунт подключен к рассылке', a, keyboard=keyboard)
            id_in_base = True
            inwait.remove(event.user_id)
    if not id_in_base:
        write_msg(event.user_id, 'Мы не нашли ваш id в базе данных', a)


#@bot.message_handler(commands=['id'])
def id_on_the_sitee(message):
    exist_user = False
    all_objects_userlist = Userlist.objects.all()
    for i in range(len(all_objects_userlist)):
        if str(message) == str(all_objects_userlist[i].ul_linkvkmessage):
            write_msg(event.user_id, f'Ваш id на сайте: {all_objects_userlist[i].ul_id}', a, keyboard=keyboard)
            exist_user = True
    if not exist_user:
        write_msg(event.user_id, 'Вы не зарегистрированы на нашем сайте', a)


#@bot.message_handler(commands=['tags'])
def id_on_the_site(message):
    all_objects_userlist = Userlist.objects.all()
    exist_user = False
    for i in range(len(all_objects_userlist)):
        if str(message) == str(all_objects_userlist[i].ul_linkvkmessage):
            tags = ''
            num_of_tag = 0
            all_objects_usertaglist = Usertaglist.objects.all()
            for j in range(len(all_objects_usertaglist)):
                if all_objects_userlist[i].ul_id == all_objects_usertaglist[j].utl_id_user.ul_id:
                    num_of_tag += 1
                    print(all_objects_usertaglist[j].utl_id_tag.tl_title)
                    tags += str(num_of_tag) + ') ' + \
                            all_objects_usertaglist[j].utl_id_tag.tl_title + '\n'
            write_msg(event.user_id, f'Ваши теги: \n{tags}', a, keyboard=keyboard)
            exist_user = True
    if not exist_user:
        write_msg(event.user_id, 'Вы не зарегистрированы на нашем сайте', a)


#@bot.message_handler(commands=['link', 'account', 'change_tags', 'options'])
def site_link(message):
    write_msg(event.user_id, 'Ссылка на сайт: ', a, keyboard=keyboard)


#@bot.message_handler(commands=['events'])
def events(message):
    all_objects_eventtaglist = Eventtaglist.objects.all()
    all_objects_userlist = Userlist.objects.all()
    all_objects_usertaglist = Usertaglist.objects.all()
    exist_user = False
    tags = []
    for i in range(len(all_objects_userlist)):
        if str(message) == str(all_objects_userlist[i].ul_linkvkmessage):
            for j in range(len(all_objects_usertaglist)):
                if all_objects_userlist[i].ul_id == all_objects_usertaglist[j].utl_id_user.ul_id:
                    tags.append(all_objects_usertaglist[j].utl_id_tag.tl_title)
            exist_user = True
    if not exist_user:
        write_msg(event.user_id, 'Вы не зарегистрированы на нашем сайте', a)
    else:
        if tags:
            repeat_events = []
            for i in range(len(all_objects_eventtaglist)):
                if all_objects_eventtaglist[i].etl_id_tag.tl_title in tags and all_objects_eventtaglist[
                    i].etl_id_event.el_id not in repeat_events:
                    event1 = all_objects_eventtaglist[i].etl_id_event.el_title + '\n\n' + 'Описание:\n' \
                            + all_objects_eventtaglist[i].etl_id_event.el_description + '\n\n' + 'Дата:\n' \
                            + str(all_objects_eventtaglist[i].etl_id_event.el_date.date())
                    if str(all_objects_eventtaglist[i].etl_id_event.el_time) != '00:00:00':
                        event1 += '\nВремя:\n' + str(all_objects_eventtaglist[i].etl_id_event.el_time)
                    if all_objects_eventtaglist[i].etl_id_event.el_link != '':
                        event1 += '\n\n' + 'Сайт:\n' + all_objects_eventtaglist[i].etl_id_event.el_link + '\n\n'

                    place = 'Где это находится:\n' + 'Город: ' + all_objects_eventtaglist[
                        i].etl_id_event.el_id_place.pl_city + '\n' \
                            + 'Улица: ' + all_objects_eventtaglist[
                                i].etl_id_event.el_id_place.pl_str_name + '\n' + 'Дом: ' + \
                            str(all_objects_eventtaglist[i].etl_id_event.el_id_place.pl_house_num) + '\n'
                    if all_objects_eventtaglist[i].etl_id_event.el_id_place.pl_letter is not None:
                        place += 'Буква дома: ' + all_objects_eventtaglist[i].etl_id_event.el_id_place.pl_letter + '\n'
                    if all_objects_eventtaglist[i].etl_id_event.el_id_place.pl_place_name is not None:
                        place += 'Название места проведения: ' + all_objects_eventtaglist[
                            i].etl_id_event.el_id_place.pl_place_name + '\n'

                    event1 += place
                    repeat_events.append(all_objects_eventtaglist[i].etl_id_event.el_id)
                    write_msg(event.user_id, event1, a, keyboard=keyboard)

        else:
            write_msg(event.user_id, 'Вы не указали теги', a)

#--------------------------------------------------





def write_msg(user_id, message, a, keyboard=None):

    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': a, 'keyboard': keyboard})






token = "9a3bacad4b8ddf056532171ff562678143251178082472860aa6468283654cd8fa0aab54afbfada72dcc9"


vk = vk_api.VkApi(token=token)


longpoll = VkLongPoll(vk)



vk.method('messages.send', {'user_id': 286488661, 'message': 'Бот включен', 'random_id': a})

print('bot on')

keyboard = VkKeyboard(one_time=False)
keyboard.add_button('tags', color=VkKeyboardColor.POSITIVE)
keyboard.add_line()
keyboard.add_button('id', color=VkKeyboardColor.POSITIVE)
keyboard.add_line()
keyboard.add_button('events', color=VkKeyboardColor.POSITIVE)
keyboard.add_line()
keyboard.add_button('link', color=VkKeyboardColor.POSITIVE)
keyboard = keyboard.get_keyboard()

for event in longpoll.listen():

    # Если пришло новое сообщение
    if event.type == VkEventType.MESSAGE_NEW:

        # Если оно имеет метку для меня( то есть бота)
        if event.to_me:

            # Сообщение от пользователя
            request = event.text
            a = random.randint(0, 200000)



            if request.lower() == "старт" or request == "start" or request == "Начать":
                start_message(event.user_id)
                print(event.user_id, request)

            if request.lower() == "id":
                id_on_the_sitee(event.user_id)
                print(event.user_id, request)

            if request.lower() == "events":
                events(event.user_id)
                print(event.user_id, request)

            elif request.lower() == "tags":
                id_on_the_site(event.user_id)

                print(event.user_id, request)

            elif request.lower() == 'link':
                site_link(event.user_id)
                print(event.user_id, request)



            else:
                if event.user_id in inwait:
                    send_id(request)
                    print(event.user_id, request)

                else:
                    write_msg(event.user_id, "не понял, ну и похуй", a)
                    print(event.user_id, request)