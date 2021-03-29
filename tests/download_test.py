import pytest
import os
from page_loader.download import download, url_to_filename, write_file
import requests
import requests_mock

# full_path = f'{os.path.dirname(os.path.abspath(__file__))}/fixtures'


@pytest.fixture()
def url():
    return ("https://ru.hexlet.io/courses",
            'http://test.com')


@pytest.fixture()
def result_url():
    return ("ru-hexlet-io-courses.html",
            "test-com.html")


@pytest.fixture()
def folders():
    return ("/var/tmp",
            )


def test_url_to_filename(url, result_url):
    assert result_url[0] == url_to_filename(url[0])


def test_download(requests_mock, folders, url, result_url):
    test_text = 'test complete'
    requests_mock.get(url[1], text=test_text)
    assert test_text == requests.get(url[1]).text

    dir_res = download(url[1], folders[0])
    dir_check = f'{folders[0]}/{result_url[1]}'
    assert dir_check == dir_res

    with open(dir_check, 'r') as data:
        assert data.read() == test_text
