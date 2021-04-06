import os
import re
import requests

from urllib.parse import urlparse
from bs4 import BeautifulSoup


def get_file_name(url='', extension='.html'):
    url = re.sub(r'\b(https:|http:|url:|ftp:)[^a-zA-Z ]{2}', '', url)
    return f"{re.sub(r'[^A-Za-z0-9]', '-', url)}{extension}"


def write_file(file='', text=''):
    with open(file, 'w', encoding='utf-8') as w:
        w.write(text)


def write_bin(file='', binory=[]):
    os.makedirs(os.path.dirname(file), exist_ok=True)
    with open(file, 'wb') as w:
        w.write(binory)


def download_files(data='', folder=os.getcwd(), url=''):
    hostname = urlparse(url).hostname
    soup = BeautifulSoup(data, 'html.parser')
    for link in soup.find_all('img'):
        old_name = link.get('src')
        new_name = get_file_name(f'{hostname}-{old_name}'.rstrip(".png"), ".png")

        binory = []
        if 'https' in old_name or 'http' in old_name or 'url' in old_name or 'ftp' in old_name:
            binory = requests.get(old_name).content
        else:
            binory = requests.get(f'{hostname}/{old_name}').content

        new_src = f'{get_file_name(url, "_files")}/{new_name}'

        write_bin(f'{folder}/{new_src}', binory)
        data = data.replace(old_name, new_src)

    return data


def download(url='', folder=os.getcwd()):
    file_name = f'{folder}/{get_file_name(url)}'
    page_data = requests.get(url).text
    page_data = download_files(page_data, folder, url)
    write_file(file_name, page_data)
    return file_name
