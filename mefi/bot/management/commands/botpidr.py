from mefi_app.models import Eventlist, Userlist, Taglist, Usertaglist, Eventtaglist
from django.core.management.base import BaseCommand
import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
import random
import requests

import os
import time
import datetime


a = random.randint(0, 200000)

name = '5'
allid = [521574415, 544416745]
inwait1 = []
inwait2 = []
inwait3 = []
inwait4 = []
inwait5 = []
inwait6 = []
inwait7 = []
inwait8 = []
inwait9 = []
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

    all_objects_userlist = Userlist.objects.all()
    exist_user = False
    for i in range(len(all_objects_userlist)):
        if str(event.user_id) == all_objects_userlist[i].ul_linkvkmessage:
            write_msg(event.user_id, 'С возвращением, друг!', a, keyboard=keyboard)
            exist_user = True
    if exist_user == False:

        new_user = Userlist(ul_linkvkmessage=str(event.user_id))
        new_user.save()



        all_objects_userlist = Userlist.objects.all()
        exist_user = False
        for i in range(len(all_objects_userlist)):
            if str(event.user_id) == all_objects_userlist[i].ul_linkvkmessage:
                tags = ''
                num_of_tag = 0
                all_objects_usertaglist = Usertaglist.objects.all()
                for j in range(len(all_objects_usertaglist)):
                    if all_objects_userlist[i].ul_id == all_objects_usertaglist[j].utl_id_user.ul_id:
                        num_of_tag += 1
                        # print(all_objects_usertaglist[j].utl_id_tag.tl_title)
                        tags += str(num_of_tag) + ') ' + \
                                all_objects_usertaglist[j].utl_id_tag.tl_title + '\n'
        keyboard2 = VkKeyboard(one_time=False)
        keyboard2.add_button('добавить', color=VkKeyboardColor.POSITIVE)
        keyboard2 = keyboard2.get_keyboard()
        write_msg(event.user_id, 'Привет, друг! Чтобы начать пользоваться ботом, тебе нужно выбрать теги.', a,
                  keyboard=keyboard2)
        inwait1.append(event.user_id)



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
            #inwait.remove(event.user_id)
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


def change_tags(message):
    print("change")
    # Клавиатура


    # item2 = types.KeyboardButton('Удалить')
    # markup.add(item1, item2)

    all_objects_userlist = Userlist.objects.all()
    exist_user = False
    for i in range(len(all_objects_userlist)):
        if str(event.user_id) == all_objects_userlist[i].ul_linkvkmessage:
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
                keyboard2 = VkKeyboard(one_time=False)
                keyboard2.add_button('добавить', color=VkKeyboardColor.POSITIVE)
                keyboard2.add_line()
                keyboard2.add_button('удалить', color=VkKeyboardColor.POSITIVE)
                keyboard2 = keyboard2.get_keyboard()
                write_msg(event.user_id, f'Ваши теги: \n{tags}', a, keyboard=keyboard2)
            else:
                keyboard2 = VkKeyboard(one_time=False)
                keyboard2.add_button('добавить', color=VkKeyboardColor.POSITIVE)
                keyboard2 = keyboard2.get_keyboard()
                write_msg(event.user_id, 'У вас нет тегов', a, keyboard=keyboard2)
            exist_user = True
    if not exist_user:
        write_msg(event.user_id, 'Вы не зарегистрированы на нашем сайте', a)
    #add_del_tags(message)

    inwait1.append(event.user_id)




def tags_without_usertags(tags_or_usertags):
    all_objects_taglist = Taglist.objects.all()
    all_objects_usertaglist = Usertaglist.objects.all()
    all_objects_userlist = Userlist.objects.all()
    tags = {}
    user_tags = {}
    for i in range(len(all_objects_userlist)):
        if str(event.user_id) == all_objects_userlist[i].ul_linkvkmessage:
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
    if message.lower() == 'добавить':
        print("succes")
        tags = tags_without_usertags('tags')

        keyboard13 = VkKeyboard(one_time=False)
        keyboard13.add_button('Готово', color=VkKeyboardColor.POSITIVE)


        for i in range(len(tags.keys())):
            keyboard13.add_line()
            keyboard13.add_button(tags[list(tags.keys())[i]], color=VkKeyboardColor.POSITIVE)


        keyboard13 = keyboard13.get_keyboard()
        print("inwait1 ", inwait1)
        inwait1.remove(event.user_id)
        print("inwait1 ", inwait1)
        print("inwait2 ", inwait2)
        inwait2.append(event.user_id)
        print("inwait2 ", inwait2)
        write_msg(event.user_id, 'Добавьте нужные теги. Список с тэгами можно листать', a, keyboard=keyboard13)




    elif message.lower() == 'удалить':
        tags = tags_without_usertags('usertags')

        keyboard3 = VkKeyboard(one_time=False)
        keyboard3.add_button('Готово', color=VkKeyboardColor.POSITIVE)

        for i in range(len(tags.keys())):
            keyboard3.add_line()
            keyboard3.add_button(tags[list(tags.keys())[i]], color=VkKeyboardColor.POSITIVE)


        keyboard3 = keyboard3.get_keyboard()
        write_msg(event.user_id, 'Удалите ненужные теги. Список с тэгами можно листать', a, keyboard=keyboard3)

        inwait1.remove(event.user_id)
        inwait3.append(event.user_id)






def add_tags(message):
    print("add")
    tags = tags_without_usertags('tags')
    all_objects_userlist = Userlist.objects.all()

    if message in tags.values():
        keyboard3 = VkKeyboard(one_time=False)
        keyboard3.add_button('Готово', color=VkKeyboardColor.POSITIVE)

        del_tag = None
        internal_user_id = None  # id юзера в бд (не id тг чата)
        for i in tags.keys():
            if tags[i] == message:
                del_tag = i

        for i in range(len(all_objects_userlist)):
            if str(event.user_id) == all_objects_userlist[i].ul_linkvkmessage:
                internal_user_id = all_objects_userlist[i].ul_id

        new_tag = Usertaglist(utl_id_user=Userlist.objects.get(ul_id=internal_user_id), utl_id_tag=Taglist.objects.get(tl_id=del_tag))

        new_tag.save()

        del tags[del_tag]
        for i in range(len(tags.keys())):
            keyboard3.add_line()
            keyboard3.add_button(tags[list(tags.keys())[i]], color=VkKeyboardColor.POSITIVE)



        #if len(tags.keys()) - len(tags.keys()) // 2 != len(tags.keys()) // 2:
            #keyboard3.add_button(tags[list(tags.keys())[len(tags.keys()) // 2]], color=VkKeyboardColor.POSITIVE)
            #keyboard3.add_button("ЧЛЕН", color=VkKeyboardColor.POSITIVE)
            #keyboard3.add_line()

        keyboard3 = keyboard3.get_keyboard()

        write_msg(event.user_id, f'Тэг {message} добавлен', a, keyboard=keyboard3)


    if message == 'Готово':
        print("inwait2 ", inwait2)
        inwait2.remove(event.user_id)
        print("inwait2 ", inwait2)
        keyboard35 = VkKeyboard(one_time=False)
        keyboard35.add_button('tags', color=VkKeyboardColor.POSITIVE)
        keyboard35.add_line()
        keyboard35.add_button('change_tags', color=VkKeyboardColor.POSITIVE)
        keyboard35.add_line()
        keyboard35.add_button('id', color=VkKeyboardColor.POSITIVE)
        keyboard35.add_line()
        keyboard35.add_button('events', color=VkKeyboardColor.POSITIVE)
        keyboard35.add_line()
        keyboard35.add_button('link', color=VkKeyboardColor.POSITIVE)
        keyboard35 = keyboard35.get_keyboard()
        write_msg(event.user_id, 'Изменения сохранены', a, keyboard=keyboard35)


def del_tags(message):
    tags = tags_without_usertags('usertags')
    all_objects_userlist = Userlist.objects.all()
    if message in tags.values():

        keyboard3 = VkKeyboard(one_time=False)
        keyboard3.add_button('Готово', color=VkKeyboardColor.POSITIVE)



        del_tag = None
        internal_user_id = None  # id юзера в бд (не id тг чата)
        for i in tags.keys():
            if tags[i] == message:
                del_tag = i

        for i in range(len(all_objects_userlist)):
            if str(event.user_id) == all_objects_userlist[i].ul_linkvkmessage:
                internal_user_id = all_objects_userlist[i].ul_id

        del_user_tag = Usertaglist.objects.get(utl_id_user=internal_user_id, utl_id_tag=del_tag)
        del_user_tag.delete()

        del tags[del_tag]
        for i in range(len(tags.keys())):
            keyboard3.add_line()
            keyboard3.add_button(tags[list(tags.keys())[i]], color=VkKeyboardColor.POSITIVE)


        keyboard3 = keyboard3.get_keyboard()
        write_msg(event.user_id, f'Тэг {message} удалён', a, keyboard=keyboard3)


    if message == 'Готово':
        keyboard3 = VkKeyboard(one_time=False)
        keyboard3.add_button('tags', color=VkKeyboardColor.POSITIVE)
        keyboard3.add_line()
        keyboard3.add_button('change_tags', color=VkKeyboardColor.POSITIVE)
        keyboard3.add_line()
        keyboard3.add_button('id', color=VkKeyboardColor.POSITIVE)
        keyboard3.add_line()
        keyboard3.add_button('events', color=VkKeyboardColor.POSITIVE)
        keyboard3.add_line()
        keyboard3.add_button('link', color=VkKeyboardColor.POSITIVE)
        keyboard3 = keyboard3.get_keyboard()
        inwait3.remove(event.user_id)
        write_msg(event.user_id, 'Изменения сохранены', a, keyboard=keyboard3)










#@bot.message_handler(commands=['link', 'account', 'change_tags', 'options'])
def site_link(message):
    write_msg(event.user_id, 'Ссылка на сайт: ', a, keyboard=keyboard)


#@bot.message_handler(commands=['events'])
def events(message):
    # all_objects_userlist = Userlist.objects.all()
    # all_objects_eventlist = Eventlist.objects.all()
    all_objects_eventtaglist = Eventtaglist.objects.all()
    all_objects_userlist = Userlist.objects.all()
    all_objects_usertaglist = Usertaglist.objects.all()
    exist_user = False
    tags = []

    for i in range(len(all_objects_userlist)):
        if str(event.user_id) == all_objects_userlist[i].ul_linkvkmessage:
            for j in range(len(all_objects_usertaglist)):

                if all_objects_userlist[i].ul_id == all_objects_usertaglist[j].utl_id_user.ul_id:
                    tags.append(all_objects_usertaglist[j].utl_id_tag.tl_title)
            exist_user = True
    if not exist_user:
        write_msg(event.user_id, 'Вы не зарегистрированы на нашем сайте', a, keyboard=keyboard)
    else:
        if tags:
            repeat_events = []
            events_alive = False  # есть ли эвенты для пользователя
            print(all_objects_eventtaglist)
            print(all_objects_usertaglist)
            print(tags)
            for i in range(len(all_objects_eventtaglist)):

                if all_objects_eventtaglist[i].etl_id_tag.tl_title in tags and all_objects_eventtaglist[
                    i].etl_id_event.el_id not in repeat_events \
                        and all_objects_eventtaglist[i].etl_id_event.el_date.date() >= datetime.datetime.today().date():
                    event1 = all_objects_eventtaglist[i].etl_id_event.el_title + '\n\n'

                    if all_objects_eventtaglist[i].etl_id_event.el_description != '﻿ ':
                        event1 += 'Описание:\n' + all_objects_eventtaglist[i].etl_id_event.el_description + '\n\n'

                    event1 += 'Дата:\n' + str(all_objects_eventtaglist[i].etl_id_event.el_date.date())

                    if str(all_objects_eventtaglist[i].etl_id_event.el_time) != '00:00:00' and \
                            all_objects_eventtaglist[i].etl_id_event.el_time is not None:
                        event1 += '\nВремя:\n' + str(all_objects_eventtaglist[i].etl_id_event.el_time)
                    else:
                        event1 += '\nВремя:\n' + str(all_objects_eventtaglist[i].etl_id_event.el_date.time())

                    if all_objects_eventtaglist[i].etl_id_event.el_link != '':
                        event1 += '\n\n' + 'Сайт:\n' + all_objects_eventtaglist[i].etl_id_event.el_link + '\n\n'

                    if all_objects_eventtaglist[i].etl_id_event.el_id_place is not None:
                        place = 'Где это находится:\n' + 'Город: ' + all_objects_eventtaglist[
                            i].etl_id_event.el_id_place.pl_city + '\n' \
                                + 'Улица: ' + all_objects_eventtaglist[
                                    i].etl_id_event.el_id_place.pl_str_name + '\n' + 'Дом: ' + \
                                str(all_objects_eventtaglist[i].etl_id_event.el_id_place.pl_house_num) + '\n'
                        if all_objects_eventtaglist[i].etl_id_event.el_id_place.pl_letter is not None:
                            place += 'Буква дома: ' + all_objects_eventtaglist[
                                i].etl_id_event.el_id_place.pl_letter + '\n'
                        if all_objects_eventtaglist[i].etl_id_event.el_id_place.pl_place_name is not None:
                            place += 'Название места проведения: ' + all_objects_eventtaglist[
                                i].etl_id_event.el_id_place.pl_place_name + '\n'

                        event1 += place

                    repeat_events.append(all_objects_eventtaglist[i].etl_id_event.el_id)
                    events_alive = True
                    write_msg(event.user_id, event1, a, keyboard=keyboard)
            if not events_alive:
                write_msg(event.user_id, 'Мы не нашли эвенты для Вас :(', a, keyboard=keyboard)
        else:
            write_msg(event.user_id, 'Вы не указали теги', a, keyboard=keyboard)

#--------------------------------------------------


#-----------------------------------------------



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
keyboard.add_button('change_tags', color=VkKeyboardColor.POSITIVE)
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


            print(request)

            if request.lower() == "старт" or request.lower() == "start" or request == "Начать":
                start_message(event.user_id)

                print(event.user_id, request, "start")

            elif request.lower() == "change_tags":
                change_tags(event.user_id)
                print(event.user_id, request)

            elif request.lower() == "id":
                id_on_the_sitee(event.user_id)
                print(event.user_id, request)

            elif request.lower() == "events":
                events(event.user_id)
                print(event.user_id, request)

            elif request.lower() == "tags":
                id_on_the_site(event.user_id)

                print(event.user_id, request)

            elif request.lower() == 'link':
                site_link(event.user_id)
                print(event.user_id, request)


            else:
                if event.user_id in inwait1:
                    print("go")
                    add_del_tags(request)
                    print(event.user_id, request)
                elif event.user_id in inwait2:
                    add_tags(request)
                    print(event.user_id, request)
                elif event.user_id in inwait3:
                    del_tags(request)
                    print(event.user_id, request)

                else:
                    write_msg(event.user_id, "не понял, ну и похуй", a)
                    print(event.user_id, request, "krai")
