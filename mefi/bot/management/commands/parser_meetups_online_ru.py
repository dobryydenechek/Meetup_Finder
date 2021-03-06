from ...models import Eventlist, Userlist, Taglist, Usertaglist, Eventtaglist
import feedparser
from django.core.management.base import BaseCommand
from datetime import datetime


class Command(BaseCommand):
    help = 'Парсер сайта meetups-online.ru'

    def handle(self, *args, **options):

        class WhizRssAggregator():
            feedurl = ""

            def __init__(self, paramrssurl):
                # print(paramrssurl)
                self.feedurl = paramrssurl
                self.parse()

            def parse(self):
                thefeed = feedparser.parse(self.feedurl)

                # print("Getting Feed Data")
                # print("title --- ", thefeed.feed.get("title", ""))
                # print("link --- ", thefeed.feed.get("link", ""))
                # print("description --- ", thefeed.feed.get("item", ""))

                all_objects_taglist = Taglist.objects.all()
                all_objects_eventlist = Eventlist.objects.all()
                all_objects_eventtagtlist = Eventtaglist.objects.all()
                # print(len(all_objects_taglist.filter(tl_title='html')))

                ava = 0
                for thefeedentry in thefeed.entries:
                    # ---------- Парсинг тегов ----------
                    if len(all_objects_taglist.filter(tl_title=thefeedentry.get("category", ""))) == 0 \
                            and thefeedentry.get("category", "") != '':
                        print(thefeedentry.get("category", ""))
                        Taglist(tl_title=thefeedentry.get("category", "")).save()

                    # ---------- Парсинг эвентов ----------
                    date = str(thefeedentry.published_parsed.tm_mday) + '/' + str(  # перевод даты с читабельную троку
                        thefeedentry.published_parsed.tm_mon) + '/' \
                           + str(thefeedentry.published_parsed.tm_year) + ' ' + str(
                        thefeedentry.published_parsed.tm_hour) + \
                           ':' + str(thefeedentry.published_parsed.tm_min)
                    date = datetime.strptime(date, "%d/%m/%Y %H:%M")  # перевод строки в datetime

                    # чиним описание
                    try:  # ---- подумать
                        bad_description = thefeedentry.description.split('&nbsp;')
                        description = ''
                        for i in bad_description:
                            description += i + ' '
                    except:  # ---- подумать
                        description = ''  # ---- подумать

                    # if description != '':
                    # проверяем, есть ли такой эвент уже бд
                    if len(all_objects_eventlist.filter(el_title=thefeedentry.get("title", ""),
                                                        el_description=description, el_date=date,
                                                        el_link=thefeedentry.get("link", ""))) == 0 \
                            and thefeedentry.get("category", "") != '':
                        Eventlist(el_title=thefeedentry.get("title", ""),
                                  el_description=description, el_date=date,
                                  el_link=thefeedentry.get("link", "")).save()
                            # print(thefeedentry.get("title", ""), ' - ', date)
                    # else:  # ---- подумать
                    #     if len(all_objects_eventlist.filter(el_title=thefeedentry.get("title", ""),
                    #                                         el_date=date,
                    #                                         el_link=thefeedentry.get("link", ""))) == 0 \
                    #             and thefeedentry.get("category", "") != '':
                    #         Eventlist(el_title=thefeedentry.get("title", ""),
                    #                   el_date=date,
                    #                   el_link=thefeedentry.get("link", "")).save()


                    # print(all_objects_eventtagtlist.filter(
                    #         etl_id_event=all_objects_eventlist.get(
                    #             el_title=thefeedentry.get("title", ""),
                    #             el_description=description, el_date=date,
                    #             el_link=thefeedentry.get("link", "")),
                    #         etl_id_tag=all_objects_taglist.get(
                    #             tl_title=thefeedentry.get("category", ""))
                    # ))

                    # print(all_objects_eventlist.get(
                    #             el_title=thefeedentry.get("title", ""),
                    #             el_description=description, el_date=date,
                    #             el_link=thefeedentry.get("link", "")))
                    # print(all_objects_taglist.get(
                    #             tl_title=thefeedentry.get("category", "")
                    #         ))

                    # print(thefeedentry.get("title", ""))
                    # print(all_objects_eventlist.get(el_title=thefeedentry.get("title", ""),
                    #                                 el_description=description, el_date=date,
                    #                                 el_link=thefeedentry.get("link", "")))

                    if thefeedentry.get("category", "") != '':
                        if len(all_objects_eventtagtlist.filter(
                                etl_id_event=all_objects_eventlist.filter(el_title=thefeedentry.get("title", ""),
                                                                          el_description=description, el_date=date,
                                                                          el_link=thefeedentry.get("link", ""))[0],
                                etl_id_tag=all_objects_taglist.filter(tl_title=thefeedentry.get("category", ""))[0])) == 0 \
                                and thefeedentry.get("category", "") != '':
                            Eventtaglist(
                                etl_id_event=all_objects_eventlist.filter(el_title=thefeedentry.get("title", ""),
                                                                          el_description=description, el_date=date,
                                                                          el_link=thefeedentry.get("link", ""))[0],
                                etl_id_tag=all_objects_taglist.filter(tl_title=thefeedentry.get("category", ""))[0]).save()

                    # if thefeedentry.get("category", "") != '':
                    #     ava += 1


                    # print("__________")
                    # print(thefeedentry.get("title", ""))
                    # print(thefeedentry.get("link", ""))
                    # # time.struct_time(tm_year=2020, tm_mon=3, tm_mday=26, tm_hour=9, tm_min=0, tm_sec=0, tm_wday=3,
                    # #                   tm_yday=86, tm_isdst=0)
                    # date = str(thefeedentry.published_parsed.tm_mday) + '/' + str(
                    #     thefeedentry.published_parsed.tm_mon) + '/' \
                    #        + str(thefeedentry.published_parsed.tm_year) + ' ' + str(
                    #     thefeedentry.published_parsed.tm_hour) + \
                    #        ':' + str(thefeedentry.published_parsed.tm_min)
                    # print(datetime.strptime(date, "%d/%m/%Y %H:%M"))
                    # print(thefeedentry.get("category", ""))
                    # bad_description = thefeedentry.description.split('&nbsp;')
                    # description = ''
                    # for i in bad_description:
                    #     description += i + ' '
                    # print(description)
                    # print("__________")

                # print(ava)

        rssobject = WhizRssAggregator("http://meetups-online.ru/rss-feed-771034387759.xml")
