from ...models import Eventlist, Userlist, Taglist, Usertaglist, Eventtaglist
from django.core.management.base import BaseCommand
import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
import random
import datetime
import threading

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
newtimee = []
optio = []
opt1 = []
opt2 = []
opt3 = []
opt4 = []
opt5 = []
opt6 = []
opt7 = []
opt8 = []
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
                        tags += str(num_of_tag) + ') ' + \
                                all_objects_usertaglist[j].utl_id_tag.tl_title + '\n'
        #######

        tags = tags_without_usertags('tags')

        keyboard13 = VkKeyboard(one_time=False)
        keyboard13.add_button('Готово', color=VkKeyboardColor.POSITIVE)

        for i in range(len(tags.keys()) // 2):
            keyboard13.add_line()
            keyboard13.add_button(tags[list(tags.keys())[i]], color=VkKeyboardColor.POSITIVE)
            keyboard13.add_button(tags[list(tags.keys())[-i - 1]], color=VkKeyboardColor.POSITIVE)
        if len(tags.keys()) - len(tags.keys()) // 2 != len(tags.keys()) // 2:
            keyboard13.add_line()
            keyboard13.add_button(tags[list(tags.keys())[len(tags.keys()) // 2]], color=VkKeyboardColor.POSITIVE)
        keyboard13 = keyboard13.get_keyboard()



        inwait2.append(event.user_id)

        write_msg(event.user_id, 'Добавьте нужные теги. Список с тэгами можно листать', a, keyboard=keyboard13)

        ########




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
    keyboard35 = VkKeyboard(one_time=False)
    keyboard35.add_button('В главное меню', color=VkKeyboardColor.POSITIVE)
    keyboard35.add_line()
    keyboard35.add_button('Посмотреть мои тэги', color=VkKeyboardColor.POSITIVE)
    keyboard35.add_button('Изменить мои тэги', color=VkKeyboardColor.POSITIVE)
    keyboard35.add_line()
    keyboard35.add_button('Что означают тэги?', color=VkKeyboardColor.POSITIVE)

    keyboard35 = keyboard35.get_keyboard()
    write_msg(event.user_id, 'Выберите настройку', a, keyboard=keyboard35)

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
            write_msg(event.user_id, f'Ваши теги: \n{tags}', a, keyboard=keyboard35)
            exist_user = True
    if not exist_user:
        write_msg(event.user_id, 'Вы не зарегистрированы на нашем сайте', a)

def mainmenu(message):
    keyboard35 = VkKeyboard(one_time=False)
    keyboard35.add_button('Ивенты', color=VkKeyboardColor.POSITIVE)
    keyboard35.add_line()
    keyboard35.add_button('Тэги', color=VkKeyboardColor.POSITIVE)
    keyboard35.add_line()
    keyboard35.add_button('Настройки', color=VkKeyboardColor.POSITIVE)
    keyboard35.add_line()
    keyboard35.add_button('Ссылка на сайт', color=VkKeyboardColor.POSITIVE)
    keyboard35 = keyboard35.get_keyboard()
    write_msg(event.user_id, 'Вы в главном меню', a, keyboard=keyboard35)

def setting_tags(message):
    keyboard35 = VkKeyboard(one_time=False)
    keyboard35.add_button('В главное меню', color=VkKeyboardColor.POSITIVE)
    keyboard35.add_line()
    keyboard35.add_button('Посмотреть мои тэги', color=VkKeyboardColor.POSITIVE)
    keyboard35.add_button('Изменить мои тэги', color=VkKeyboardColor.POSITIVE)
    keyboard35.add_line()
    keyboard35.add_button('Что означают тэги?', color=VkKeyboardColor.POSITIVE)

    keyboard35 = keyboard35.get_keyboard()
    write_msg(event.user_id, 'Выберите настройку', a, keyboard=keyboard35)



def change_tags(message):

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

        tags = tags_without_usertags('tags')

        keyboard13 = VkKeyboard(one_time=False)
        keyboard13.add_button('Готово', color=VkKeyboardColor.POSITIVE)


        for i in range(len(tags.keys()) // 2):
            keyboard13.add_line()
            keyboard13.add_button(tags[list(tags.keys())[i]], color=VkKeyboardColor.POSITIVE)
            keyboard13.add_button(tags[list(tags.keys())[-i-1]], color=VkKeyboardColor.POSITIVE)
        if len(tags.keys()) - len(tags.keys()) // 2 != len(tags.keys()) // 2:
            keyboard13.add_line()
            keyboard13.add_button(tags[list(tags.keys())[len(tags.keys()) // 2]], color=VkKeyboardColor.POSITIVE)
        keyboard13 = keyboard13.get_keyboard()

        inwait1.remove(event.user_id)

        inwait2.append(event.user_id)

        write_msg(event.user_id, 'Добавьте нужные теги. Список с тэгами можно листать', a, keyboard=keyboard13)




    elif message.lower() == 'удалить':
        tags = tags_without_usertags('usertags')

        keyboard3 = VkKeyboard(one_time=False)
        keyboard3.add_button('Готово', color=VkKeyboardColor.POSITIVE)

        for i in range(len(tags.keys()) // 2):
            keyboard3.add_line()
            keyboard3.add_button(tags[list(tags.keys())[i]], color=VkKeyboardColor.POSITIVE)
            keyboard3.add_button(tags[list(tags.keys())[-i - 1]], color=VkKeyboardColor.POSITIVE)
        if len(tags.keys()) - len(tags.keys()) // 2 != len(tags.keys()) // 2:
            keyboard3.add_line()
            keyboard3.add_button(tags[list(tags.keys())[len(tags.keys()) // 2]], color=VkKeyboardColor.POSITIVE)


        keyboard3 = keyboard3.get_keyboard()
        write_msg(event.user_id, 'Удалите ненужные теги. Список с тэгами можно листать', a, keyboard=keyboard3)

        inwait1.remove(event.user_id)
        inwait3.append(event.user_id)






def add_tags(message):

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
        for i in range(len(tags.keys()) // 2):
            keyboard3.add_line()
            keyboard3.add_button(tags[list(tags.keys())[i]], color=VkKeyboardColor.POSITIVE)
            keyboard3.add_button(tags[list(tags.keys())[-i-1]], color=VkKeyboardColor.POSITIVE)
        if len(tags.keys()) - len(tags.keys()) // 2 != len(tags.keys()) // 2:
            keyboard3.add_line()
            keyboard3.add_button(tags[list(tags.keys())[len(tags.keys()) // 2]], color=VkKeyboardColor.POSITIVE)
        #if len(tags.keys()) - len(tags.keys()) // 2 != len(tags.keys()) // 2:
            #keyboard3.add_button(tags[list(tags.keys())[len(tags.keys()) // 2]], color=VkKeyboardColor.POSITIVE)
            #keyboard3.add_button("ЧЛЕН", color=VkKeyboardColor.POSITIVE)
            #keyboard3.add_line()

        keyboard3 = keyboard3.get_keyboard()

        write_msg(event.user_id, f'Тэг {message} добавлен', a, keyboard=keyboard3)


    if message == 'Готово':

        inwait2.remove(event.user_id)

        keyboard35 = VkKeyboard(one_time=False)
        keyboard35.add_button('В главное меню', color=VkKeyboardColor.POSITIVE)
        keyboard35.add_line()
        keyboard35.add_button('Посмотреть мои тэги', color=VkKeyboardColor.POSITIVE)
        keyboard35.add_button('Изменить мои тэги', color=VkKeyboardColor.POSITIVE)
        keyboard35.add_line()
        keyboard35.add_button('Что означают тэги?', color=VkKeyboardColor.POSITIVE)

        keyboard35 = keyboard35.get_keyboard()

        write_msg(event.user_id, 'Вы в главном меню', a, keyboard=keyboard35)


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
        for i in range(len(tags.keys()) // 2):
            keyboard3.add_line()
            keyboard3.add_button(tags[list(tags.keys())[i]], color=VkKeyboardColor.POSITIVE)
            keyboard3.add_button(tags[list(tags.keys())[-i - 1]], color=VkKeyboardColor.POSITIVE)
        if len(tags.keys()) - len(tags.keys()) // 2 != len(tags.keys()) // 2:
            keyboard3.add_line()
            keyboard3.add_button(tags[list(tags.keys())[len(tags.keys()) // 2]], color=VkKeyboardColor.POSITIVE)


        keyboard3 = keyboard3.get_keyboard()
        write_msg(event.user_id, f'Тэг {message} удалён', a, keyboard=keyboard3)


    if message == 'Готово':
        keyboard35 = VkKeyboard(one_time=False)
        keyboard35.add_button('В главное меню', color=VkKeyboardColor.POSITIVE)
        keyboard35.add_line()
        keyboard35.add_button('Посмотреть мои тэги', color=VkKeyboardColor.POSITIVE)
        keyboard35.add_button('Изменить мои тэги', color=VkKeyboardColor.POSITIVE)
        keyboard35.add_line()
        keyboard35.add_button('Что означают тэги?', color=VkKeyboardColor.POSITIVE)

        keyboard35 = keyboard35.get_keyboard()

        write_msg(event.user_id, 'Изменения сохранены', a, keyboard=keyboard35)










#@bot.message_handler(commands=['link', 'account', 'change_tags', 'options'])
def site_link(message):
    write_msg(event.user_id, 'Ссылка на сайт: http://project2205235.tilda.ws/', a, keyboard=keyboard)


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

                if all_objects_eventtaglist[i].etl_id_tag.tl_title in tags and all_objects_eventtaglist[i].etl_id_event.el_id not in repeat_events and all_objects_eventtaglist[i].etl_id_event.el_date.date() >= datetime.datetime.today().date():
                    event1 = all_objects_eventtaglist[i].etl_id_event.el_title + '\n\n'

                    if all_objects_eventtaglist[i].etl_id_event.el_description != '﻿ ':

                        event1 += 'Описание:\n' + all_objects_eventtaglist[i].etl_id_event.el_description + '\n\n'

                    event1 += 'Дата:\n' + str(all_objects_eventtaglist[i].etl_id_event.el_date.date())

                    if str(all_objects_eventtaglist[i].etl_id_event.el_time) != '00:00:00+03' and \
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
                    print(" ")
                    print("_________________")
                    print(event1)
                    print("_________________")
                    ######

                    keyboard45 = VkKeyboard(one_time=False, inline=True)
                    keyboard45.add_button('❤', color=VkKeyboardColor.POSITIVE)

                    keyboard45.add_button('👎', color=VkKeyboardColor.NEGATIVE)

                    keyboard45 = keyboard45.get_keyboard()



                    ######
                    write_msg(event.user_id, event1, a, keyboard=keyboard45)
            if not events_alive:
                write_msg(event.user_id, 'Мы не нашли эвенты для Вас :(', a, keyboard=keyboard)
        else:
            write_msg(event.user_id, 'Вы не указали теги', a, keyboard=keyboard)




#--------------------------------------------------
#--------------------------------------------------
#--------------------------------------------------





def mailing_options(message):
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button("Готово", color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button("Изменить время", color=VkKeyboardColor.POSITIVE)
    keyboard.add_button("Изменить день недели", color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button("Мой айди", color=VkKeyboardColor.POSITIVE)
    keyboard = keyboard.get_keyboard()
    write_msg(event.user_id, 'Выбирите настройку', a, keyboard=keyboard)


    opt1.append(event.user_id)



def choose_option(message):


    if message.lower() == 'изменить время':
        opt1.remove(event.user_id)
        change_time(message)
    elif message.lower() == 'изменить день недели':
        opt1.remove(event.user_id)
        day_change(message)
    elif message.lower() == 'готово':

        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button('Ивенты', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button('Тэги', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button('Настройки', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button('Ссылка на сайт', color=VkKeyboardColor.POSITIVE)
        keyboard = keyboard.get_keyboard()
        write_msg(event.user_id, 'Готово', a, keyboard=keyboard)
        opt1.remove(event.user_id)
    else:
        write_msg(event.user_id, 'Это не один из вариантов меню', a)




def show_days(message):
    a = random.randint(0, 200000)
    print(382)
    user = Userlist.objects.get(ul_linkvkmessage = event.user_id)
    user_days = []

    for i in range(len(str(user.ul_mailing_days))):
        if user.ul_mailing_days != None:
            user_days.append(int(str(user.ul_mailing_days)[len(str(user.ul_mailing_days)) - i - 1:len(str(user.ul_mailing_days)) - i ]))

    days = {1 : 'Понедельник', 2 : 'Вторник', 3 : 'Среда', 4 : 'Четверг', 5 : 'Пятница', 6 : 'Суббота', 7 : 'Воскресенье'}

    keyboard = VkKeyboard(one_time=False)

    if message.lower() == 'изменить день недели':
        keyboard.add_button('Готово', color=VkKeyboardColor.POSITIVE)
    else:
        keyboard.add_button('В настройки', color=VkKeyboardColor.POSITIVE)

    for i in range(1, len(days) + 1):
        if list(days.keys())[i - 1] in user_days:
            keyboard.add_line()
            keyboard.add_button(str(days[i]), color=VkKeyboardColor.POSITIVE)
        else:
            keyboard.add_line()
            keyboard.add_button(str(days[i]), color=VkKeyboardColor.NEGATIVE)
    print(message)
    print(message.lower() == 'изменить день недели')
    print(keyboard)
    keyboard = keyboard.get_keyboard()
    return keyboard



def day_change(message):
    print("554")
    print(message)
    a = random.randint(0, 200000)
    days = {'Понедельник' : 1,
            'Вторник' : 2,
            'Среда' : 3,
            'Четверг' : 4,
            'Пятница' : 5,
            'Суббота' : 6,
            'Воскресенье' : 7}

    if message.lower() == 'готово' or message.lower() == 'в настройки':

        keyboard = VkKeyboard(one_time=False)

        keyboard.add_button('Ивенты', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button('Тэги', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button('Настройки', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button('Ссылка на сайт', color=VkKeyboardColor.POSITIVE)
        keyboard = keyboard.get_keyboard()

        write_msg(event.user_id, 'Готово', a, keyboard=keyboard)
        opt2.remove(event.user_id)
    elif message in list(days): #если сообщение равно одному из дней недели
        user = Userlist.objects.get(ul_linkvkmessage=event.user_id)
        user_days = []

        if user.ul_mailing_days == None:
            user.ul_mailing_days = ""
            user.save()

        for i in range(len(str(user.ul_mailing_days))):
            user_days.append(int(str(user.ul_mailing_days)[len(str(user.ul_mailing_days)) - i - 1:len(str(user.ul_mailing_days)) - i ]))  #обращаемся к бд и разбиваем строку на отдельные символы
        print(user_days)
        if days[message] in user_days: #формируем новый список дней пользователя
            user_days.remove(days[message])
            ans = f'удалили {message}'
        else:
            ans = f'добавили {message}'
            user_days.append(days[message])

        print(user_days)
        new_days=''
        for i in user_days:# формируем новую строку из отдельных символов
            new_days += str(i)

        user = Userlist.objects.get(ul_linkvkmessage=event.user_id)
        user.ul_mailing_days = new_days
        user.save()
        #отображаем новую клавиатуру
        markup = show_days(message)
        write_msg(event.user_id, f'Вы {ans}', a, keyboard=markup)
        opt2.append(event.user_id)

    elif message.lower() == 'изменить день недели':
        markup = show_days(message)
        print(markup)
        write_msg(event.user_id, 'Выбирите день для рассылки', a, keyboard=markup)
        opt2.append(event.user_id)

    else:

        write_msg(event.user_id, 'Нажимайте на кнопки', a)
        opt2.append(event.user_id)


#######################################################

#######################################################

def change_time(message):
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button("01:00", color=VkKeyboardColor.POSITIVE)
    keyboard.add_button("02:00", color=VkKeyboardColor.POSITIVE)
    keyboard.add_button("03:00", color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button("04:00", color=VkKeyboardColor.POSITIVE)
    keyboard.add_button("05:00", color=VkKeyboardColor.POSITIVE)
    keyboard.add_button("06:00", color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button("07:00", color=VkKeyboardColor.POSITIVE)
    keyboard.add_button("08:00", color=VkKeyboardColor.POSITIVE)
    keyboard.add_button("09:00", color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button("10:00", color=VkKeyboardColor.POSITIVE)
    keyboard.add_button("11:00", color=VkKeyboardColor.POSITIVE)
    keyboard.add_button("12:00", color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button("13:00", color=VkKeyboardColor.POSITIVE)
    keyboard.add_button("14:00", color=VkKeyboardColor.POSITIVE)
    keyboard.add_button("15:00", color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button("16:00", color=VkKeyboardColor.POSITIVE)
    keyboard.add_button("17:00", color=VkKeyboardColor.POSITIVE)
    keyboard.add_button("18:00", color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button("19:00", color=VkKeyboardColor.POSITIVE)
    keyboard.add_button("20:00", color=VkKeyboardColor.POSITIVE)
    keyboard.add_button("21:00", color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button("22:00", color=VkKeyboardColor.POSITIVE)
    keyboard.add_button("23:00", color=VkKeyboardColor.POSITIVE)
    keyboard.add_button("00:00", color=VkKeyboardColor.POSITIVE)
    keyboard = keyboard.get_keyboard()
    write_msg(event.user_id, 'Выберите время', a, keyboard=keyboard)

    newtimee.append(event.user_id)


def new_time(message):

    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Ивенты', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('Тэги', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('Настройки', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('Ссылка на сайт', color=VkKeyboardColor.POSITIVE)

    all_objects_userlist = Userlist.objects.get(ul_linkvkmessage=event.user_id) #Нынешний пользователь

    all_objects_userlist.ul_mailing_time = message[:2]
    print(message[:2])
    print(all_objects_userlist.ul_mailing_time)
    all_objects_userlist.save()
    newtimee.remove(event.user_id)

    keyboard = keyboard.get_keyboard()
    write_msg(event.user_id, f'Следующая рассылка будет в {message}', a, keyboard=keyboard)


#-----------------------------------------------
#--------------------------------------------------
#--------------------------------------------------

def write_msg(user_id, message, a, keyboard=None):
    a = random.randint(0, 200000)
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': a, 'keyboard': keyboard})






token = "9a3bacad4b8ddf056532171ff562678143251178082472860aa6468283654cd8fa0aab54afbfada72dcc9"


vk = vk_api.VkApi(token=token)


longpoll = VkLongPoll(vk)



vk.method('messages.send', {'user_id': 286488661, 'message': 'Бот включен', 'random_id': a})

print('bot on')

keyboard = VkKeyboard(one_time=False)
keyboard.add_button('Ивенты', color=VkKeyboardColor.POSITIVE)
keyboard.add_line()
keyboard.add_button('Тэги', color=VkKeyboardColor.POSITIVE)
keyboard.add_line()
keyboard.add_button('Настройки', color=VkKeyboardColor.POSITIVE)
keyboard.add_line()
keyboard.add_button('Ссылка на сайт', color=VkKeyboardColor.POSITIVE)
keyboard = keyboard.get_keyboard()



for event in longpoll.listen():
    a = random.randint(0, 200000)

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

            elif request.lower() == "изменить мои тэги":
                change_tags(event.user_id)
                print(event.user_id, request)

            elif request.lower() == "тэги":
                setting_tags(event.user_id)
                print(event.user_id, request)

            elif request.lower() == "help":
                write_msg(event.user_id, "Доступные команды:\n 1)'Ивенты'\n 2)'Тэги'\n 3)'Изменить тэги'\n 4)'Мой айди'\n 5)'Ссылка на сайт'", a, keyboard=keyboard)
                print(event.user_id, request)

            elif request.lower() == "нихуя себе":
                write_msg(event.user_id, keyboard, a, keyboard=keyboard)
                print(event.user_id, request)

            elif request.lower() == "мой айди":
                id_on_the_sitee(event.user_id)
                print(event.user_id, request)

            elif request.lower() == "настройки":
                mailing_options(event.user_id)
                print(event.user_id, request)

            elif request.lower() == "ивенты":
                events(event.user_id)
                print(event.user_id, request)

            elif request.lower() == "посмотреть мои тэги":
                id_on_the_site(event.user_id)

                print(event.user_id, request)

            elif request.lower() == 'ссылка на сайт':
                site_link(event.user_id)
                print(event.user_id, request)

            elif request.lower() == 'в главное меню':
                mainmenu(event.user_id)
                print(event.user_id, request)

            else:
                if event.user_id in inwait1:
                    add_del_tags(request)
                    print(event.user_id, request)
                elif event.user_id in inwait2:
                    add_tags(request)
                    print(event.user_id, request)
                elif event.user_id in newtimee:
                    new_time(request)
                    print(event.user_id, request)
                elif event.user_id in inwait3:
                    del_tags(request)
                    print(event.user_id, request)
                elif event.user_id in opt1:
                    choose_option(request)
                    print(event.user_id, request)
                elif event.user_id in opt2:
                    day_change(request)
                    print(event.user_id, request)


                else:
                    write_msg(event.user_id, "к сожалению, я не понял вашего сообщения\n напишите 'help'", a, keyboard=keyboard)
                    print(event.user_id, request, "krai")






