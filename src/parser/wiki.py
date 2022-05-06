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

ARTICLES_DIRECTORY = 'C:/Users/minga/PycharmProjects/Maps/articles'
WIKI_RANDOM = "https://ru.wikipedia.org/wiki/Special:Random"
WIKI_DOMAIN = "https://ru.wikipedia.org"


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


def multi_parsing(url: str, mode: Union[ThreadPoolExecutor, Pool], depth: int = 1):
    """
    :(
    :param url:
    :param mode:
    :param depth:
    :return:
    """
    curr_urls = [url]
    for curr_depth in range(depth+1):
        if curr_depth != 0:
            curr_urls = [new_url for urls in curr_urls for new_url in urls]
        # print(len(curr_urls), curr_urls)
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

    heading = unquote(url).replace('_', ' ').split('/wiki/')[-1]

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

    with urlopen(url) as response:
        content = response.read()
        curr_url = response.geturl()

    html = content.decode()
    # print(curr_url)

    # if url is new, file with it is written
    if not folder_exists:
        try:
            os.mkdir(current_path)
        except FileExistsError:
            print("error")
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
    TEST_URL = "https://ru.wikipedia.org/wiki/%D0%90%D0%B1%D1%83_" \
               "%D0%97%D0%B0%D0%BA%D0%B0%D1%80%D0%B8%D1%8F_" \
               "%D0%AF%D1%85%D1%8C%D1%8F_II_%D0%B0%D0%BB%D1%8C" \
               "-%D0%92%D0%B0%D1%82%D0%B8%D0%BA"

    print('Parsing using multithreading')
    start = time.time()
    multi_parsing(TEST_URL, ThreadPoolExecutor, depth=1)
    print(time.time() - start)

    shutil.rmtree(ARTICLES_DIRECTORY)
    os.mkdir(ARTICLES_DIRECTORY)

    print('Parsing using multiprocessing')
    start = time.time()
    multi_parsing(TEST_URL, Pool, depth=1)
    print(time.time() - start)

    shutil.rmtree(ARTICLES_DIRECTORY)
    os.mkdir(ARTICLES_DIRECTORY)

    print('Parsing coherently')
    start = time.time()
    for _url in wiki_parser(TEST_URL):
        wiki_parser(_url)
    print(time.time() - start)

    print('Merging')
    start = time.time()
    files_merge(*(f'{ARTICLES_DIRECTORY}/{folder}/words.txt'
                  for folder in os.listdir(ARTICLES_DIRECTORY)),
                result_path='res.txt')
    print(time.time() - start)
