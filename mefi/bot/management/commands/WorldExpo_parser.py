import datetime
from collections import namedtuple
import requests
import bs4

InnerBlock = namedtuple('Block', 'title, description, date,  link')


class Block(InnerBlock):
    def __str__(self):
        return f'{self.title}\t{self.date}\t{self.link}\t{self.description}'


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
        date = date_block.string.strip()[13:]

        self.get_discription()
        return Block(
            link=url,
            title=title,
            date=date,
            description=discription,
        )

    def get_discription_page(self):
        r = self.session.get(url)
        return r.text

    def get_blocks(self):
        text = self.get_page()

        soup = bs4.BeautifulSoup(text, 'lxml')
        container = soup.select('div.row.event-wrapper')
        for i in container:
            block = self.parse_block(i=i)
            print(block)
            print('____________________________________________________________________')

    def get_discription(self):
        text = self.get_discription_page()

        soup = bs4.BeautifulSoup(text, 'lxml')
        container = soup.select('div.description.event-desc-block')
        for i in container:
            global discription
            discription = i.get_text('\n')


def main():
    p = WorldexpoParser()
    p.get_blocks()


if __name__ == '__main__':
    main()
