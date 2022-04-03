"""
This code parses random wikipedia article.
1. Counts how many times each word appears in the article.
2. In text finds links to other wikipedia articles and does (1.) with each.
"""
import re
import os
import uuid
from urllib.request import urlopen
from typing import List
from bs4 import BeautifulSoup
from src.maps.hash_map import HashMap


def count_words(html_txt: str, hash_map: HashMap) -> HashMap:
    """
    Counts words in wikipedia article.
    Hashmap is used to count words. Key is a word and value is number of the word in article
    :param html_txt: html text of wiki article
    :param hash_map: hash map to write results
    :return: hashmap with (key, value) -> (word, word quantity)
    """
    soup = BeautifulSoup(html_txt, 'html.parser')
    main_txt = soup.find(id="mw-content-text").div
    splitters = (r'\s', r'\.', r'\!', r'\?', r',', r';',
                 r'править \| править код',
                 r'\[', r'\]', r'\(', r'\)', r'\n', r'\\', r'\|')
    splitters = r'|'.join(splitters)
    words = re.split(splitters, main_txt.get_text())  # \s|\[|\]|,|;|\.|\(|\)|\n|\\|
    for word in words:
        if word != '' and word.isalpha():  # to count numbers, isalpha should be changed to isalnum
            lower_word = word.lower()
            hash_map[lower_word] = hash_map.get(lower_word, 0) + 1
    return hash_map


def get_urls(html_txt: str, max_urls=-1) -> list:
    """
    In given wikipedia article finds links to other wikipedia articles
    :param html_txt: html text of wiki article
    :param max_urls: amount of urls required (default '-1' means 'all')
    :return: set of urls
    """
    url_set = set()
    urls = 0
    soup = BeautifulSoup(html_txt, 'html.parser')
    main_txt = soup.find(id="mw-content-text").div
    for link in main_txt.find_all('a'):
        article_link = link.get('href')
        if article_link is not None and url_is_valid(article_link):
            if WIKI_DOMAIN + article_link not in url_set:  # adds only unique urls
                urls += 1
            url_set.add(WIKI_DOMAIN + article_link)
            if urls >= max_urls >= 0:
                return url_set
    return list(url_set)


def get_html(_url: str) -> str:
    """
    Gets html code of website
    :param _url: link
    :return: decoded html
    """
    with urlopen(_url) as response:
        # print(response.geturl())
        response_bytes = response.read()
        return response_bytes.decode("utf8")


def write_html(_url: str, path: str) -> None:
    """
    Writes binary file
    :param _url: url to the article
    :param path: directory where to write
    :return: None
    """
    with open(os.path.join(path, 'content.txt'), 'wb') as file:
        with urlopen(_url) as response:
            file.write(response.read())


def counted_words_sum(words: [list, HashMap]) -> int:
    """
    Calculates how many words were counted
    :param words: iterables that yield LinkedElems which data consists of [word, quantity]
    :return: total number of words in article (with repeats)
    """
    total = 0
    for word in words:
        total += word.data[1]
    return total


def url_is_valid(_url: str) -> bool:
    """
    Checks if URL leads to other wikipedia article
    :param _url: url
    :return: true if url is valid / false if not
    """
    if not _url.startswith('/wiki/'):
        return False
    black_list = ['gif', 'jpg', 'svg']
    if _url[-3:len(_url)] in black_list:
        return False
    if 'Edit' in _url:
        return False
    return True


def wiki_parser(_url: str, base_path: str) -> List[str]:
    """
    0) пробегается по директориям в base_path, сравнивает содержимое файла url.txt
     с параметром url. Если такая найдена то сразу переходим в пункт 2)
    1) в директории по пути base_path создает папку
        со случайно сгенерированным именем. Для генерации можно использовать
        import uuid
        dirname = uuid.uuid4().hex
    2) если папка существовала и в ней уже есть файл content с контентом страницы то её читает
       иначе загружает и записывает в бинарный файл content всё содержимое страницы
    3) из контента вытаскивает текст, считает слова с помощью Map
    4) сериализует мапу в текcтовый файл words.txt в папке
    5) из контента вытаскивает ссылки, фильтрует оставляя только ссылки на викиепедию
       и возвращает список
    :param _url:
    :param base_path:
    :return:
    """
    with urlopen(_url) as response:
        content = response.read()
        curr_url = response.geturl()

    current_path = ''

    folder_exists = False
    for folder in os.listdir(base_path):
        if folder_exists:
            break
        with open(os.path.join(base_path, folder, 'url.txt'), 'r', encoding='utf8') as file:
            line = file.readline()
            if line == curr_url:
                folder_exists = True
                current_path = os.path.join(base_path, folder)

    if not folder_exists:
        new_folder = uuid.uuid4().hex
        current_path = os.path.join(base_path, new_folder)
        os.mkdir(current_path)
        with open(os.path.join(current_path, 'url.txt'), 'w', encoding='utf8') as file:
            file.write(curr_url)

    if not os.path.exists(os.path.join(current_path, 'content.txt')):
        with open(os.path.join(current_path, 'content.txt'), 'wb') as file:
            file.write(content)

    hash_map = HashMap()

    with open(os.path.join(current_path, 'content.txt'), 'r', encoding='utf8') as file:
        html = file.read()

    count_words(html, hash_map)
    hash_map.write(os.path.join(current_path, 'words.txt'))
    return get_urls(html)


if __name__ == '__main__':
    ARTICLES_DIRECTORY = 'C:\\Users\\minga\\PycharmProjects\\Maps\\articles'
    WIKI = "https://ru.wikipedia.org/wiki/Special:Random"
    WIKI_DOMAIN = "https://ru.wikipedia.org"
    print(wiki_parser(WIKI, ARTICLES_DIRECTORY))
