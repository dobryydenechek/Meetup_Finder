import requests
from datetime import datetime
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

from .choice_tags import check_conformity

from ...models import Eventlist, Eventtaglist, Taglist

URL = 'https://ict2go.ru/ajax/index_load_more/?page=1&filter=index&id=undefined'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0', 'accept': '*/*'}
HOST = 'https://ict2go.ru'

our_tags = {
    'Java': 'Бэк',
    'Python': 'Бэк',
    'Разработка ПО': 'Бэк',
    'Машинное обучение': 'Аналитика и data science',
    'MVNO': 'Mobile',
    'Мобильная коммерция': 'Mobile',
    'Мобильные приложения': 'Mobile',
    'QA и тестирование': 'QA',
    'JavaScript': 'Фронт',
    'UI': 'Фронт',
    'UX': 'Фронт',
    'веб-дизайн': 'Фронт',
    'веб/онлайн': 'Фронт',
    'Графический дизайн': 'Фронт',
    'управление проектами (project management)': 'Подукт',
    'Разработка игр (геймдев)': 'Геймдев',
    'робототехника': 'Роботы',
    'Информационная безопасность': 'Безопасность',
    'Интернет вещей (IoT)': 'Hard и IoT'
}

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def check_page(num):
    html = get_html(f'https://ict2go.ru/ajax/index_load_more/?page={num}&filter=index&id=undefined')
    soup = BeautifulSoup(html.content, 'html.parser')
    items = soup.find_all('div', class_='media-body')
    if items:
        return True
    else:
        return False


def get_content(html):

    soup = BeautifulSoup(html.content, 'html.parser')
    items = soup.find_all('div', class_='media-body')

    event = Eventlist(el_title='')

#ПОЛУЧЕНИЕ ДЕННЫХ О ИВЕНТЕ

    for item in items:
        event = Eventlist()
        event.el_title=''
        title = str(item.find('a', class_='event-title').get_text(strip=True))
        if ('перенесено' in title) or ('перенесен' in title) or ('новая дата' in title):
            title = '-'
        event.el_title = title
        event.el_date = item.find('div', class_='date-place').get_text(strip=True)[:10]
        event.el_date = datetime.strptime(event.el_date, "%d.%m.%Y")

        if item.find('a', class_='event-title').get('href')[0] == '/' and \
                (item.select('.date-place a')[0].get_text(strip=True).lower() == 'онлайн' or \
                item.select('.date-place a')[0].get_text(strip=True).lower() == 'ростов-на-дону'):
            internal_link = HOST + item.find('a', class_='event-title').get('href')
            internal_html = get_html(internal_link)
            internal_soup = BeautifulSoup(internal_html.content, 'html.parser')
            internal_items = internal_soup.find_all('div', class_='main-content')
            for internal_item in internal_items:
                description = internal_item.find_all('div', class_ ='tab-item description-info')
                text = ''
                for p in description:
                    try:
                        text += p.find('div', class_='tab-item description-info').get_text(strip=True)
                    except:
                        pass
                    try:
                        text += p.find('p').text.replace('\xa0', ' ') + '\n'
                    except:
                        pass
                    try:
                        online_link = 'Ссылка на мероприятие: ' + internal_item.find('div', class_='event-links').find('a', class_='www-info invoke-count').get('href') + '\n'
                    except:
                        online_link = ''
                    try:
                        reg_link ='Ссылка на регистрацию: ' + internal_item.find('div', class_='event-links').find('a', class_='register-info invoke-count').get('href')
                    except:
                        reg_link = ''
                    if 'перенесено' in text or 'перенесён' in text or 'новая дата' in text or 'отменено' in text:
                        text = '-'

                event.el_description = text
                event.el_link =online_link + reg_link
        if (event.el_description != '-') and (event.el_title != '-'):
            all_events = Eventlist.objects.all()
            can_save = True

#ПОЛУЧЕНИЕ ТЭГОВ И ПРИСОБАЧИВАНИЕ ИВЕНТА
            tags = item.find('div', class_='event-themes').find_all('a')
            internal_tags = []
            try:
                for tag in tags:
                    try:
                        internal_tag = Taglist.objects.get(tl_title=our_tags[tag.get_text(strip=True)])
                        internal_tags.append(internal_tag)
                    except Exception as e:
                        continue
            except Exception as e:
                print('Something went wrong', e)
                can_save = False
            for Event in all_events:
                if check_conformity(event,Event) > 80:
                    can_save = False
            if can_save == True and len(internal_tags) > 0:
                try:
                    event.save()
                    for tag in internal_tags:
                        tag = Eventtaglist(etl_id_event=Eventlist.objects.get(el_id=event.el_id), etl_id_tag=tag)
                        tag.save()
                except Exception as e:
                    print(e)
            else:
                pass


def pagination(num):
    html = get_html(f'https://ict2go.ru/ajax/index_load_more/?page={num}&filter=index&id=undefined')
    get_content(html)

def parse():
    html = get_html(URL)
    if html.status_code == 200:
        page = 1
        while check_page(page):
            print(page)
            pagination(page)
            page += 1
    else:
        print('---------------------------------------------------------------------------------------------------------------------------')
        print('THE END')


class Command(BaseCommand):
    help = 'Парсер сайта ICT2GO'

    def handle(self, *args, **options):
        parse()
