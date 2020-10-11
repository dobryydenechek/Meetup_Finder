import datetime
from collections import namedtuple
import requests
import bs4
from .choice_tags import choice_tag
from ...models import Eventlist, Eventtaglist, Taglist
from django.core.management.base import BaseCommand
import psycopg2


InnerBlock = namedtuple('Block', 'title, description, date, tags, link')


class Block(InnerBlock):

    # def __init__(self):
    #     self.title = InnerBlock.title
    #     self.date = InnerBlock.date
    #     self.link = InnerBlock.link
    #     self.tags = InnerBlock.tags
    #     self.description = InnerBlock.description

    # def __init__(self):
    #     title = self.title

    def __str__(self):
        return f'{self.title}\t{self.date}\t{self.link}\t{self.tags}\n{self.description}'


    def add_in_database(self):
        all_objects_taglist = Taglist.objects.all()
        all_objects_eventlist = Eventlist.objects.all()
        all_objects_eventtagtlist = Eventtaglist.objects.all()
        print(self.date)
        if len(all_objects_eventlist.filter(el_title=self.title,
                                            el_description=self.description, el_date=self.date,
                                            el_link=self.link)) == 0 \
                and self.tags != []:
            Eventlist(el_title=self.title,
                      el_description=self.description, el_date=self.date,
                      el_link=self.link).save()

        if self.tags:
            print(self.tags)
            for i in range(len(self.tags)):
                if len(all_objects_eventtagtlist.filter(
                        etl_id_event=all_objects_eventlist.filter(el_title=self.title,
                                                                  el_description=self.description,
                                                                  el_date=self.date,
                                                                  el_link=self.link)[0],
                        etl_id_tag=all_objects_taglist.filter(tl_title=self.tags[i])[0])) == 0 \
                        and self.tags:
                    Eventtaglist(
                        etl_id_event=all_objects_eventlist.filter(el_title=self.title,
                                                                  el_description=self.description,
                                                                  el_date=self.date,
                                                                  el_link=self.link)[0],
                        etl_id_tag=all_objects_taglist.filter(tl_title=self.tags[i])[0]).save()

class WorldexpoParser:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/85.0.4183.121 Safari/537.36 OPR/71.0.3770.234 (Edition Yx GX) '
        }

    def get_page(self):
        url = 'https://worldexpo.pro/country/rossiya/sector/it-it-digital-elektronnaya-kommerciya/online'
        r = self.session.get(url)
        return r.text

    def parse_block(self, i):
        # Выбрать блок со ссылкой
        url_block = i.select_one('h4.item-content-title a')
        href = url_block.get('href')
        if href:
            global url
            url = 'https://worldexpo.pro' + href
        else:
            url = None

        # Выбрать блок с названием и датой
        title_block = i.select_one('h4.item-content-title a')
        title = title_block.string.strip()

        date_block = i.select_one('span.item-content-date')
        date_s = date_block.string.strip()[13:]
        date = datetime.datetime.strptime(date_s, "%d.%m.%Y")

        self.get_description()

        tags = choice_tag(title, description)


        return Block(
            link=url,
            title=title,
            date=date,
            description=description,
            tags=tags
        )



    def get_description_page(self):
        r = self.session.get(url)
        return r.text

    def get_blocks(self):
        text = self.get_page()

        soup = bs4.BeautifulSoup(text, 'lxml')
        container = soup.select('div.row.event-wrapper')
        for i in container:
            global block
            block = self.parse_block(i=i)
            # print(block)
            block.add_in_database()
            print('____________________________________________________________________')





    def get_description(self):
        text = self.get_description_page()

        soup = bs4.BeautifulSoup(text, 'lxml')
        container = soup.select('div.description.event-desc-block')
        for i in container:
            global description
            description = i.get_text('\n')






def main():
    p = WorldexpoParser()
    p.get_blocks()


class Command(BaseCommand):
    help = 'Парсер сайта it-events.com'

    def handle(self, *args, **options):
        main()