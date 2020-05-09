from ...models import Eventlist, Userlist, Taglist, Usertaglist, Eventtaglist
from django.core.management.base import BaseCommand

from django.conf import settings
import telebot
from telebot import apihelper
from telebot import types
import random
import datetime
import time

bot = telebot.TeleBot(settings.TOKEN)

apihelper.proxy = {
    'https': settings.PROXY_URL
}

timecheck = datetime.datetime.now().strftime("%H")



def autoevents():
    global timecheck
    allsend = True
    while allsend == True:
        print("19")
        a = random.randint(0, 200000)
        ti = datetime.datetime.now().strftime("%H")
        print("сейчас - ",ti)
        print("требуется - ", timecheck)

        if ti == timecheck:
            all_objects_eventtaglist = Eventtaglist.objects.all()
            all_objects_userlist = Userlist.objects.all()
            all_objects_usertaglist = Usertaglist.objects.all()
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

                            if ti == all_objects_userlist[i].ul_mailing_time:
                                bot.send_message(all_objects_userlist[i].ul_linktgmessage, event1)
                            print(all_objects_userlist[i].ul_linktgmessage)
                    if not events_alive:
                        if ti == all_objects_userlist[i].ul_mailing_time:
                            bot.send_message(all_objects_userlist[i].ul_linktgmessage, 'Мы не нашли эвенты для Вас :(')
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
        time.sleep(20)



print('bot on')



autoevents()
print("ну и пошел нахуй")