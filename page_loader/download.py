import os
import re
import requests


def url_to_filename(url=''):
    # Берется адрес страницы без схемы
    # Все символы, кроме букв и цифр заменяются на дефис -.
    # В конце ставится .html.
    url = re.sub(r'\b(https:|http:|url:|ftp:)[^a-zA-Z ]{2}', '', url)
    return f"{re.sub(r'[^A-Za-z0-9]', '-', url)}.html"


def write_file(file='', text=''):
    with open(file, 'w', encoding='utf-8') as w:
        w.write(text)


def download(url='', output=os.getcwd()):
    file_name = f'{output}/{url_to_filename(url)}'
    page_data = requests.get(url).text
    write_file(file_name, page_data)
    return file_name
