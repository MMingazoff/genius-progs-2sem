"""
This code parses random wikipedia article and:
1. Counts how many times each word appears in the article.
2. In text finds links to other wikipedia articles and does (1.) with each.
"""
import re
import os
import time
import shutil
from urllib.request import urlopen
from urllib.parse import unquote
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool
from typing import List, Union
from bs4 import BeautifulSoup
from src.parser.file_funcs import list_writer, files_merge
from maps.hash_map import HashMap

ARTICLES_DIRECTORY = os.path.abspath('../../articles')  # where to write articles data
WIKI_RANDOM = "https://ru.wikipedia.org/wiki/Special:Random"
WIKI_DOMAIN = "https://ru.wikipedia.org"


def count_words(html_txt: str, hash_map: HashMap) -> HashMap:
    """
    Counts words in wikipedia article.
    Hashmap is used to count words. Key is a word and value is number of the word in article
    :param html_txt: html text of wiki article
    :param hash_map: hash map to write results
    :return: hashmap (key, value = word, word quantity)
    """
    soup = BeautifulSoup(html_txt, 'html.parser')
    main_txt = soup.find(id="mw-content-text").div
    splitters = (r'\s', r'\.', r'\!', r'\?', r',', r';',
                 r'править \| править код',
                 r'\[', r'\]', r'\(', r'\)', r'\n', r'\\', r'\|')
    splitters = r'|'.join(splitters)  # by this, strings words will be split
    words = re.split(splitters, main_txt.get_text())
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
                return list(url_set)
    return list(url_set)


def url_is_valid(url: str) -> bool:
    """
    Checks if URL leads to other wikipedia article
    :param url: url
    :return: true if url is valid / false if not
    """
    black_list = ['gif', 'jpg', 'svg', 'png', 'ogg']
    if not url.startswith('/wiki/'):
        return False
    if url[-3:len(url)].lower() in black_list:
        return False
    if ':' in url or 'Edit' in url or url.endswith('#identifiers'):
        return False
    return True


def multi_parsing(url: str, mode: Union[ThreadPoolExecutor, Pool], depth: int = 0):
    """
    Parses articles from base articles (found links) and can be repeated multiple times
    :param url: url to base article
    :param mode: multi[threading|processing]
    :param depth: depth of parsing
    :return: None
    """
    curr_urls = [[url]]
    for _ in range(depth+1):
        curr_urls = [new_url for urls in curr_urls for new_url in urls]
        with mode(32) as executor:
            curr_urls = executor.map(wiki_parser, curr_urls)


def wiki_parser(url: str, base_path=ARTICLES_DIRECTORY) -> List[str]:
    """
    1) Gets article heading from url
    2) If the folder with such heading, url, content, words files exist,
    reads content and returns urls from content, else goes next
    3) Sends request, gets page's content and url
    4) If folder doesn't exist, function makes directory (its name's heading) and writes in url
    5) If content file doesn't exist it will be written in binary file
    6) If words file doesn't exist, words will be counted (in alphabetic order) and written
    7) Gets urls from content (firstly it's being decoded) and returns them

    :param url: url to the article
    :param base_path: path where to write files with content etc.
    :return: list with found wiki urls
    """
    heading = unquote(url).split('/wiki/')[-1].replace('_', ' ')

    # checks if url leads to random article
    is_random = False
    if heading == 'Special:Random':
        is_random = True
        with urlopen(url) as response:
            curr_url = response.geturl()
            print(curr_url)
            heading = unquote(curr_url).replace('_', ' ').split('/wiki/')[-1]
            content = response.read()

    heading = heading.replace('?', '(q.mark)')

    # checks if the article's folder already exists
    folder_exists = heading in os.listdir(base_path)
    current_path = os.path.join(base_path, heading)

    url_path = os.path.join(current_path, 'url.txt')
    content_path = os.path.join(current_path, 'content.txt')
    words_path = os.path.join(current_path, 'words.txt')

    if folder_exists and os.path.exists(url_path) \
            and os.path.exists(content_path) and os.path.exists(words_path):
        with open(content_path, 'r', encoding='utf8') as file:
            html = file.read()
        return get_urls(html)

    if not is_random:
        with urlopen(url) as response:
            content = response.read()
            curr_url = response.geturl()

    html = content.decode()

    # if url is new, file with it is written
    if not folder_exists:
        try:
            os.mkdir(current_path)
        except FileExistsError:
            # if such exception occurred than another thread/process is handling this task
            return []
        with open(url_path, 'w', encoding='utf8') as file:
            file.write(curr_url)

    # if content of url doesn't exist it will be written
    if not os.path.exists(content_path):
        with open(content_path, 'wb') as file:
            file.write(content)

    # if words weren't counted than count
    if not os.path.exists(words_path):
        hash_map = HashMap()
        count_words(html, hash_map)
        list_writer(hash_map.sort(), words_path)  # writes all calculated words in file

    # gets urls from article
    return get_urls(html)


if __name__ == '__main__':
    shutil.rmtree(ARTICLES_DIRECTORY)
    os.mkdir(ARTICLES_DIRECTORY)

    print('Parsing using multithreading')
    start = time.time()
    multi_parsing(WIKI_RANDOM, ThreadPoolExecutor, depth=1)
    print(time.time() - start)

    print(len(os.listdir(ARTICLES_DIRECTORY)))

    shutil.rmtree(ARTICLES_DIRECTORY)
    os.mkdir(ARTICLES_DIRECTORY)

    print('Parsing using multiprocessing')
    start = time.time()
    multi_parsing(WIKI_RANDOM, Pool, depth=1)
    print(time.time() - start)

    print(len(os.listdir(ARTICLES_DIRECTORY)))

    print('Merging')
    start = time.time()
    files_merge(*(f'{ARTICLES_DIRECTORY}/{folder}/words.txt'
                  for folder in os.listdir(ARTICLES_DIRECTORY)),
                result_path='res.txt')
    print(time.time() - start)
