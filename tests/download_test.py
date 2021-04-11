import pytest
import requests
import requests_mock
import os
from page_loader.download import download, get_file_name, write_file, download_files, write_bin


@pytest.fixture()
def files():
    fls = []
    fixtures_dir = f'{os.path.dirname(os.path.abspath(__file__))}/fixtures'
    names = os.listdir(fixtures_dir)
    for name in names:
        if '.html' in name:
            with open(f'{fixtures_dir}/{name}', 'r') as data:
                fls.append(data.read())

    return fls


@pytest.fixture()
def url():
    return ("https://ru.hexlet.io/courses",
            'http://test.com')


@pytest.fixture()
def folders():
    return ("/var/tmp",
            "/var/tmp/ru-hexlet-io-courses_files")


@pytest.fixture()
def file_names():
    return ("ru-hexlet-io-courses.html",
            "test-com.html",
            "ru-hexlet-io-courses_files",
            "ru-hexlet-io-courses.png",
            "ru-hexlet-io-ru-hexlet-io-lesson.rss")


def test_get_file_name(url, file_names):
    assert file_names[0] == get_file_name(url[0])
    assert file_names[2] == get_file_name(url[0], "_files")
    assert file_names[3] == get_file_name(url[0], ".png")


def test_download(requests_mock, folders, url, file_names):
    test_text = 'test complete'
    requests_mock.get(url[1], text=test_text)
    assert test_text == requests.get(url[1]).text

    dir_res = download(url[1], folders[0])
    dir_check = f'{folders[0]}/{file_names[1]}'
    assert dir_check == dir_res

    with open(dir_check, 'r') as data:
        assert data.read() == test_text


def test_download_2(folders, url, file_names):
    download(url[0], folders[0])

    assert file_names[4] in os.listdir(folders[1])

    with open(f'{folders[0]}/{file_names[0]}', 'r') as data:
        assert f'{file_names[4]}' in data.read()
