from ...models import Eventlist, Userlist, Taglist, Usertaglist, Eventtaglist
from django.core.management.base import BaseCommand
import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
import random
import datetime
import time



timecheck = datetime.datetime.now().strftime("%H")
timecheck = str(int(timecheck) + 3)

def write_msg(user_id, message, a, keyboard=None):
    a = random.randint(0, 200000)
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': a, 'keyboard': keyboard})

def autoevents():
    global timecheck
    allsend = True
    while allsend == True:
        print("19")
        a = random.randint(0, 200000)
        ti = datetime.datetime.now().strftime("%H")
        ti = str(int(ti) + 3)
        print("сейчас - ",ti)
        print("требуется - ", timecheck)

        if ti == timecheck:
            all_objects_eventtaglist = Eventtaglist.objects.all()
            today = str(datetime.datetime.today().isoweekday())
            all_objects_userlist = Userlist.objects.all()
            all_objects_usertaglist = Usertaglist.objects.all()
            for i in range(len(all_objects_userlist)):
                if all_objects_userlist[i].ul_mailing_days != None:
                    if today in all_objects_userlist[i].ul_mailing_days : 
                        tags = []
                        if all_objects_userlist[i].ul_linkvkmessage is not None:

                            for j in range(len(all_objects_usertaglist)):
                                if all_objects_userlist[i].ul_id == all_objects_usertaglist[j].utl_id_user.ul_id:
                                    tags.append(all_objects_usertaglist[j].utl_id_tag.tl_title)
                        if tags:
                            repeat_events = []
                            events_alive = False
                            for j in range(len(all_objects_eventtaglist)):
                                if all_objects_eventtaglist[j].etl_id_tag.tl_title in tags and all_objects_eventtaglist[
                                    j].etl_id_event.el_id not in repeat_events \
                                        and all_objects_eventtaglist[j].etl_id_event.el_date.date() >= datetime.datetime.today().date():
                                    event1 = all_objects_eventtaglist[j].etl_id_event.el_title + '\n\n'

                                    if all_objects_eventtaglist[j].etl_id_event.el_description != '﻿ ':
                                        event1 += 'Описание:\n' + all_objects_eventtaglist[j].etl_id_event.el_description + '\n\n'

                                    event1 += 'Дата:\n' + str(all_objects_eventtaglist[j].etl_id_event.el_date.date())

                                    if str(all_objects_eventtaglist[j].etl_id_event.el_time) != '00:00:00' and \
                                            all_objects_eventtaglist[j].etl_id_event.el_time is not None:
                                        event1 += '\nВремя:\n' + str(all_objects_eventtaglist[j].etl_id_event.el_time)
                                    else:
                                        event1 += '\nВремя:\n' + str(all_objects_eventtaglist[j].etl_id_event.el_date.time())

                                    if all_objects_eventtaglist[j].etl_id_event.el_link != '':
                                        event1 += '\n\n' + 'Сайт:\n' + all_objects_eventtaglist[j].etl_id_event.el_link + '\n\n'

                                    if all_objects_eventtaglist[j].etl_id_event.el_id_place is not None:
                                        place = 'Где это находится:\n' + 'Город: ' + all_objects_eventtaglist[
                                            j].etl_id_event.el_id_place.pl_city + '\n' \
                                                + 'Улица: ' + all_objects_eventtaglist[
                                                    j].etl_id_event.el_id_place.pl_str_name + '\n' + 'Дом: ' + \
                                                str(all_objects_eventtaglist[j].etl_id_event.el_id_place.pl_house_num) + '\n'
                                        if all_objects_eventtaglist[j].etl_id_event.el_id_place.pl_letter is not None:
                                            place += 'Буква дома: ' + all_objects_eventtaglist[
                                                j].etl_id_event.el_id_place.pl_letter + '\n'
                                        if all_objects_eventtaglist[j].etl_id_event.el_id_place.pl_place_name is not None:
                                            place += 'Название места проведения: ' + all_objects_eventtaglist[
                                                j].etl_id_event.el_id_place.pl_place_name + '\n'

                                        event1 += place

                                    repeat_events.append(all_objects_eventtaglist[j].etl_id_event.el_id)
                                    events_alive = True
                                    keyboard45 = VkKeyboard(one_time=False, inline=True)
                                    keyboard45.add_button('❤', color=VkKeyboardColor.POSITIVE)

                                    keyboard45.add_button('👎', color=VkKeyboardColor.NEGATIVE)

                                    keyboard45 = keyboard45.get_keyboard()
                                    if ti == all_objects_userlist[i].ul_mailing_time:
                                        write_msg(all_objects_userlist[i].ul_linkvkmessage, event1, a, keyboard=keyboard45)
                                    print(all_objects_userlist[i].ul_linkvkmessage)
                            if not events_alive:
                                if ti == all_objects_userlist[i].ul_mailing_time:
                                    write_msg(all_objects_userlist[i].ul_linkvkmessage, 'Мы не нашли эвенты для Вас :(', a, keyboard=keyboard)
                        #else:
                #write_msg(all_objects_userlist[i].ul_linkvkmessage, 'Вы не указали теги', a, keyboard=keyboard)
            print("87")
            #allsend = False
            if (int(timecheck) + 1) == 24:
                timecheck = "00"
            elif (int(timecheck) < 10):
                timecheck = "0" + str(int(timecheck) + 1)
            else:
                timecheck = str(int(timecheck) + 1)
        time.sleep(300)

token = "9a3bacad4b8ddf056532171ff562678143251178082472860aa6468283654cd8fa0aab54afbfada72dcc9"


vk = vk_api.VkApi(token=token)


longpoll = VkLongPoll(vk)

a = random.randint(0, 200000)
vk.method('messages.send', {'user_id': 286488661, 'message': 'Бот включен', 'random_id': a})

print('bot on')

keyboard = VkKeyboard(one_time=False)
keyboard.add_button('Ивенты', color=VkKeyboardColor.POSITIVE)
keyboard.add_line()
keyboard.add_button('Тэги', color=VkKeyboardColor.POSITIVE)
keyboard.add_line()
keyboard.add_button('Изменить тэги', color=VkKeyboardColor.POSITIVE)
keyboard.add_line()
keyboard.add_button('Изменить рассылку', color=VkKeyboardColor.POSITIVE)
keyboard.add_line()
keyboard.add_button('Мой айди', color=VkKeyboardColor.POSITIVE)
keyboard.add_line()
keyboard.add_button('Ссылка на сайт', color=VkKeyboardColor.POSITIVE)

keyboard = keyboard.get_keyboard()

autoevents()