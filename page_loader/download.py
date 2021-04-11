import os
import re
import requests
import logging
import sys

from urllib.parse import urlparse
from bs4 import BeautifulSoup
from progress.spinner import Spinner

logger = logging.getLogger(__name__)

logger.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(formatter)
logger.addHandler(stdout_handler)

file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def get_file_name(url='', extension='.html'):
    logger.debug(f'file: {url}, text: {extension}')
    url = re.sub(r'\b(https:|http:|url:|ftp:)[^a-zA-Z ]{2}', '', url)
    return f"{re.sub(r'[^A-Za-z0-9]', '-', url)}{extension}"


def write_file(file='', text=''):
    logger.debug(f'file: {file}, text: {text}')
    try:
        with open(file, 'w', encoding='utf-8') as w:
            w.write(text)
    except Exception as exp:
        logger.error(exp)
        os._exit(0)


def write_bin(file='', binory=[]):
    logger.debug(f'file: {file}, binory: {binory}')
    try:
        os.makedirs(os.path.dirname(file), exist_ok=True)
        with open(file, 'wb') as w:
            w.write(binory)
    except Exception as exp:
        logger.error(exp)
        os._exit(0)


def download_files(data='', folder=os.getcwd(), url=''):
    logger.debug(f'data: {data}, folder: {folder}, url: {url}')
    hostname = urlparse(url).hostname
    soup = BeautifulSoup(data, 'html.parser')

    parts = len(soup.find_all(['img', 'link', 'script']))
    spinner = None
    if (parts != 0):
        spinner = Spinner('Download files ')

    for link in soup.find_all(['img', 'link', 'script']):
        old_name = ''
        if '<link' in str(link):
            old_name = link.get('href')
        else:
            old_name = link.get('src')

        old_name_host = urlparse(old_name).hostname

        try:
            file_suffix = os.path.splitext(old_name)[-1]
        except TypeError:
            continue

        if hostname != old_name_host and old_name_host is not None:
            continue

        old_file_name = old_name.rstrip(file_suffix).lstrip('/')
        new_name = get_file_name(f'{hostname}-{old_file_name}', file_suffix)

        binory = []
        try:
            if 'https' in old_name or 'http' in old_name or 'url' in old_name or 'ftp' in old_name:
                binory = requests.get(old_name).content
            else:
                binory = requests.get(f'http://{hostname}/{old_file_name}{file_suffix}').content
        except Exception as exp:
            logger.error(exp)
            os._exit(0)

        new_src = f'{get_file_name(url, "_files")}/{new_name}'
        write_bin(f'{folder}/{new_src}', binory)
        data = data.replace(old_name, new_src)
        spinner.next()

    if spinner is not None:
        spinner.finish()

    logger.debug(f'data: {data}')
    return data


def download(url='', folder=os.getcwd()):
    logger.debug(f'data: {url}, {folder}')

    if url[-1] == '/':
        url = url[0:-1]

    file_name = f'{folder}/{get_file_name(url)}'

    spinner = Spinner('Download page ')

    page_data = ''
    try:
        page_data = requests.get(url).text
    except Exception as exp:
        logger.error(exp)
        os._exit(0)

    spinner.next()
    spinner.finish()

    page_data = download_files(page_data, folder, url)
    write_file(file_name, page_data)
    return file_name
