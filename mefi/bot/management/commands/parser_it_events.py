# coding=utf-8
from ...models import Eventlist, Userlist, Taglist, Usertaglist, Eventtaglist
from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup as BS
from .choice_tags import choice_tag
from datetime import datetime


class Command(BaseCommand):
    help = 'Парсер сайта it-events.com'

    def handle(self, *args, **options):
        month = {
            'января': 'January',
            'февраля': 'February',
            'марта': 'March',
            'апреля': 'April',
            'мая': 'May',
            'июня': 'June',
            'июля': 'July',
            'августа': 'August',
            'сентября': 'September',
            'октября': 'October',
            'ноября': 'November',
            'декабря': 'December'
        }

        all_objects_taglist = Taglist.objects.all()
        all_objects_eventlist = Eventlist.objects.all()
        all_objects_eventtagtlist = Eventtaglist.objects.all()

        site = 'https://it-events.com'
        r = requests.get(site)
        html = BS(r.content, 'html.parser')
        page = 0
        while html.select('.event-list-item'):
            page += 1
            site_with_page = 'https://it-events.com' + '/?page={}'.format(page)
            r = requests.get(site_with_page)
            html = BS(r.content, 'html.parser')
            for el in html.select('.event-list-item'):
                online = el.find_all('div', class_='event-list-item__info_online')
                type = el.select('.event-list-item__type')
                # print(online)
                if online and 'курс' not in type[0].get_text(strip=True).lower():

                    title = el.select('.event-list-item__title')
                    date = el.select('.event-list-item__info')
                    print('type: ', type[0].get_text(strip=True))
                    print('title: ', title[0].get_text(strip=True))
                    print('date: ', date[0].get_text(strip=True))
                    fix_date = date[0].get_text(strip=True)
                    # if date[0].get_text(strip=True)[1] == ' ':
                    #     for i in month.keys():
                    #         if i in date[0].get_text(strip=True).split():
                    #             fix_date = '0' + date[0].get_text(strip=True).replace(i, month[i])

                    if len(fix_date) > 20:
                        fix_date = fix_date.split(' - ')[0]
                    elif ' - ' in fix_date:
                        fix_date = fix_date.replace('  ', ' ').replace(' - ', ' ').split(' ')
                        fix_date = fix_date[0] + ' ' + fix_date[2] + ' ' + fix_date[3]

                    if fix_date[1] == ' ':
                        fix_date = '0' + fix_date[:2] + month[fix_date[2:-5]] + fix_date[-5:]
                    else:
                        fix_date = fix_date[:3] + month[fix_date[3:-5]] + fix_date[-5:]
                    print(fix_date)

                    fix_date = datetime.strptime(fix_date, "%d %B %Y")

                    event_page = site + title[0].get('href')
                    print('link:', event_page)
                    event_request = requests.get(event_page)
                    event_page_parse = BS(event_request.content, 'html.parser')
                    description = event_page_parse.select('.col-md-8')

                    tags_for_desc = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul']
                    desc_fixed = ''
                    for el_desc in description:
                        tags_obj = el_desc.find_all(tags_for_desc)
                        for p in tags_obj:
                            # print(p.get_text())
                            desc_fixed += p.get_text() + '\n'

                    desc_fixed = desc_fixed.strip()
                    print(desc_fixed)
                    tags = []
                    tags.extend(choice_tag(title[0].get_text(strip=True), desc_fixed))
                    print('tags:', tags)

                    # link_place_page = event_page_parse.select('.nav-tabs-item__link')
                    # print(link_place_page)
                    if not online:
                        place_page = event_page + '/location'
                        place_request = requests.get(place_page)
                        place_page_parse = BS(place_request.content, 'html.parser')
                        location = place_page_parse.select('.col-12 .section__header')[0].get_text(strip=True)
                        print('location: ', location)

                    # дописать сохранение тегов в eventtaglist и увеличить кол-во символов описания
                    if len(all_objects_eventlist.filter(el_title=title[0].get_text(strip=True),
                                                        el_description=desc_fixed, el_date=fix_date,
                                                        el_link=event_page)) == 0 \
                            and tags != []:
                        Eventlist(el_title=title[0].get_text(strip=True),
                                  el_description=desc_fixed, el_date=fix_date,
                                  el_link=event_page).save()

                    if tags:
                        for i in range(len(tags)):
                            if len(all_objects_eventtagtlist.filter(
                                    etl_id_event=all_objects_eventlist.filter(el_title=title[0].get_text(strip=True),
                                                                              el_description=desc_fixed, el_date=fix_date,
                                                                              el_link=event_page)[0],
                                    etl_id_tag=all_objects_taglist.filter(tl_title=tags[i])[0])) == 0 \
                                    and tags:
                                Eventtaglist(
                                    etl_id_event=all_objects_eventlist.filter(el_title=title[0].get_text(strip=True),
                                                                              el_description=desc_fixed, el_date=fix_date,
                                                                              el_link=event_page)[0],
                                    etl_id_tag=all_objects_taglist.filter(tl_title=tags[i])[0]).save()

                    print('----------------')
