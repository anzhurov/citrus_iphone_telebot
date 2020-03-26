import requests
from bs4 import BeautifulSoup

IPHONE_PAGE_URL = 'https://www.citrus.ua/smartfony/iphone-11-pro-256gb-gold-apple-653237.html'


def fetch_price():
    page_html = requests.get(IPHONE_PAGE_URL).text
    parsed_html = BeautifulSoup(page_html, features='html.parser')
    return parsed_html \
        .find(attrs={'class': 'normal__prices'}) \
        .find_all(attrs={'class': 'price'})[1] \
        .span.span.text
